"""
Admin Blueprint - All admin management endpoints
"""

import os
from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.models import get_db
from utils.helpers import save_uploaded_file, delete_file
from flask_jwt_extended import get_jwt

admin_bp = Blueprint('admin', __name__)

def admin_required(f):
    from functools import wraps

    @wraps(f)
    @jwt_required()
    def decorated(*args, **kwargs):
        identity = get_jwt_identity()

        claims = get_jwt()

        if claims.get('role') != 'admin':
            return jsonify({'error': 'Admin access required'}), 403

        return f(*args, **kwargs)

    return decorated

@admin_bp.route('/stats', methods=['GET'])
@admin_required
def get_stats():
    """Get admin dashboard statistics."""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) as total FROM users")
    total_users = cursor.fetchone()['total']
    
    cursor.execute("SELECT COUNT(*) as total FROM users WHERE status = 'pending'")
    pending_users = cursor.fetchone()['total']
    
    cursor.execute("SELECT COUNT(*) as total FROM products")
    total_products = cursor.fetchone()['total']
    
    cursor.execute("SELECT COUNT(*) as total FROM inquiries")
    total_inquiries = cursor.fetchone()['total']
    
    cursor.execute("SELECT COUNT(*) as total FROM categories WHERE is_active = 1")
    total_categories = cursor.fetchone()['total']
    
    cursor.close()
    
    return jsonify({
        'total_users': total_users,
        'pending_users': pending_users,
        'total_products': total_products,
        'total_inquiries': total_inquiries,
        'total_categories': total_categories
    })


@admin_bp.route('/users/<int:user_id>/reset-device', methods=['PUT'])
@admin_required
def reset_device(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET device_id = NULL WHERE id = ?", (user_id,))
    conn.commit()
    cursor.close()
    return jsonify({'message': 'Device reset. User can login from new device.'})


# --- User Management ---
@admin_bp.route('/users', methods=['GET'])
@admin_required
def get_users():
    """Get all users with optional filtering."""
    status = request.args.get('status', 'all')
    search = request.args.get('search', '')
    
    conn = get_db()
    cursor = conn.cursor()
    
    where = ["role = 'dealer'"]
    params = []
    
    if status != 'all':
        where.append("status = ?")
        params.append(status)
    
    if search:
        where.append("(full_name LIKE ? OR business_name LIKE ? OR phone LIKE ? OR email LIKE ?)")
        s = f'%{search}%'
        params.extend([s, s, s, s])
    
    where_clause = ' AND '.join(where)
    cursor.execute(f"SELECT * FROM users WHERE {where_clause} ORDER BY created_at DESC", params)
    users = cursor.fetchall()
    cursor.close()
    
    return jsonify({'users': users})

@admin_bp.route('/users/<int:user_id>/approve', methods=['PUT'])
@admin_required
def approve_user(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET status = 'approved' WHERE id = ?", (user_id,))
    conn.commit()
    cursor.close()
    return jsonify({'message': 'User approved'})

@admin_bp.route('/users/<int:user_id>/reject', methods=['PUT'])
@admin_required
def reject_user(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET status = 'rejected' WHERE id = ?", (user_id,))
    conn.commit()
    cursor.close()
    return jsonify({'message': 'User rejected'})

@admin_bp.route('/users/<int:user_id>/block', methods=['PUT'])
@admin_required
def block_user(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET status = 'blocked' WHERE id = ?", (user_id,))
    conn.commit()
    cursor.close()
    return jsonify({'message': 'User blocked'})

# --- Product Management ---

@admin_bp.route('/products', methods=['GET'])
@admin_required
def get_admin_products():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.*, c.name as category_name
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        ORDER BY p.created_at DESC
    """)
    products = cursor.fetchall()
    
    products_list = []
    for p in products:
        p_dict = dict(p)
        cursor.execute("SELECT image_path FROM product_images WHERE product_id = ? LIMIT 1", (p_dict['id'],))
        img = cursor.fetchone()
        p_dict['images'] = [img['image_path']] if img else []
        products_list.append(p_dict)
    
    cursor.close()
    return jsonify({'products': products_list})


@admin_bp.route('/products', methods=['POST'])
@admin_required
def create_product():
    """Create a new product with images and variants."""
    name = request.form.get('name', '').strip()
    if not name:
        return jsonify({'error': 'Product name is required'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Generate slug
    import re
    slug = re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
    
    cursor.execute("""
        INSERT INTO products (name, description, sku, slug, category_id, price, compare_price, stock, moq, discount, is_featured, is_active)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        name,
        request.form.get('description', ''),
        request.form.get('sku', ''),
        slug,
        request.form.get('category_id', type=int),
        request.form.get('price', 0, type=float),
        request.form.get('compare_price', 0, type=float),
        request.form.get('stock', 0, type=int),
        request.form.get('moq', 1, type=int),
        request.form.get('discount', 0, type=int),
        request.form.get('is_featured', 0, type=int),
        request.form.get('is_active', 1, type=int),
    ))
    
    product_id = cursor.lastrowid
    
    # Handle image uploads
    images = request.files.getlist('images')
    for i, img in enumerate(images):
        if img and img.filename:
            path = save_uploaded_file(img, 'images')
            if path:
                cursor.execute("""
                    INSERT INTO product_images (product_id, image_path, is_primary, sort_order)
                    VALUES (?, ?, ?, ?)
                """, (product_id, path, 1 if i == 0 else 0, i))
    
    # Handle colors
    colors_str = request.form.get('colors', '')
    if colors_str:
        for c_name in [c.strip() for c in colors_str.split(',') if c.strip()]:
            cursor.execute("SELECT id FROM colors WHERE LOWER(name) = ?", (c_name.lower(),))
            color = cursor.fetchone()
            if color:
                cursor.execute("INSERT OR IGNORE INTO product_colors (product_id, color_id) VALUES (?, ?)", (product_id, color['id']))
    
    # Handle sizes
    sizes_str = request.form.get('sizes', '')
    if sizes_str:
        for s_name in [s.strip() for s in sizes_str.split(',') if s.strip()]:
            cursor.execute("SELECT id FROM sizes WHERE LOWER(name) = LOWER(?)", (s_name,))
            size = cursor.fetchone()
            if size:
                cursor.execute("INSERT OR IGNORE INTO product_sizes (product_id, size_id) VALUES (?, ?)", (product_id, size['id']))
    # Handle multi-category linking (cat1, cat2, cat3)
    for field in ['cat1_id', 'cat2_id', 'cat3_id']:
        cid = request.form.get(field, type=int)
        if cid:
            cursor.execute("SELECT cat_type FROM categories WHERE id = ?", (cid,))
            crow = cursor.fetchone()
            if crow:
                cursor.execute("""
                    INSERT OR IGNORE INTO product_categories (product_id, category_id, cat_type)
                    VALUES (?, ?, ?)
                """, (product_id, cid, crow['cat_type']))

    conn.commit()
    cursor.close()
    
    return jsonify({'message': 'Product created', 'id': product_id}), 201

@admin_bp.route('/products/<int:product_id>', methods=['PUT', 'POST'])
@admin_required
def update_product(product_id):

    """Update a product."""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        UPDATE products SET name=?, description=?, sku=?, category_id=?, price=?, compare_price=?,
        stock=?, moq=?, discount=?, is_featured=?, is_active=?
        WHERE id=?
    """, (
        request.form.get('name'),
        request.form.get('description'),
        request.form.get('sku'),
        request.form.get('category_id', type=int),
        request.form.get('price', type=float),
        request.form.get('compare_price', type=float),
        request.form.get('stock', type=int),
        request.form.get('moq', type=int),
        request.form.get('discount', type=int),
        request.form.get('is_featured', type=int),
        request.form.get('is_active', type=int),
        product_id
    ))
    
    # Handle new images
    images = request.files.getlist('images')
    for i, img in enumerate(images):
        if img and img.filename:
            path = save_uploaded_file(img, 'images')
            if path:
                cursor.execute("""
                    INSERT INTO product_images (product_id, image_path, is_primary, sort_order)
                    VALUES (?, ?, ?, ?)
                """, (product_id, path, 1 if i == 0 else 0, i))
    
    # Update category links
    for field in ['cat1_id', 'cat2_id', 'cat3_id']:
        cid = request.form.get(field, type=int)
        if cid:
            cursor.execute("SELECT cat_type FROM categories WHERE id = ?", (cid,))
            crow = cursor.fetchone()
            if crow:
                cursor.execute("""
                    INSERT OR IGNORE INTO product_categories (product_id, category_id, cat_type)
                    VALUES (?, ?, ?)
                """, (product_id, cid, crow['cat_type']))
                
    conn.commit()
    cursor.close()
    
    return jsonify({'message': 'Product updated'})

# GET single product for edit
@admin_bp.route('/products/<int:product_id>', methods=['GET'])
@admin_required
def get_admin_product(product_id):
    try:
        conn = get_db()
        cursor = conn.cursor()
        
        # Product basic info
        cursor.execute("SELECT * FROM products WHERE id = ?", (product_id,))
        product = cursor.fetchone()
        
        if not product:
            return jsonify({'error': 'Product not found'}), 404
        
        product_dict = dict(product)
        
        # Images
        cursor.execute("SELECT image_path FROM product_images WHERE product_id = ? ORDER BY sort_order", (product_id,))
        images = [row['image_path'] for row in cursor.fetchall()]
        product_dict['images'] = images
        
        # Colors
        cursor.execute("""
            SELECT c.name FROM product_colors pc
            JOIN colors c ON pc.color_id = c.id
            WHERE pc.product_id = ?
        """, (product_id,))
        colors = [row['name'] for row in cursor.fetchall()]

        product_dict['colors'] = colors
        
        # Sizes
        cursor.execute("""
            SELECT s.name FROM product_sizes ps
            JOIN sizes s ON ps.size_id = s.id
            WHERE ps.product_id = ?
        """, (product_id,))
        sizes = [row['name'] for row in cursor.fetchall()]

        product_dict['sizes'] = sizes
        
        # Category info
        if product_dict.get('category_id'):
            cursor.execute("SELECT id, name, cat_type FROM categories WHERE id = ?", (product_dict['category_id'],))
            cat = cursor.fetchone()
            if cat:
                product_dict['category_name'] = cat['name']
        
        cursor.close()
        return jsonify({'product': product_dict})
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        pass


@admin_bp.route('/products/<int:product_id>', methods=['DELETE'])
@admin_required
def delete_product(product_id):
    conn = None
    try:
        conn = get_db()
        cursor = conn.cursor()
        # Delete related data first
        cursor.execute("DELETE FROM product_images WHERE product_id = ?", (product_id,))
        cursor.execute("DELETE FROM product_colors WHERE product_id = ?", (product_id,))
        cursor.execute("DELETE FROM product_sizes WHERE product_id = ?", (product_id,))
        cursor.execute("DELETE FROM product_categories WHERE product_id = ?", (product_id,))
        cursor.execute("DELETE FROM products WHERE id = ?", (product_id,))
        conn.commit()
        cursor.close()
        return jsonify({'message': 'Product deleted'})
    except Exception as e:
        if conn:
            conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        pass

# --- Inquiry Management ---

@admin_bp.route('/inquiries', methods=['GET'])
@admin_required
def get_all_inquiries():
    limit = request.args.get('limit', 50, type=int)
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT i.*, 
            (SELECT COUNT(*) FROM inquiry_items WHERE inquiry_id = i.id) as items_count
        FROM inquiries i
        ORDER BY i.created_at DESC
        LIMIT ?
    """, (limit,))
    inquiries = cursor.fetchall()
    
    for inq in inquiries:
        cursor.execute("""
            SELECT ii.*, p.name as product_name, p.price as product_price
            FROM inquiry_items ii
            LEFT JOIN products p ON ii.product_id = p.id
            WHERE ii.inquiry_id = ?
        """, (inq['id'],))
        inq['items'] = cursor.fetchall()
    
    cursor.close()
    return jsonify({'inquiries': inquiries})

@admin_bp.route('/inquiries/<int:inquiry_id>', methods=['GET'])
@admin_required
def get_inquiry_details(inquiry_id):

    conn = get_db()
    cursor = conn.cursor()

    # Main inquiry
    cursor.execute("""
        SELECT *
        FROM inquiries
        WHERE id = ?
    """, (inquiry_id,))

    inquiry = cursor.fetchone()

    if not inquiry:
        return jsonify({'error': 'Inquiry not found'}), 404

    # Inquiry items with product images
    cursor.execute("""
        SELECT
            ii.*,
            p.name as product_name,
            p.price as product_price,
            (
                SELECT image_path
                FROM product_images
                WHERE product_id = p.id
                ORDER BY is_primary DESC, sort_order ASC
                LIMIT 1
            ) as image
        FROM inquiry_items ii
        LEFT JOIN products p ON ii.product_id = p.id
        WHERE ii.inquiry_id = ?
    """, (inquiry_id,))

    inquiry['items'] = cursor.fetchall()

    cursor.close()

    return jsonify({
        'inquiry': inquiry
    })


@admin_bp.route('/inquiries/<int:inquiry_id>', methods=['PUT'])
@admin_required
def update_inquiry(inquiry_id):
    data = request.json
    if not data or 'status' not in data:
        return jsonify({'error': 'Status is required'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("UPDATE inquiries SET status = ?, admin_notes = ? WHERE id = ?",
                   (data['status'], data.get('admin_notes', ''), inquiry_id))
    conn.commit()
    cursor.close()
    
    return jsonify({'message': 'Inquiry updated'})

# --- Banners Management ---

@admin_bp.route('/banners', methods=['POST'])
@admin_required
def create_banner():
    from blueprints.banners import create_banner as cb
    return cb()

# --- Catalogues Management ---

@admin_bp.route('/catalogues', methods=['POST'])
@admin_required
def create_catalogue():
    from blueprints.catalogues import create_catalogue as cc
    return cc()

# --- Device Login Request Management ---

@admin_bp.route('/device-requests', methods=['GET'])
@admin_required
def get_device_requests():
    """Get all device login requests."""
    status = request.args.get('status', 'all')
    conn = get_db()
    cursor = conn.cursor()

    if status != 'all':
        cursor.execute("""
            SELECT d.*, u.full_name, u.business_name, u.phone, u.email
            FROM device_login_requests d
            JOIN users u ON d.user_id = u.id
            WHERE d.status = ?
            ORDER BY d.requested_at DESC
        """, (status,))
    else:
        cursor.execute("""
            SELECT d.*, u.full_name, u.business_name, u.phone, u.email
            FROM device_login_requests d
            JOIN users u ON d.user_id = u.id
            ORDER BY d.requested_at DESC
        """)

    requests_list = cursor.fetchall()
    cursor.close()
    return jsonify({'requests': requests_list})


@admin_bp.route('/device-requests/<int:req_id>/approve', methods=['PUT'])
@admin_required
def approve_device_request(req_id):
    """Approve a device login request."""
    from datetime import datetime
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE device_login_requests
        SET status = 'approved', resolved_at = ?
        WHERE id = ?
    """, (datetime.now(), req_id))
    conn.commit()
    cursor.close()
    return jsonify({'message': 'Device approved'})


@admin_bp.route('/device-requests/<int:req_id>/reject', methods=['PUT'])
@admin_required
def reject_device_request(req_id):
    """Reject a device login request."""
    from datetime import datetime
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        UPDATE device_login_requests
        SET status = 'rejected', resolved_at = ?
        WHERE id = ?
    """, (datetime.now(), req_id))
    conn.commit()
    cursor.close()
    return jsonify({'message': 'Device rejected'})