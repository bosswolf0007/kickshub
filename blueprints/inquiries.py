"""
Inquiries Blueprint - Submit and manage order inquiries
"""

from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from models.models import get_db

inquiries_bp = Blueprint('inquiries', __name__)

@inquiries_bp.route('', methods=['GET'])
@jwt_required()
def get_my_inquiries():
    """Get current user's inquiries."""
    identity = get_jwt_identity()
    limit = request.args.get('limit', 20, type=int)
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT i.*, 
            (SELECT COUNT(*) FROM inquiry_items WHERE inquiry_id = i.id) as items_count
        FROM inquiries i
        WHERE i.user_id = ?
        ORDER BY i.created_at DESC
        LIMIT ?
    """, (int(identity), limit))
    inquiries = cursor.fetchall()
    
    cursor.close()
    return jsonify({'inquiries': inquiries})

@inquiries_bp.route('', methods=['POST'])
@jwt_required()
def create_inquiry():
    """Create a new inquiry with order items."""
    identity = get_jwt_identity()
    data = request.json
    
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    items = data.get('items', [])
    if not items:
        return jsonify({'error': 'At least one product is required'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Create inquiry
    cursor.execute("""
        INSERT INTO inquiries (user_id, dealer_name, shop_name, phone, gst_number, address, city, state, pincode, latitude, longitude, notes, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'new')
    """, (
        int(identity),
        data.get('dealer_name', ''),
        data.get('shop_name', ''),
        data.get('phone', ''),
        data.get('gst_number', ''),
        data.get('address', ''),
        data.get('city', ''),
        data.get('state', ''),
        data.get('pincode', ''),
        data.get('latitude'),
        data.get('longitude'),
        data.get('notes', '')
    ))
    
    inquiry_id = cursor.lastrowid
    
    # Add items
    for item in items:
        product_id = item.get('product_id')
        product_name = item.get('product_name', '')
        
        # Get product name if not provided
        if not product_name and product_id:
            cursor.execute("SELECT name FROM products WHERE id = ?", (product_id,))
            prod = cursor.fetchone()
            product_name = prod['name'] if prod else ''
        
        cursor.execute("""
            INSERT INTO inquiry_items (inquiry_id, product_id, product_name, quantity, size, color, price)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            inquiry_id,
            product_id,
            product_name,
            item.get('quantity', 1),
            item.get('size', ''),
            item.get('color', ''),
            item.get('price', 0)
        ))
    
    conn.commit()
    cursor.close()
    
    return jsonify({
        'message': 'Inquiry submitted successfully! We will contact you within 24 hours.',
        'inquiry_id': inquiry_id
    }), 201
