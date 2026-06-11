"""
Contact Blueprint - Contact form submissions
"""

from flask import Blueprint, request, jsonify
from models.models import get_db

contact_bp = Blueprint('contact', __name__)

@contact_bp.route('', methods=['POST'])
def submit_contact():
    """Submit a contact form message."""
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    name = data.get('name', '').strip()
    message = data.get('message', '').strip()
    
    if not name or not message:
        return jsonify({'error': 'Name and message are required'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO contact_messages (name, phone, email, subject, message)
        VALUES (?, ?, ?, ?, ?)
    """, (
        name,
        data.get('phone', ''),
        data.get('email', ''),
        data.get('subject', ''),
        message
    ))
    conn.commit()
    cursor.close()
    
    return jsonify({'message': 'Thank you for your message! We will get back to you soon.'}), 201

@contact_bp.route('/messages', methods=['GET'])
def get_messages():
    """Get contact messages (admin only)."""
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM contact_messages ORDER BY created_at DESC LIMIT 50")
    messages = cursor.fetchall()
    cursor.close()
    return jsonify({'messages': messages})
