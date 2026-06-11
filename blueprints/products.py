"""
Products Blueprint - Browse, Search, Filter Products
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.models import get_db

products_bp = Blueprint('products', __name__)

@products_bp.route('', methods=['GET'])
@jwt_required(optional=True)
def get_products():
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 12, type=int)
    sort = request.args.get('sort', 'latest')
    search = request.args.get('search', '')
    category = request.args.get('category', '')
    featured = request.args.get('featured', 0, type=int)
    exclude = request.args.get('exclude', 0, type=int)
    min_price = request.args.get('min_price', 0, type=float)
    max_price = request.args.get('max_price', 0, type=float)

    offset = (page - 1) * limit
    conn = get_db()
    cursor = conn.cursor()

    where = ["p.is_active = 1"]
    params = []

    if search:
        where.append("(p.name LIKE ? OR p.description LIKE ?)")
        params.extend([f'%{search}%', f'%{search}%'])

    if category:
        # Support filtering by any cat_type (cat1/cat2/cat3) slug
        where.append("""
            (c.slug = ? OR LOWER(c.name) = ?
             OR EXISTS (
                 SELECT 1 FROM product_categories pc2
                 JOIN categories c2 ON pc2.category_id = c2.id
                 WHERE pc2.product_id = p.id AND (c2.slug = ? OR LOWER(c2.name) = ?)
             ))
        """)
        params.extend([category, category, category, category])

    if featured:
        where.append("p.is_featured = 1")

    if exclude:
        where.append("p.id != ?")
        params.append(exclude)

    if min_price > 0:
        where.append("p.price >= ?")
        params.append(min_price)

    if max_price > 0:
        where.append("p.price <= ?")
        params.append(max_price)

    order_map = {
        'latest': 'p.created_at DESC',
        'popular': 'p.stock DESC',
        'name_asc': 'p.name ASC',
        'name_desc': 'p.name DESC',
        'price_asc': 'p.price ASC',
        'price_desc': 'p.price DESC',
    }
    order = order_map.get(sort, 'p.created_at DESC')
    where_clause = ' AND '.join(where) if where else '1=1'

    cursor.execute(f"""
        SELECT COUNT(*) as total FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        WHERE {where_clause}
    """, params)
    total = cursor.fetchone()['total']

    cursor.execute(f"""
        SELECT p.*, c.name as category_name, c.slug as category_slug, b.name as brand_name
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        LEFT JOIN brands b ON p.brand_id = b.id
        WHERE {where_clause}
        ORDER BY {order}
        LIMIT ? OFFSET ?
    """, params + [limit, offset])
    products = cursor.fetchall()

    for product in products:
        cursor.execute("SELECT image_path FROM product_images WHERE product_id = ? ORDER BY is_primary DESC, sort_order ASC LIMIT 5", (product['id'],))
        product['images'] = [r['image_path'] for r in cursor.fetchall()]

        cursor.execute("""
            SELECT c.id, c.name, c.hex_code FROM colors c
            JOIN product_colors pc ON c.id = pc.color_id WHERE pc.product_id = ?
        """, (product['id'],))
        product['colors'] = cursor.fetchall()

        cursor.execute("""
            SELECT s.id, s.name FROM sizes s
            JOIN product_sizes ps ON s.id = ps.size_id
            WHERE ps.product_id = ? ORDER BY s.sort_order
        """, (product['id'],))
        product['sizes'] = cursor.fetchall()

        # Get all linked categories (cat1, cat2, cat3)
        cursor.execute("""
            SELECT c.id, c.name, c.slug, c.cat_type FROM categories c
            JOIN product_categories pc ON c.id = pc.category_id
            WHERE pc.product_id = ?
        """, (product['id'],))
        linked_cats = cursor.fetchall()
        product['cat1'] = next((c for c in linked_cats if c['cat_type'] == 'cat1'), None)
        product['cat2'] = next((c for c in linked_cats if c['cat_type'] == 'cat2'), None)
        product['cat3'] = next((c for c in linked_cats if c['cat_type'] == 'cat3'), None)

    cursor.close()
    return jsonify({'products': products, 'total': total, 'page': page, 'per_page': limit})

@products_bp.route('/<int:product_id>', methods=['GET'])
@jwt_required(optional=True)
def get_product(product_id):
    """Get single product with full details."""
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT p.*, c.name as category_name, c.slug as category_slug, b.name as brand_name
        FROM products p
        LEFT JOIN categories c ON p.category_id = c.id
        LEFT JOIN brands b ON p.brand_id = b.id
        WHERE p.id = ?
    """, (product_id,))
    product = cursor.fetchone()
    
    if not product:
        cursor.close()
        return jsonify({'error': 'Product not found'}), 404
    
    # Get images
    cursor.execute("SELECT image_path FROM product_images WHERE product_id = ? ORDER BY is_primary DESC, sort_order ASC", (product_id,))
    product['images'] = [r['image_path'] for r in cursor.fetchall()]
    
    # Get colors
    cursor.execute("""
        SELECT c.id, c.name, c.hex_code FROM colors c
        JOIN product_colors pc ON c.id = pc.color_id
        WHERE pc.product_id = ?
    """, (product_id,))
    product['colors'] = cursor.fetchall()
    
    # Get sizes
    cursor.execute("""
        SELECT s.id, s.name FROM sizes s
        JOIN product_sizes ps ON s.id = ps.size_id
        WHERE ps.product_id = ? ORDER BY s.sort_order
    """, (product_id,))
    product['sizes'] = cursor.fetchall()
    
    # Get variants
    cursor.execute("""
        SELECT pv.*, c.name as color_name, c.hex_code as color_hex, s.name as size_name
        FROM product_variants pv
        LEFT JOIN colors c ON pv.color_id = c.id
        LEFT JOIN sizes s ON pv.size_id = s.id
        WHERE pv.product_id = ?
    """, (product_id,))
    product['variants'] = cursor.fetchall()
    
    cursor.close()
    
    return jsonify({'product': product})
