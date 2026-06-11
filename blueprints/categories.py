"""
Categories Blueprint
"""

from flask import Blueprint, request, jsonify
from models.models import get_db, query, execute

categories_bp = Blueprint('categories', __name__)

@categories_bp.route('', methods=['GET'])
def get_categories():
    """Get all active categories grouped by cat_type."""
    cat_type = request.args.get('type', '')  # optional filter: cat1, cat2, cat3

    if cat_type:
        cats = query("""
            SELECT c.*,
                (SELECT COUNT(*) FROM products p WHERE p.category_id = c.id AND p.is_active = 1) as product_count
            FROM categories c
            WHERE c.is_active = 1 AND c.cat_type = ?
            ORDER BY c.sort_order ASC, c.name ASC
        """, (cat_type,))
    else:
        cats = query("""
            SELECT c.*,
                (SELECT COUNT(*) FROM products p WHERE p.category_id = c.id AND p.is_active = 1) as product_count
            FROM categories c
            WHERE c.is_active = 1
            ORDER BY c.cat_type ASC, c.sort_order ASC, c.name ASC
        """)

    return jsonify({'categories': cats})

@categories_bp.route('/<int:category_id>', methods=['GET'])
def get_category(category_id):
    """Get a single category."""
    cat = query("SELECT * FROM categories WHERE id = ?", (category_id,), one=True)
    if not cat:
        return jsonify({'error': 'Category not found'}), 404
    return jsonify({'category': cat})

@categories_bp.route('', methods=['POST'])
def create_category():
    """Create a new category."""
    data = request.json
    if not data or not data.get('name'):
        return jsonify({'error': 'Category name is required'}), 400

    import re
    name = data['name'].strip()
    slug = data.get('slug', '').strip() or re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')
    cat_type = data.get('cat_type', 'cat3')
    parent_id = data.get('parent_id', None)

    cat_id = execute("""
        INSERT INTO categories (name, slug, description, icon, parent_id, cat_type, sort_order)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    """, (name, slug, data.get('description', ''), data.get('icon', '📁'), parent_id, cat_type, data.get('sort_order', 0)))

    return jsonify({'message': 'Category created', 'id': cat_id}), 201

@categories_bp.route('/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    """Update a category."""
    data = request.json
    if not data:
        return jsonify({'error': 'No data'}), 400
    
    execute("""
        UPDATE categories SET name=?, description=?, icon=?, is_active=?
        WHERE id=?
    """, (data.get('name'), data.get('description'), data.get('icon'), data.get('is_active', 1), category_id))
    
    return jsonify({'message': 'Category updated'})

@categories_bp.route('/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    """Delete a category."""
    execute("DELETE FROM categories WHERE id = ?", (category_id,))
    return jsonify({'message': 'Category deleted'})
