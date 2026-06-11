"""
Catalogues Blueprint - PDF Catalogue Management
"""

from flask import Blueprint, request, jsonify, send_file
from models.models import get_db
from utils.helpers import save_uploaded_file

catalogues_bp = Blueprint('catalogues', __name__)

@catalogues_bp.route('', methods=['GET'])
def get_catalogues():
    """Get all active catalogues."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT cat.*, c.name as category_name
        FROM catalogues cat
        LEFT JOIN categories c ON cat.category_id = c.id
        WHERE cat.is_active = 1
        ORDER BY cat.created_at DESC
    """)
    catalogues = cursor.fetchall()
    cursor.close()
    return jsonify({'catalogues': catalogues})

@catalogues_bp.route('', methods=['POST'])
def create_catalogue():
    """Upload a new catalogue PDF."""
    title = request.form.get('title', '').strip()
    if not title:
        return jsonify({'error': 'Title is required'}), 400
    
    pdf_file = request.files.get('pdf')
    if not pdf_file or not pdf_file.filename:
        return jsonify({'error': 'PDF file is required'}), 400
    
    pdf_path = save_uploaded_file(pdf_file, 'catalogues')
    if not pdf_path:
        return jsonify({'error': 'Failed to save PDF'}), 500
    
    cover_image = None
    cover = request.files.get('cover')
    if cover and cover.filename:
        cover_image = save_uploaded_file(cover, 'images')
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO catalogues (title, description, category_id, pdf_path, cover_image)
        VALUES (?, ?, ?, ?, ?)
    """, (title, request.form.get('description', ''), request.form.get('category_id', type=int), pdf_path, cover_image))
    conn.commit()
    catalogue_id = cursor.lastrowid
    cursor.close()
    
    return jsonify({'message': 'Catalogue uploaded', 'id': catalogue_id}), 201

@catalogues_bp.route('/<int:catalogue_id>/download')
def download_catalogue(catalogue_id):
    """Download a catalogue PDF."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM catalogues WHERE id = ?", (catalogue_id,))
    catalogue = cursor.fetchone()
    cursor.close()
    
    if not catalogue or not catalogue['pdf_path']:
        return jsonify({'error': 'Catalogue not found'}), 404
    
    import os
    from flask import current_app
    pdf_full_path = os.path.join(current_app.config['UPLOAD_FOLDER'], catalogue['pdf_path'])
    
    if not os.path.exists(pdf_full_path):
        return jsonify({'error': 'File not found'}), 404
    
    return send_file(pdf_full_path, as_attachment=True, download_name=f"{catalogue['title']}.pdf")
