"""
KicksHub DB Fix Script
Run this from your backend folder: python3 fix_db.py
"""

import sqlite3
import os
import sys

# ── DB path find பண்ணு ──────────────────────────────────────
possible_paths = [
    'kickshub.db',
    '../kickshub.db',
    'backend/kickshub.db',
    'instance/kickshub.db',
]

db_path = None
for p in possible_paths:
    if os.path.exists(p):
        db_path = p
        break

if not db_path:
    # Current directory-ல் .db files தேடு
    for root, dirs, files in os.walk('.'):
        for f in files:
            if f.endswith('.db'):
                db_path = os.path.join(root, f)
                break
        if db_path:
            break

if not db_path:
    print("❌ kickshub.db file கண்டுபிடிக்கல!")
    print("   இந்த script-ஐ backend folder-ல் run பண்ணு")
    print("   அல்லது DB path manually set பண்ணு:")
    print("   db_path = '/path/to/kickshub.db'")
    sys.exit(1)

print(f"✅ DB found: {db_path}")

conn = sqlite3.connect(db_path)
conn.row_factory = sqlite3.Row
conn.execute("PRAGMA foreign_keys = OFF")  # fix பண்றப்போ temporarily off

# ── Step 1: device_logins table create பண்ணு ───────────────
print("\n📋 Step 1: device_logins table...")
conn.execute("""
CREATE TABLE IF NOT EXISTS device_logins (
    id          INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id     INTEGER NOT NULL,
    fingerprint TEXT    NOT NULL,
    user_agent  TEXT,
    ip_address  TEXT,
    status      TEXT    NOT NULL DEFAULT 'pending',
    created_at  DATETIME DEFAULT CURRENT_TIMESTAMP,
    approved_at DATETIME,
    UNIQUE(user_id, fingerprint),
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
)
""")
conn.execute("""
CREATE INDEX IF NOT EXISTS idx_device_logins_status 
ON device_logins(status)
""")
conn.execute("""
CREATE INDEX IF NOT EXISTS idx_device_logins_user 
ON device_logins(user_id)
""")
conn.commit()
print("   ✅ device_logins table ready")

# ── Step 2: Admin user இருக்கான்னு check பண்ணு ─────────────
print("\n👤 Step 2: Admin user check...")
cur = conn.cursor()
cur.execute("SELECT id, email, status, password_hash FROM users WHERE role='admin'")
admins = cur.fetchall()

if not admins:
    print("   ⚠️  Admin user இல்லை! Create பண்றோம்...")
    try:
        from werkzeug.security import generate_password_hash
        pw_hash = generate_password_hash('admin123')
    except ImportError:
        # werkzeug இல்லன்னா simple hash use பண்ணு (dev only)
        import hashlib
        pw_hash = hashlib.sha256('admin123'.encode()).hexdigest()
        print("   ⚠️  werkzeug இல்லை, SHA256 hash use பண்றோம் (dev only)")

    conn.execute("""
        INSERT OR IGNORE INTO users 
            (full_name, business_name, email, phone, password_hash, role, status, 
             address, city, state, pincode)
        VALUES (
            'Admin KicksHub', 'KicksHub Wholesale',
            'admin@kickshub.in', '9876543210',
            ?, 'admin', 'approved',
            '123, Footwear Market, BKC Complex',
            'Mumbai', 'Maharashtra', '400051'
        )
    """, (pw_hash,))
    conn.commit()
    print("   ✅ Admin created: admin@kickshub.in / admin123")
else:
    print(f"   Found {len(admins)} admin(s):")
    for a in admins:
        print(f"   - {a['email']} (status: {a['status']})")
        
        # Password hash valid-ஆ இருக்கான்னு check பண்ணு
        ph = a['password_hash']
        is_valid_hash = (
            ph.startswith('$2b$') or  # bcrypt
            ph.startswith('$2a$') or  # bcrypt alt
            ph.startswith('pbkdf2:')  or  # werkzeug pbkdf2
            ph.startswith('scrypt:')      # werkzeug scrypt
        )
        
        if not is_valid_hash:
            print(f"   ⚠️  Hash invalid ({ph[:20]}...) — fix பண்றோம்")
            try:
                from werkzeug.security import generate_password_hash
                new_hash = generate_password_hash('admin123')
                conn.execute(
                    "UPDATE users SET password_hash=? WHERE id=?",
                    (new_hash, a['id'])
                )
                conn.commit()
                print(f"   ✅ Password hash updated")
            except ImportError:
                print("   ❌ werkzeug இல்லை — pip install werkzeug")
        else:
            print(f"   ✅ Hash valid ({ph[:15]}...)")
            
            # Login test பண்ணு
            try:
                from werkzeug.security import check_password_hash
                if check_password_hash(ph, 'admin123'):
                    print("   ✅ Password 'admin123' works!")
                else:
                    print("   ❌ Password 'admin123' WRONG — reset பண்றோம்")
                    from werkzeug.security import generate_password_hash
                    new_hash = generate_password_hash('admin123')
                    conn.execute(
                        "UPDATE users SET password_hash=? WHERE id=?",
                        (new_hash, a['id'])
                    )
                    conn.commit()
                    print("   ✅ Password reset to 'admin123'")
            except ImportError:
                print("   ⚠️  werkzeug இல்லை, password test skip")

# ── Step 3: Admin-ஓட device auto-approve பண்ணு ─────────────
print("\n📱 Step 3: Existing admin device entries check...")
cur.execute("SELECT COUNT(*) as c FROM device_logins WHERE status='pending'")
pending = cur.fetchone()['c']
print(f"   Pending devices: {pending}")

# ── Step 4: Table structure verify ──────────────────────────
print("\n🔍 Step 4: Final verification...")
cur.execute("SELECT name FROM sqlite_master WHERE type='table' ORDER BY name")
tables = [r['name'] for r in cur.fetchall()]
print(f"   Tables: {', '.join(tables)}")

required = ['users', 'products', 'categories', 'device_logins', 'inquiries']
for t in required:
    status = "✅" if t in tables else "❌ MISSING"
    print(f"   {status} {t}")

cur.execute("SELECT COUNT(*) as c FROM users WHERE role='admin' AND status='approved'")
admin_count = cur.fetchone()['c']
print(f"\n   Approved admins: {admin_count}")

conn.execute("PRAGMA foreign_keys = ON")
conn.close()

print("\n" + "="*50)
print("✅ DB fix complete!")
print("="*50)
print("\nNext steps:")
print("1. Backend restart பண்ணு (Ctrl+C then python app.py)")
print("2. Browser-ல் login பண்ணு: admin@kickshub.in / admin123")
print("3. /admin/devices page-ல் data வருது check பண்ணு")