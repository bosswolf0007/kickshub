import os
import re
import uuid
from werkzeug.utils import secure_filename
from flask import current_app

def allowed_file(filename, allowed_extensions=None):
    """Check if file has an allowed extension."""
    if allowed_extensions is None:
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'pdf'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions

def save_uploaded_file(file, subfolder='images'):
    """Save an uploaded file and return the filename."""
    if not file:
        return None
    
    # Create upload directory if not exists
    upload_dir = os.path.join(current_app.config['UPLOAD_FOLDER'], subfolder)
    os.makedirs(upload_dir, exist_ok=True)
    
    # Generate unique filename
    original_name = secure_filename(file.filename)
    ext = original_name.rsplit('.', 1)[1].lower() if '.' in original_name else ''
    unique_name = f"{uuid.uuid4().hex}_{int(__import__('time').time())}.{ext}"
    
    file_path = os.path.join(upload_dir, unique_name)
    file.save(file_path)
    
    return os.path.join(subfolder, unique_name)

def delete_file(filepath):
    """Delete a file from the uploads folder."""
    if not filepath:
        return
    full_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filepath)
    try:
        if os.path.exists(full_path):
            os.remove(full_path)
    except Exception:
        pass

def validate_email(email):
    """Validate email format."""
    pattern = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
    return re.match(pattern, email) is not None

def validate_phone(phone):
    """Validate Indian phone number."""
    pattern = r'^[6-9]\d{9}$'
    return re.match(pattern, str(phone)) is not None

def validate_gst(gst):
    """Validate GST number format."""
    pattern = r'^[0-9]{2}[A-Z]{5}[0-9]{4}[A-Z]{1}[1-9A-Z]{1}Z[0-9A-Z]{1}$'
    return re.match(pattern, str(gst).upper()) is not None

def format_currency(amount):
    """Format amount in Indian Rupee format."""
    try:
        amount = float(amount)
        if amount >= 10000000:
            return f"₹{amount/10000000:.2f}Cr"
        elif amount >= 100000:
            return f"₹{amount/100000:.2f}L"
        else:
            return f"₹{amount:,.2f}"
    except (ValueError, TypeError):
        return f"₹0.00"

def paginate(query, page=1, per_page=20):
    """Simple pagination helper."""
    page = max(1, int(page))
    per_page = min(100, max(1, int(per_page)))
    offset = (page - 1) * per_page
    return offset, per_page

def json_response(data=None, message='Success', status=200, error=None):
    """Create a standardized JSON response."""
    response = {'message': message, 'status': status}
    if data is not None:
        response['data'] = data
    if error:
        response['error'] = error
    return response, status
