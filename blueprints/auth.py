"""
Authentication Blueprint - Login, Register, Forgot/Reset Password, Profile
"""

import hashlib
import secrets
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, session
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from werkzeug.security import generate_password_hash, check_password_hash
from models.models import get_db, query, execute

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new dealer account."""
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    full_name = data.get('full_name', '').strip()
    phone = data.get('phone', '').strip()
    password = data.get('password', '')
    
    if not full_name or not phone or not password:
        return jsonify({'error': 'Name, phone and password are required'}), 400
    
    if len(password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    
    # Check if phone already exists
    cursor.execute("SELECT id FROM users WHERE phone = ?", (phone,))
    if cursor.fetchone():
        cursor.close()
        return jsonify({'error': 'Phone number already registered'}), 400
    
    # Check email if provided
    email = data.get('email', '').strip()
    if email:
        cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
        if cursor.fetchone():
            cursor.close()
            return jsonify({'error': 'Email already registered'}), 400
    
    password_hash = generate_password_hash(password)
    
    cursor.execute("""
        INSERT INTO users (full_name, business_name, email, phone, password_hash, gst_number, address, city, state, pincode, role, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'dealer', 'pending')
    """, (
        full_name,
        data.get('business_name', '').strip(),
        email,
        phone,
        password_hash,
        data.get('gst_number', '').strip().upper(),
        data.get('address', '').strip(),
        data.get('city', '').strip(),
        data.get('state', '').strip(),
        data.get('pincode', '').strip()
    ))
    
    conn.commit()
    user_id = cursor.lastrowid
    cursor.close()
    
    return jsonify({
        'message': 'Registration successful! Your account is pending approval.',
        'user_id': user_id
    }), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    """Authenticate a user and create session."""
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400

    login_id = data.get('email', '').strip()
    password = data.get('password', '')

    if not login_id or not password:
        return jsonify({'error': 'Email/Phone and password are required'}), 400

    conn = get_db()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE email = ? OR phone = ?", (login_id, login_id))
    user = cursor.fetchone()

    if not user or not check_password_hash(user['password_hash'], password):
        cursor.close()
        return jsonify({'error': 'Invalid credentials'}), 401

    # --- Device login check (only for approved dealers) ---
    device_id = data.get('device_id', '').strip()
    if device_id and user['role'] == 'dealer' and user['status'] == 'approved':
        registered_device = user.get('device_id') if isinstance(user, dict) else None
        if not registered_device:
            cursor.execute("UPDATE users SET device_id = ? WHERE id = ?", (device_id, user['id']))
            conn.commit()
        elif registered_device != device_id:
            cursor.close()
            return jsonify({
                'error': 'device_locked',
                'message': 'This account is registered on another device. Please contact admin.'
            }), 403

    # Create JWT token
    access_token = create_access_token(
        identity=str(user['id']),
        additional_claims={'role': user['role']},
        expires_delta=timedelta(days=7)
    )

    session['user_id'] = user['id']
    session['role'] = user['role']

    user_data = {
        'id': user['id'],
        'full_name': user['full_name'],
        'business_name': user['business_name'],
        'email': user['email'],
        'phone': user['phone'],
        'gst_number': user['gst_number'],
        'address': user['address'],
        'city': user['city'],
        'state': user['state'],
        'pincode': user['pincode'],
        'role': user['role'],
        'status': user['status'],
    }

    cursor.close()
    return jsonify({
        'message': 'Login successful',
        'token': access_token,
        'user': user_data
    })


@auth_bp.route('/session', methods=['GET'])
def check_session():
    """Check if user has an active session."""
    from flask_jwt_extended import decode_token
    from flask_jwt_extended.exceptions import JWTExtendedException
    from jwt.exceptions import PyJWTError
    
    auth_header = request.headers.get('Authorization', '')
    if not auth_header.startswith('Bearer '):
        return jsonify({'user': None}), 200
    
    token = auth_header.split(' ')[1]
    
    try:
        decoded = decode_token(token)
        identity = decoded.get('sub')
        if not identity:
            return jsonify({'user': None}), 200
    except Exception:
        # Token invalid, expired, or wrong format (e.g. old mock token)
        return jsonify({'user': None}), 200

    try:
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE id = ?", (int(identity),))
        user = cursor.fetchone()
        cursor.close()

        if not user or user['status'] == 'blocked':
            return jsonify({'user': None}), 200

        user_data = {
            'id': user['id'],
            'full_name': user['full_name'],
            'business_name': user['business_name'],
            'email': user['email'],
            'phone': user['phone'],
            'gst_number': user['gst_number'],
            'address': user['address'],
            'city': user['city'],
            'state': user['state'],
            'pincode': user['pincode'],
            'role': user['role'],
            'status': user['status'],
        }
        return jsonify({'user': user_data})
    except Exception as e:
        return jsonify({'user': None}), 200
    
@auth_bp.route('/logout', methods=['POST'])
def logout():
    """Logout user and clear session."""
    session.clear()
    return jsonify({'message': 'Logged out successfully'})

@auth_bp.route('/profile', methods=['PUT'])
@jwt_required()
def update_profile():
    """Update user profile."""
    identity = get_jwt_identity()
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    
    update_fields = []
    params = []
    
    for field in ['full_name', 'business_name', 'email', 'phone', 'gst_number', 'address', 'city', 'state', 'pincode']:
        if field in data:
            update_fields.append(f"{field} = ?")
            params.append(data[field])
    
    if data.get('password'):
        password_hash = generate_password_hash(data['password'])
        update_fields.append("password_hash = ?")
        params.append(password_hash)
    
    if update_fields:
        params.append(int(identity))
        cursor.execute(f"UPDATE users SET {', '.join(update_fields)} WHERE id = ?", params)
        conn.commit()
    
    cursor.execute("SELECT * FROM users WHERE id = ?", (int(identity),))
    user = cursor.fetchone()
    cursor.close()
    
    user_data = {
        'id': user['id'],
        'full_name': user['full_name'],
        'business_name': user['business_name'],
        'email': user['email'],
        'phone': user['phone'],
        'gst_number': user['gst_number'],
        'address': user['address'],
        'city': user['city'],
        'state': user['state'],
        'pincode': user['pincode'],
        'role': user['role'],
        'status': user['status'],
    }
    
    return jsonify({'message': 'Profile updated', 'user': user_data})

@auth_bp.route('/forgot-password', methods=['POST'])
def forgot_password():
    """Send password reset token."""
    data = request.json
    email = data.get('email', '').strip()
    
    if not email:
        return jsonify({'error': 'Email is required'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT id FROM users WHERE email = ?", (email,))
    user = cursor.fetchone()
    
    if not user:
        return jsonify({'message': 'If the email exists, a reset link has been sent'}), 200
    
    token = secrets.token_urlsafe(32)
    expires = datetime.now() + timedelta(hours=1)
    
    cursor.execute("""
        INSERT INTO password_resets (user_id, token, expires_at)
        VALUES (?, ?, ?)
    """, (user['id'], token, expires))
    conn.commit()
    cursor.close()
    
    # In production, send actual email here
    print(f"Password reset token for {email}: {token}")
    
    return jsonify({
        'message': 'If the email exists, a reset link has been sent',
        'token': token  # Remove in production
    })

@auth_bp.route('/reset-password', methods=['POST'])
def reset_password():
    """Reset password using token."""
    data = request.json
    token = data.get('token', '')
    new_password = data.get('password', '')
    
    if not token or not new_password:
        return jsonify({'error': 'Token and password are required'}), 400
    
    if len(new_password) < 6:
        return jsonify({'error': 'Password must be at least 6 characters'}), 400
    
    conn = get_db()
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT * FROM password_resets
        WHERE token = ? AND used = 0 AND expires_at > datetime('now')
    """, (token,))
    reset = cursor.fetchone()
    
    if not reset:
        cursor.close()
        return jsonify({'error': 'Invalid or expired token'}), 400
    
    password_hash = generate_password_hash(new_password)
    cursor.execute("UPDATE users SET password_hash = ? WHERE id = ?", (password_hash, reset['user_id']))
    cursor.execute("UPDATE password_resets SET used = 1 WHERE id = ?", (reset['id'],))
    conn.commit()
    cursor.close()
    
    return jsonify({'message': 'Password reset successfully'})