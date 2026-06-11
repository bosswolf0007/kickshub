"""
Banners Blueprint
"""

from flask import Blueprint, request, jsonify
from models.models import get_db
from utils.helpers import save_uploaded_file

banners_bp = Blueprint('banners', __name__)

@banners_bp.route('', methods=['GET'])
def get_banners():
    """Get active banners."""
    banner_type = request.args.get('type', 'home')
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM banners WHERE is_active = 1 AND (type = ? OR ? = '')
        ORDER BY sort_order ASC
    """, (banner_type, banner_type))
    banners = cursor.fetchall()
    cursor.close()
    return jsonify({'banners': banners})

@banners_bp.route('', methods=['POST'])
def create_banner():
    """Create a new banner."""
    title = request.form.get('title', '')
    subtitle = request.form.get('subtitle', '')
    link = request.form.get('link', '')
    banner_type = request.form.get('type', 'home')
    image = request.files.get('image')
    
    image_path = None
    if image and image.filename:
        image_path = save_uploaded_file(image, 'banners')
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO banners (title, subtitle, image_path, link_url, type)
        VALUES (?, ?, ?, ?, ?)
    """, (title, subtitle, image_path, link, banner_type))
    conn.commit()
    banner_id = cursor.lastrowid
    cursor.close()
    
    return jsonify({'message': 'Banner created', 'id': banner_id}), 201

@banners_bp.route('/<int:banner_id>', methods=['DELETE'])
def delete_banner(banner_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM banners WHERE id = ?", (banner_id,))
    conn.commit()
    cursor.close()
    return jsonify({'message': 'Banner deleted'})
