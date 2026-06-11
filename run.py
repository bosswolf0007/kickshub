#!/usr/bin/env python3
"""
KicksHub B2B Footwear Wholesale - Server Runner
Run: python run.py
"""

import os
import sys

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app

if __name__ == '__main__':
    app = create_app()
    
    # Create database tables on first run
    with app.app_context():
        try:
            from models.models import init_db
            init_db()
        except Exception as e:
            print(f"⚠️ Database init skipped: {e}")
            print("   Make sure MySQL is running and database 'kickshub' exists.")
    
    print("""
    ╔══════════════════════════════════════════╗
    ║     👟 KicksHub Wholesale Platform      ║
    ║     B2B Footwear Ordering System         ║
    ║──────────────────────────────────────────║
    ║  Frontend:  http://localhost:5173        ║
    ║  API:       http://localhost:5000/api    ║
    ║  Admin:     Login as admin@kickshub.in   ║
    ╚══════════════════════════════════════════╝
    """)
    
    app.run(
        host=app.config['HOST'],
        port=app.config['PORT'],
        debug=app.config['DEBUG']
    )
