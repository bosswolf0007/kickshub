#!/usr/bin/env python3
"""
KicksHub - B2B Footwear Wholesale Platform
Flask Application Entry Point
"""

import os
import sys
from flask import Flask, send_from_directory, jsonify, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager, jwt_required
from config import config_by_name
from models.models import get_db
import sqlite3


# Create upload directories
upload_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')
for sub in ['images', 'catalogues', 'banners']:
    os.makedirs(os.path.join(upload_dir, sub), exist_ok=True)

def create_app(config_name='default'):
    app = Flask(__name__, static_folder='../dist', static_url_path='')
    # Initialize extensions
    app.config.from_object(config_by_name.get(config_name, config_by_name['default']))
    app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

    CORS(app,
        supports_credentials=True,
        origins=['http://localhost:5173', 'http://localhost:3000', 'http://localhost:5000'],
        methods=['GET', 'POST', 'PUT', 'DELETE', 'PATCH', 'OPTIONS'],
        allow_headers=['Content-Type', 'Authorization', 'X-Requested-With']
    )

    JWTManager(app)

    # SQLite WAL mode — concurrent access fix
    def init_sqlite_settings():
        try:
            conn = get_db()
            conn.execute("PRAGMA journal_mode=WAL")
            conn.execute("PRAGMA busy_timeout=10000")
            conn.execute("PRAGMA synchronous=NORMAL")
            conn.close()
        except Exception as e:
            print(f"SQLite pragma setup: {e}")

    with app.app_context():
        init_sqlite_settings()

    
    # Session setup
    app.config['SESSION_TYPE'] = 'filesystem'
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'kickshub-secret-key-2024')
    
    # Register Blueprints
    from blueprints.auth import auth_bp
    from blueprints.products import products_bp
    from blueprints.categories import categories_bp
    from blueprints.inquiries import inquiries_bp
    from blueprints.admin import admin_bp
    from blueprints.banners import banners_bp
    from blueprints.catalogues import catalogues_bp
    from blueprints.contact import contact_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(products_bp, url_prefix='/api/products')
    app.register_blueprint(categories_bp, url_prefix='/api/categories')
    app.register_blueprint(inquiries_bp, url_prefix='/api/inquiries')
    app.register_blueprint(admin_bp, url_prefix='/api/admin')
    app.register_blueprint(banners_bp, url_prefix='/api/banners')
    app.register_blueprint(catalogues_bp, url_prefix='/api/catalogues')
    app.register_blueprint(contact_bp, url_prefix='/api/contact')
    
    # Dashboard stats endpoint
    @app.route('/api/dashboard/stats')
    @jwt_required()
    def dashboard_stats():
        from flask_jwt_extended import jwt_required, get_jwt_identity
        from models.models import get_db
        get_jwt_identity()
        
        try:
            identity = get_jwt_identity()
        except:
            return jsonify({'error': 'Not authenticated'}), 401
        
        conn = get_db()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) as total FROM products WHERE is_active=1")
        total_products = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as total FROM inquiries WHERE user_id=?", (int(identity),))
        my_inquiries = cursor.fetchone()['total']
        
        cursor.close()
        
        return jsonify({'total_products': total_products, 'my_inquiries': my_inquiries})
    
    
    # Serve uploaded files
    @app.route('/api/uploads/<path:filename>')
    def serve_upload(filename):
        return send_from_directory(os.path.join(app.config['UPLOAD_FOLDER']), filename)
    
    # Serve frontend for SPA
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_frontend(path):
        if path and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        return send_from_directory(app.static_folder, 'index.html')
    
    return app

if __name__ == '__main__':
    app = create_app()
    print(f"🚀 KicksHub API Server starting on {app.config['HOST']}:{app.config['PORT']}")
    app.run(host=app.config['HOST'], port=app.config['PORT'], debug=app.config['DEBUG'])
