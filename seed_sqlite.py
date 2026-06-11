#!/usr/bin/env python3
"""
KicksHub - SQLite Database Seed Script
Works WITHOUT MySQL! Uses SQLite (built into Python).

Usage:
    python seed_sqlite.py              # Full seed
    python seed_sqlite.py --force      # Delete & reseed
"""

import os
import sys
import sqlite3
import random
import json
import argparse
import shutil
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

DB_PATH = os.path.join(os.path.dirname(__file__), 'kickshub.db')

def get_conn():
    return sqlite3.connect(DB_PATH)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def create_tables(conn):
    """Create all tables for SQLite."""
    cursor = conn.cursor()
    
    cursor.executescript("""
        PRAGMA foreign_keys = OFF;
        
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            full_name TEXT NOT NULL,
            business_name TEXT,
            email TEXT UNIQUE,
            phone TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL,
            gst_number TEXT,
            address TEXT,
            city TEXT,
            state TEXT,
            pincode TEXT,
            role TEXT DEFAULT 'dealer',
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            slug TEXT UNIQUE,
            description TEXT,
            icon TEXT,
            parent_id INTEGER DEFAULT NULL,
            cat_type TEXT DEFAULT 'cat3',
            is_active INTEGER DEFAULT 1,
            sort_order INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (parent_id) REFERENCES categories(id) ON DELETE SET NULL
        );

        CREATE TABLE IF NOT EXISTS brands (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            slug TEXT UNIQUE,
            description TEXT,
            logo TEXT,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS colors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            hex_code TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS sizes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category_type TEXT,
            sort_order INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS products (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            description TEXT,
            sku TEXT UNIQUE,
            slug TEXT UNIQUE,
            product_number INTEGER,
            category_id INTEGER,
            brand_id INTEGER,
            price REAL NOT NULL DEFAULT 0,
            compare_price REAL DEFAULT 0,
            cost_price REAL DEFAULT 0,
            stock INTEGER DEFAULT 0,
            moq INTEGER DEFAULT 1,
            discount INTEGER DEFAULT 0,
            weight REAL DEFAULT 0,
            is_featured INTEGER DEFAULT 0,
            is_active INTEGER DEFAULT 1,
            meta_title TEXT,
            meta_description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL,
            FOREIGN KEY (brand_id) REFERENCES brands(id) ON DELETE SET NULL
        );

        CREATE TABLE IF NOT EXISTS product_images (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            image_path TEXT NOT NULL,
            is_primary INTEGER DEFAULT 0,
            sort_order INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS product_variants (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            color_id INTEGER,
            size_id INTEGER,
            price REAL,
            stock INTEGER DEFAULT 0,
            sku TEXT,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
            FOREIGN KEY (color_id) REFERENCES colors(id) ON DELETE SET NULL,
            FOREIGN KEY (size_id) REFERENCES sizes(id) ON DELETE SET NULL
        );

        CREATE TABLE IF NOT EXISTS product_meta (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            meta_key TEXT,
            meta_value TEXT,
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS product_colors (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            color_id INTEGER NOT NULL,
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
            FOREIGN KEY (color_id) REFERENCES colors(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS product_sizes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            size_id INTEGER NOT NULL,
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
            FOREIGN KEY (size_id) REFERENCES sizes(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS inquiries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            dealer_name TEXT NOT NULL,
            shop_name TEXT,
            phone TEXT NOT NULL,
            gst_number TEXT,
            address TEXT,
            city TEXT,
            state TEXT,
            pincode TEXT,
            latitude REAL,
            longitude REAL,
            notes TEXT,
            status TEXT DEFAULT 'new',
            admin_notes TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE SET NULL
        );

        CREATE TABLE IF NOT EXISTS inquiry_items (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            inquiry_id INTEGER NOT NULL,
            product_id INTEGER,
            product_name TEXT,
            quantity INTEGER DEFAULT 1,
            size TEXT,
            color TEXT,
            price REAL,
            FOREIGN KEY (inquiry_id) REFERENCES inquiries(id) ON DELETE CASCADE,
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE SET NULL
        );

        CREATE TABLE IF NOT EXISTS banners (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT,
            subtitle TEXT,
            image_path TEXT,
            link_url TEXT,
            type TEXT DEFAULT 'home',
            is_active INTEGER DEFAULT 1,
            sort_order INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS catalogues (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            title TEXT NOT NULL,
            description TEXT,
            category_id INTEGER,
            pdf_path TEXT NOT NULL,
            cover_image TEXT,
            is_active INTEGER DEFAULT 1,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
        );

        CREATE TABLE IF NOT EXISTS contact_messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT,
            email TEXT,
            subject TEXT,
            message TEXT NOT NULL,
            is_read INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            setting_key TEXT UNIQUE NOT NULL,
            setting_value TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS password_resets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            token TEXT NOT NULL,
            expires_at TIMESTAMP NOT NULL,
            used INTEGER DEFAULT 0,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
        );
                         
        CREATE TABLE IF NOT EXISTS product_categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            product_id INTEGER NOT NULL,
            category_id INTEGER NOT NULL,
            cat_type TEXT NOT NULL,
            UNIQUE(product_id, category_id),
            FOREIGN KEY (product_id) REFERENCES products(id) ON DELETE CASCADE,
            FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
        );
        
        ALTER TABLE users ADD COLUMN device_id TEXT DEFAULT NULL;
        
        -- Device login approvals
        CREATE TABLE IF NOT EXISTS device_login_requests (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            device_id TEXT NOT NULL,
            device_info TEXT,          -- browser/OS info
            status TEXT DEFAULT 'pending',  -- pending/approved/rejected
            requested_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            resolved_at TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );

        PRAGMA foreign_keys = ON;
    """)
    conn.commit()

def truncate_tables(conn):
    """Drop all data from tables."""
    cursor = conn.cursor()
    cursor.execute("PRAGMA foreign_keys = OFF")
    tables = [
        'password_resets', 'contact_messages', 'inquiry_items', 'inquiries',
        'product_meta', 'product_colors', 'product_sizes', 'product_variants',
        'product_images', 'products', 'catalogues', 'banners',
        'categories', 'brands', 'colors', 'sizes', 'users', 'settings',
    ]
    for table in tables:
        cursor.execute(f"DELETE FROM {table}")
    cursor.execute("PRAGMA foreign_keys = ON")
    conn.commit()

# ============================================================
# DATA SEED FUNCTIONS
# ============================================================

def seed_users(conn):
    print("👤 Seeding users...")
    cursor = conn.cursor()
    users = [
        ('Admin KicksHub', 'KicksHub Wholesale Pvt Ltd', 'admin@kickshub.in', '9876543210', 'admin123',
         '27ABCDE1234F1Z5', '123, Footwear Market, BKC Complex', 'Mumbai', 'Maharashtra', '400051', 'admin', 'approved'),
        ('Rajesh Kumar', 'Kicks Footwear Store', 'rajesh@kicksfootwear.in', '9876543211', 'dealer123',
         '07FGHI5678J2K6', '45, Shoe Market, Chandni Chowk', 'Delhi', 'Delhi', '110006', 'dealer', 'approved'),
        ('Priya Sharma', 'Stepso Footwear', 'priya@stepso.in', '9876543212', 'dealer123',
         '27JKLM9012N3P7', '78, Fashion Street, Colaba', 'Mumbai', 'Mumbai', '400005', 'dealer', 'approved'),
        ('Amit Patel', 'Hommy Spot', 'amit@hammyspot.in', '9876543213', 'dealer123',
         '24QRST3456U7V8', '12, CG Road', 'Ahmedabad', 'Gujarat', '380009', 'dealer', 'approved'),
        ('Sneha Reddy', 'Reddy Footwear World', 'sneha@reddyfw.in', '9876543214', 'dealer123',
         '36WXYZ7890A1B2', '56, RB Road, Secunderabad', 'Hyderabad', 'Telangana', '500003', 'dealer', 'approved'),
        ('Vikram Singh', 'Singh Shoes & Sons', 'vikram@singhshoes.in', '9876543215', 'dealer123',
         '09CDEF3456G7H8', '23, MI Road, Jaipur', 'Jaipur', 'Rajasthan', '302001', 'dealer', 'approved'),
        ('Ananya Gupta', 'Gupta Footwear Bazaar', 'ananya@guptafw.in', '9876543216', 'dealer123',
         '09IJKL7890M1N2', '89, Nai Sarak', 'Lucknow', 'Uttar Pradesh', '226001', 'dealer', 'pending'),
        ('Rahul Verma', 'Verma Shoe Palace', 'rahul@vermasp.in', '9876543217', 'dealer123',
         '', '34, MG Road, Camp', 'Pune', 'Maharashtra', '411001', 'dealer', 'approved'),
        ('Deepika Joshi', 'Joshi Footwear Hub', 'deepika@joshifh.in', '9876543218', 'dealer123',
         '29OPQR1234S5T6', '67, Commercial Street', 'Bengaluru', 'Karnataka', '560001', 'dealer', 'approved'),
        ('Arjun Nair', 'Nair Trading Co', 'arjun@nairtrading.in', '9876543219', 'dealer123',
         '32UVWX5678Y9Z0', '12, Jew Town', 'Kochi', 'Kerala', '682002', 'dealer', 'pending'),
        ('Meera Desai', 'Desai Footwear Mart', 'meera@desaifm.in', '9876543220', 'dealer123',
         '', '78, Law Garden', 'Ahmedabad', 'Gujarat', '380006', 'dealer', 'approved'),
        ('Karan Malhotra', 'Malhotra Shoe Company', 'karan@malhotrashoe.in', '9876543221', 'dealer123',
         '03ABCD9012E3F4', '56, Sector 17', 'Chandigarh', 'Chandigarh', '160017', 'dealer', 'blocked'),
        ('Ishita Bose', 'Bose Footwear Emporium', 'ishita@bosefe.in', '9876543222', 'dealer123',
         '19WXYZ3456A7B8', '90, Park Street', 'Kolkata', 'West Bengal', '700016', 'dealer', 'pending'),
        ('Ravi Shankar', 'Shankar Wholesale Shoes', 'ravi@shankarws.in', '9876543223', 'dealer123',
         '33CDEF7890G1H2', '45, Ranganathan Street', 'Chennai', 'Tamil Nadu', '600001', 'dealer', 'approved'),
        ('Pooja Agarwal', 'Agarwal Footwear Junction', 'pooja@agarwalfj.in', '9876543224', 'dealer123',
         '23IJKL1234M5N6', '22, Ashok Marg', 'Indore', 'Madhya Pradesh', '452001', 'dealer', 'approved'),
    ]
    for name, biz, email, phone, pw, gst, addr, city, state, pin, role, status in users:
        pw_hash = generate_password_hash(pw)
        created_at = (datetime.now() - timedelta(days=random.randint(0, 180))).isoformat()
        cursor.execute("""
            INSERT INTO users (full_name, business_name, email, phone, password_hash, gst_number,
                               address, city, state, pincode, role, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, biz, email, phone, pw_hash, gst, addr, city, state, pin, role, status, created_at))
    conn.commit()
    print(f"✅ {len(users)} users seeded")

def seed_categories(conn):
    print("📂 Seeding categories...")
    cursor = conn.cursor()

    # cat_type: 'cat1' = deal/collection type, 'cat2' = gender/age, 'cat3' = material/product type
    categories = [
        # CAT 1 — Deal / Collection Type
        ('New Arrivals',  'new-arrivals',  '🆕', 'Latest products added',              'cat1', 1),
        ('Offer',         'offer',         '🔥', 'Special deals and discounts',         'cat1', 2),
        ('Imported',      'imported',      '🌍', 'International brand footwear',        'cat1', 3),
        ('Branded',       'branded',       '⭐', 'Top Indian brand footwear',           'cat1', 4),
        ('Non Branded',   'non-branded',   '📦', 'Affordable quality footwear',         'cat1', 5),
        ('School',        'school',        '🏫', 'School footwear collection',          'cat1', 6),

        # CAT 2 — Gender / Age group
        ('Mens',          'mens',          '👔', 'Footwear for men',                    'cat2', 1),
        ('Womens',        'womens',        '👠', 'Footwear for women',                  'cat2', 2),
        ('Kids',          'kids',          '👶', 'Footwear for children',               'cat2', 3),

        # CAT 3 — Material / Product Type
        ('EVA',           'eva',           '🩴', 'Lightweight EVA slippers & sandals',  'cat3', 1),
        ('PU',            'pu',            '👟', 'Premium PU material shoes',           'cat3', 2),
        ('Hawai',         'hawai',         '🌴', 'Classic Hawai chappals',              'cat3', 3),
        ('Shoes',         'shoes',         '👞', 'General shoes category',              'cat3', 4),
        ('Socks',         'socks',         '🧦', 'Socks for all ages',                  'cat3', 5),
        ('Accessories',   'accessories',   '🎒', 'Shoe care and accessories',           'cat3', 6),
    ]

    for name, slug, icon, desc, cat_type, sort in categories:
        cursor.execute("""
            INSERT INTO categories (name, slug, icon, description, cat_type, sort_order, is_active)
            VALUES (?, ?, ?, ?, ?, ?, 1)
        """, (name, slug, icon, desc, cat_type, sort))

    conn.commit()
    print(f"✅ {len(categories)} categories seeded (cat1: 6, cat2: 3, cat3: 6)")

def seed_brands(conn):
    print("🏷️  Seeding brands...")
    cursor = conn.cursor()
    brands = [
        ('KicksHub Premium', 'kickshub-premium', 'Premium in-house brand'),
        ('KicksHub Value', 'kickshub-value', 'Affordable quality range'),
        ('Bata India', 'bata', 'Iconic Indian footwear brand'),
        ('Paragon', 'paragon', 'Popular casual footwear brand'),
        ('Relaxo', 'relaxo', 'Comfort footwear specialist'),
        ('Liberty', 'liberty', 'Trusted formal footwear brand'),
        ("Khadim's", 'khadims', 'Popular everyday footwear'),
        ('Action', 'action', 'Sports and casual footwear'),
        ('Lancer', 'lancer', 'School shoes specialist'),
        ('Adidas (Import)', 'adidas-import', 'Premium imported sports brand'),
        ('Nike (Import)', 'nike-import', 'Premium imported sports brand'),
        ('Puma (Import)', 'puma-import', 'Premium imported lifestyle brand'),
    ]
    for name, slug, desc in brands:
        cursor.execute("INSERT INTO brands (name, slug, description, is_active) VALUES (?, ?, ?, 1)", (name, slug, desc))
    conn.commit()
    print(f"✅ {len(brands)} brands seeded")

def seed_colors(conn):
    print("🎨 Seeding colors...")
    cursor = conn.cursor()
    colors = [
        ('Black', '#000000'), ('White', '#FFFFFF'), ('Brown', '#8B4513'),
        ('Blue', '#0000FF'), ('Red', '#FF0000'), ('Green', '#008000'),
        ('Grey', '#808080'), ('Navy', '#000080'), ('Pink', '#FFC0CB'),
        ('Purple', '#800080'), ('Maroon', '#800000'), ('Beige', '#F5F5DC'),
        ('Tan', '#D2B48C'), ('Olive', '#808000'), ('Teal', '#008080'),
        ('Coral', '#FF7F50'), ('Mustard', '#FFDB58'), ('Burgundy', '#800020'),
        ('Charcoal', '#36454F'), ('Cream', '#FFFDD0'), ('Khaki', '#C3B091'),
        ('Sky Blue', '#87CEEB'), ('Peach', '#FFDAB9'), ('Mint', '#98FB98'),
    ]
    for name, hex_code in colors:
        cursor.execute("INSERT INTO colors (name, hex_code) VALUES (?, ?)", (name, hex_code))
    conn.commit()
    print(f"✅ {len(colors)} colors seeded")

def seed_sizes(conn):
    print("📏 Seeding sizes...")
    cursor = conn.cursor()
    sizes = [
        (1, 'kids', 1), (2, 'kids', 2), (3, 'kids', 3), (4, 'kids', 4), (5, 'kids', 5),
        (6, 'general', 6), (7, 'general', 7), (8, 'general', 8), (9, 'general', 9),
        (10, 'general', 10), (11, 'general', 11), (12, 'general', 12), (13, 'general', 13),
        (14, 'general', 14),
        ('S', 'socks', 1), ('M', 'socks', 2), ('L', 'socks', 3), ('XL', 'socks', 4),
        ('XXL', 'socks', 5),
        ('One Size', 'general', 0),
        (3, 'women', 1), (4, 'women', 2), (5, 'women', 3), (6, 'women', 4),
        (7, 'women', 5), (8, 'women', 6), (9, 'women', 7),
    ]
    for name, cat_type, sort in sizes:
        cursor.execute("INSERT INTO sizes (name, category_type, sort_order) VALUES (?, ?, ?)", (str(name), cat_type, sort))
    conn.commit()
    print(f"✅ {len(sizes)} sizes seeded")

# ─── PRODUCT DEFINITIONS ─────────────────────────────────────────────────

PRODUCT_DEFS = [
    # (cat_id, name, desc, price, compare, brand_id, colors_list, sizes_list, stock, moq, disc, featured)
    
    # SCHOOL SHOES
    (1, 'Premium School Shoe - Black', 'High-quality school shoe in premium black leather. Durable sole, reinforced stitching, comfortable insole.',
     450, 599, 1, [1, 2], [6,7,8,9,10,11,12], 500, 10, 25, 1),
    (1, 'School Oxford Shoe - White', 'Classic white school oxford made from premium synthetic leather. Lightweight, breathable.',
     425, 575, 1, [2], [6,7,8,9,10,11], 350, 10, 26, 1),
    (1, 'Junior School Sneakers', 'Comfortable sneakers for junior students. Soft cushion, breathable mesh, velcro closure.',
     380, 499, 2, [1,4,2], [5,6,7,8,9], 400, 10, 24, 0),
    (1, 'School Formal Shoes - Brown', 'Premium brown formal school shoes with durable leather finish. Anti-skid sole.',
     475, 649, 1, [3,1], [7,8,9,10,11,12], 250, 10, 27, 0),
    (1, 'School Loafers - Navy Blue', 'Smart navy blue loafers with slip-on design. Premium synthetic upper.',
     400, 549, 8, [8,1], [6,7,8,9,10], 200, 10, 25, 0),
    (1, 'School Sports Shoes - White/Blue', 'Multi-purpose sports shoes for PT and daily wear. Lightweight EVA sole.',
     520, 699, 2, [2,4], [6,7,8,9,10,11], 300, 10, 26, 0),

    # MEN'S
    (2, "Men's Formal Derby - Black", 'Premium black derby shoes. Genuine leather, classic design.',
     1299, 1799, 6, [1], [7,8,9,10,11,12], 200, 6, 28, 1),
    (2, "Men's Casual Loafers - Brown", 'Stylish brown casual loafers. Premium synthetic leather, cushioned insole.',
     899, 1299, 4, [3,1,12], [7,8,9,10,11], 300, 6, 30, 1),
    (2, "Men's Sports Running Shoes", 'High-performance running shoes. Breathable mesh, shock-absorbing sole.',
     1499, 1999, 1, [1,4,5], [7,8,9,10,11,12], 250, 6, 25, 1),
    (2, "Men's Sneakers - White", 'Trendy white sneakers. Padded collar, rubber outsole.',
     1099, 1499, 1, [2,1,7], [7,8,9,10,11], 400, 6, 27, 1),
    (2, "Men's Leather Boots - Brown", 'Rugged brown leather boots. Premium leather, sturdy sole.',
     1899, 2499, 3, [3,1], [8,9,10,11,12], 150, 6, 24, 0),
    (2, "Men's Formal Oxford - Black Patent", 'Premium black patent leather oxford. High-gloss finish.',
     1599, 2199, 6, [1], [8,9,10,11], 120, 6, 27, 0),

    # WOMEN'S
    (3, "Women's Heeled Sandals - Black", 'Elegant black heeled sandals. Block heel, adjustable strap.',
     899, 1299, 1, [1,19], [5,6,7,8,9], 250, 6, 30, 1),
    (3, "Women's Casual Flats - Ballet", 'Comfortable ballet flats. Soft upper, padded insole.',
     599, 849, 1, [1,2,10,5], [5,6,7,8,9], 400, 6, 29, 1),
    (3, "Women's Sneakers - White", 'Chunky sole white sneakers. Padded collar, breathable.',
     1099, 1499, 1, [2,20,21], [5,6,7,8,9,10], 300, 6, 25, 1),
    (3, "Women's Party Heels - Gold", 'Stunning gold party heels. Embellished design.',
     1299, 1799, 1, [22,1,2], [5,6,7,8,9], 150, 6, 28, 0),
    (3, "Women's Wedge Sandals - Beige", 'Comfortable wedge sandals. Braided detail, EVA sole.',
     799, 1099, 5, [12,3], [5,6,7,8,9], 280, 6, 27, 0),
    (3, "Women's Ankle Boots", 'Stylish ankle boots. Side zipper, block heel.',
     1499, 1999, 1, [1,3,19], [6,7,8,9,10], 180, 6, 25, 0),

    # KIDS
    (4, "Kids' Running Shoes - Blue", 'Fun blue running shoes. Lightweight, flexible sole.',
     599, 849, 2, [4,1,5], [1,2,3,4,5,6], 350, 12, 25, 1),
    (4, "Baby Soft Sole - First Walkers", 'Soft sole shoes for babies. Cotton upper, suede sole.',
     349, 499, 1, [2,9,22], [1,2,3], 400, 12, 20, 1),
    (4, "Kids' Casual Sneakers", 'Colorful sneakers with fun designs. Velcro straps.',
     499, 699, 2, [4,5,2,1], [2,3,4,5,6], 450, 12, 22, 1),
    (4, "Kids' Sandals", 'Durable sandals. Adjustable straps, protective toe cap.',
     399, 549, 4, [4,5,7], [2,3,4,5,6], 300, 12, 24, 0),
    (4, "Kids' Party Shoes - Formal", 'Smart formal shoes for special occasions. Patent finish.',
     699, 949, 6, [1,2], [3,4,5,6], 200, 12, 25, 0),
    (4, "Kids' Rain Boots", 'Waterproof boots. Warm lining, non-slip sole.',
     799, 1099, 1, [5,4,1], [3,4,5,6,7], 150, 12, 22, 0),

    # SOCKS
    (5, 'Ankle Socks - Cotton Pack of 6', 'Breathable cotton ankle socks. Reinforced heel/toe.',
     199, 299, 1, [1,2,7,4], [17,18,19,20], 1000, 24, 33, 1),
    (5, 'Crew Socks - Formal Black Pack of 3', 'Premium formal crew socks. Cotton blend.',
     249, 349, 1, [1,19], [18,19,20], 800, 24, 30, 1),
    (5, 'Knee High Socks - School White Pack of 3', 'School knee-high socks. Durable cotton-polyester.',
     299, 399, 1, [2], [1,2,3,4,5,6,17,18,19], 600, 24, 28, 1),
    (5, 'No-Show Socks - Invisible Pack of 5', 'Invisible socks with silicone heel grip.',
     249, 349, 1, [1,2,4,7], [17,18,19,20], 700, 24, 29, 0),
    (5, 'Sports Socks - Cushioned Pack of 3', 'Performance sports socks. Moisture-wicking.',
     349, 499, 1, [2,1,4], [18,19,20,21], 500, 24, 30, 0),
    (5, 'Wool Winter Socks - Pack of 2', 'Warm wool blend winter socks. Thermal.',
     399, 549, 1, [1,7,3], [18,19,20], 300, 12, 25, 0),

    # ACCESSORIES
    (6, 'Shoe Polish Kit - Complete Care', 'Complete kit with black, brown, neutral polish.',
     199, 299, 1, [17], [21], 500, 12, 20, 1),
    (6, 'Shoe Laces Premium Pack - 6 Pairs', 'Premium laces. Assorted colors. 120cm.',
     99, 149, 1, [1,2,3,8], [21], 1000, 24, 34, 1),
    (6, 'Memory Foam Insoles - Comfort Plus', 'Premium memory foam. Shock-absorbing, arch support.',
     299, 449, 1, [1,2], [17,18,19,20], 600, 12, 25, 1),
    (6, 'Shoe Deodorizer Spray - 200ml', 'Eliminates odor-causing bacteria.',
     149, 199, 1, [17], [21], 400, 12, 25, 0),
    (6, 'Shoe Bags - Travel Pack of 3', 'Waterproof nylon shoe bags. Drawstring closure.',
     249, 349, 1, [1,4,7], [21], 350, 12, 28, 0),

    # EVA
    (7, 'EVA Slides - Classic Black', 'Ultra-lightweight, waterproof. Cushioned footbed.',
     249, 399, 1, [1,4,5], [6,7,8,9,10,11,12,13], 800, 12, 35, 1),
    (7, 'EVA Sandals - Comfort Fit', 'Lightweight, flexible, waterproof. Adjustable strap.',
     299, 449, 2, [1,2,4,9], [7,8,9,10,11,12], 600, 12, 32, 1),
    (7, 'Premium EVA Flip Flops', 'Soft cushioned sole, durable strap. Multiple colors.',
     199, 299, 1, [1,2,4,5,8], [7,8,9,10,11,12,13], 900, 12, 40, 1),
    (7, 'EVA Bathroom Slippers - Anti-Skid', 'Drainage holes, quick-drying, mold-resistant.',
     179, 249, 2, [1,2,22,9], [7,8,9,10,11], 1000, 12, 38, 0),
    (7, 'Memory Foam EVA Slides - Luxury', 'Memory foam footbed. Thick cushioned sole.',
     449, 649, 1, [1,2,7,8], [7,8,9,10,11,12], 400, 12, 25, 0),

    # PU
    (8, 'PU Formal Shoes - Black', 'Professional black PU formal shoes. Padded insole.',
     799, 1099, 1, [1], [7,8,9,10,11,12], 400, 6, 28, 1),
    (8, 'PU Loafers - Brown', 'Stylish brown PU loafers. Tassel detail, slip-on.',
     699, 949, 2, [3,1], [7,8,9,10,11], 350, 6, 27, 1),
    (8, 'PU Sneakers - White', 'Trendy white PU sneakers. Perforations, breathable.',
     599, 849, 1, [2,1,4], [7,8,9,10,11,12], 500, 6, 30, 1),
    (8, "Women's PU Sandals", 'Adjustable strap, cushioned footbed, lightweight.',
     449, 649, 1, [1,2,12,9], [5,6,7,8,9], 450, 6, 29, 0),
    (8, 'PU Ankle Boots', 'Side zipper, faux leather, block heel.',
     999, 1399, 1, [1,3,19], [7,8,9,10,11], 200, 6, 25, 0),

    # HAWAI
    (9, 'Classic Hawai Chappal - Black', 'Original classic. Durable rubber, iconic design.',
     149, 199, 4, [1,2], [7,8,9,10,11,12,13], 2000, 24, 40, 1),
    (9, 'Premium Hawai - Cushioned', 'Extra cushioned footbed. Durable rubber sole.',
     199, 299, 4, [1,2,4,5,8], [7,8,9,10,11,12,13], 1500, 24, 35, 1),
    (9, 'Designer Hawai Chappal', 'Printed straps, colorful patterns. Durable rubber.',
     249, 349, 1, [4,5,9,22], [7,8,9,10,11,12], 800, 24, 30, 0),
    (9, "Women's Slim Fit Hawai", 'Narrower strap, lighter weight. Feminine colors.',
     149, 199, 4, [9,5,2,1], [5,6,7,8,9], 1000, 24, 33, 0),
    (9, "Kids' Fun Hawai", 'Character prints, smaller sizes, softer rubber.',
     99, 149, 4, [5,4,9,22], [1,2,3,4,5,6], 1200, 24, 40, 0),

    # IMPORTED
    (10, 'Premium Running Shoes - Imported', 'Advanced cushioning. Lightweight mesh.',
     2499, 3499, 10, [1,4,5], [7,8,9,10,11,12], 100, 6, 20, 1),
    (10, 'Imported Lifestyle Sneakers', 'Premium materials, superior comfort.',
     1999, 2999, 12, [2,1,4,5], [7,8,9,10,11], 120, 6, 18, 1),
    (10, 'Imported Leather Boots', 'Full-grain leather, Goodyear welt. Premium.',
     3999, 5499, 11, [3,1], [8,9,10,11,12], 50, 6, 15, 1),
    (10, 'Imported Training Shoes', 'Professional gym training. Excellent grip.',
     2199, 2999, 11, [1,4,5,7], [7,8,9,10,11,12], 80, 6, 17, 0),
    (10, 'Imported Casual Slip-Ons', 'Elastic panels, memory foam insole.',
     1799, 2499, 12, [1,2,8], [7,8,9,10,11], 90, 6, 16, 0),

    # BRANDED
    (11, 'Campus Sneakers - Original', 'Original Campus. Authorized distributor.',
     899, 1299, 2, [2,1,4], [7,8,9,10,11], 300, 6, 22, 1),
    (11, 'Bata Formal Shoes - Premium', 'Genuine Bata. Quality guarantee.',
     1399, 1899, 3, [1,3], [7,8,9,10,11,12], 200, 6, 20, 1),
    (11, 'Paragon Hawaii - Original', 'Original Paragon. Iconic quality.',
     199, 299, 4, [1,2,4,5], [7,8,9,10,11,12,13], 2000, 24, 30, 1),
    (11, 'Relaxo Slippers - Comfort Plus', 'Memory foam footbed. Best-selling.',
     349, 499, 5, [1,2,4], [7,8,9,10,11,12], 600, 12, 25, 0),
    (11, 'Action Sports Shoes', 'Breathable mesh, cushioned sole.',
     799, 1099, 8, [2,4,5], [7,8,9,10,11], 350, 6, 24, 0),

    # NON-BRANDED
    (12, 'Economy Casual Shoes', 'Affordable daily wear. Durable construction.',
     349, 499, 1, [1,4,7], [7,8,9,10,11], 600, 12, 30, 1),
    (12, 'Bulk Economy Slippers', 'Mass market slippers. Super affordable.',
     99, 149, 2, [1,4,5], [7,8,9,10,11], 2000, 24, 40, 1),
    (12, 'Budget School Shoes', 'Price-sensitive option. Basic quality.',
     299, 399, 2, [1,2], [6,7,8,9,10,11], 800, 12, 28, 0),
    (12, 'Mass Market Chappal', 'High-volume wholesale chappal. MOQ 50.',
     79, 129, 2, [1,2], [7,8,9,10,11,12,13], 5000, 50, 45, 0),
    (12, 'Economy Canvas Shoes', 'Budget canvas. Popular in rural markets.',
     249, 349, 1, [1,4,7,8], [7,8,9,10,11], 700, 12, 32, 0),
]

def seed_products(conn):
    print("👟 Seeding products with variants...")
    cursor = conn.cursor()
    
    # Get IDs
    cursor.execute("SELECT id, name FROM colors")
    db_colors = {row['name'].lower(): row['id'] for row in cursor.fetchall()}

    cursor.execute("SELECT id, name FROM sizes")
    db_sizes = {str(row['name']): row['id'] for row in cursor.fetchall()}
    
    inserted = 0
    for i, (cat_id, name, desc, price, compare, brand_id, color_ids, size_ids, stock, moq, disc, featured) in enumerate(PRODUCT_DEFS):
        slug = name.lower().replace(' ', '-').replace("'", '').replace('"', '')
        slug = ''.join(c for c in slug if c.isalnum() or c == '-')
        sku = f"PRD-{str(i+1).zfill(4)}"
        
        cursor.execute("""
            INSERT INTO products (name, description, sku, slug, product_number, category_id, brand_id,
                                  price, compare_price, stock, moq, discount, is_featured, is_active, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?)
        """, (name, desc, sku, slug, 1000 + (i + 1), cat_id, brand_id, price, compare, stock, moq, disc, featured,
              (datetime.now() - timedelta(days=random.randint(0, 120))).isoformat()))
        product_id = cursor.lastrowid

        # ── IMAGES: randomly pick 2–4 images from 1.jpeg to 21.jpeg ──────
        num_images = random.randint(2, 4)
        for img_idx in range(num_images):
            image_num = ((i * 10) + img_idx) % 21 + 1
            image_path = f"images/{image_num}.jpeg"



            cursor.execute("""
                INSERT INTO product_images (product_id, image_path, is_primary, sort_order)
                VALUES (?, ?, ?, ?)
            """, (
                product_id,
                image_path,
                1 if img_idx == 0 else 0,
                img_idx
            ))

        # ─────────────────────────────────────────────────────────────────

        # Colors
        for cid in color_ids:
            if cid in db_colors.values():
                cursor.execute("INSERT OR IGNORE INTO product_colors (product_id, color_id) VALUES (?, ?)", (product_id, cid))
        
        # Sizes
        for sid in size_ids:
            s_str = str(sid)
            if s_str in db_sizes:
                cursor.execute("INSERT OR IGNORE INTO product_sizes (product_id, size_id) VALUES (?, ?)", (product_id, db_sizes[s_str]))
        
        # Variants
        vi = 0
        for cid in color_ids:
            if cid in db_colors.values():
                for sid in size_ids:
                    s_str = str(sid)
                    if s_str in db_sizes:
                        vi += 1
                        vprice = max(0, price + random.choice([0, 0, 20, 30, -20, -10]))
                        vstock = max(0, stock + random.randint(-50, 50))
                        cursor.execute("""
                            INSERT INTO product_variants (product_id, color_id, size_id, price, stock, sku, is_active)
                            VALUES (?, ?, ?, ?, ?, ?, 1)
                        """, (product_id, cid, db_sizes[s_str], vprice, vstock, f"{sku}-V{vi}"))
        
        # Category-specific meta
        if cat_id == 1:
            cursor.execute("INSERT INTO product_meta (product_id, meta_key, meta_value) VALUES (?, 'school_type', ?)",
                          (product_id, random.choice(['CBSE', 'ICSE', 'State Board', 'All'])))
            cursor.execute("INSERT INTO product_meta (product_id, meta_key, meta_value) VALUES (?, 'lace_type', ?)",
                          (product_id, random.choice(['Lace', 'Velcro', 'Both', 'Slip-on'])))
        elif cat_id == 5:
            cursor.execute("INSERT INTO product_meta (product_id, meta_key, meta_value) VALUES (?, 'material', ?)",
                          (product_id, random.choice(['Cotton', 'Cotton Blend', 'Polyester', 'Wool'])))
            cursor.execute("INSERT INTO product_meta (product_id, meta_key, meta_value) VALUES (?, 'pair_count', ?)",
                          (product_id, str(random.randint(3, 6))))
        elif cat_id in (7, 9):
            cursor.execute("INSERT INTO product_meta (product_id, meta_key, meta_value) VALUES (?, 'sole_type', ?)",
                          (product_id, 'EVA' if cat_id == 7 else 'Rubber'))
            cursor.execute("INSERT INTO product_meta (product_id, meta_key, meta_value) VALUES (?, 'eva_type', ?)",
                          (product_id, random.choice(['Standard', 'Premium', 'Memory Foam'])))
        # ── Link product to categories (cat1 + cat2/cat3 based on product type) ──
        # cat_id is already the primary category — link it
        cursor.execute("SELECT cat_type FROM categories WHERE id = ?", (cat_id,))
        cat_row = cursor.fetchone()
        if cat_row:
            cursor.execute("""
                INSERT OR IGNORE INTO product_categories (product_id, category_id, cat_type)
                VALUES (?, ?, ?)
            """, (product_id, cat_id, cat_row['cat_type'] if isinstance(cat_row, dict) else cat_row[0]))
            
        inserted += 1
        if inserted % 20 == 0:
            print(f"   ... {inserted}/{len(PRODUCT_DEFS)} products")
    
    conn.commit()
    print(f"✅ {inserted} products with images, colors, sizes, variants")

def seed_inquiries(conn):
    print("📋 Seeding inquiries...")
    cursor = conn.cursor()
    
    cursor.execute("SELECT id, full_name, business_name, phone, address, city, state, pincode, gst_number FROM users WHERE role='dealer' AND status='approved'")
    dealers = cursor.fetchall()
    cursor.execute("SELECT id, name, price FROM products WHERE is_active=1 LIMIT 30")
    products = cursor.fetchall()
    
    statuses = ['new', 'contacted', 'negotiation', 'confirmed', 'closed']
    weights = [3, 2, 2, 1.5, 1.5]
    
    notes_list = [
        'Need this urgently for school season. Please confirm availability.',
        'Looking for bulk pricing. Need 50 pairs to start.',
        'Please send sample before bulk order.',
        'Regular monthly order. Same pricing as last time.',
        'New customer inquiry. Interested in becoming regular dealer.',
        'Need mixed sizes. Confirm size-wise stock.',
        'School tender requirement. Need certificates.',
        'Festival season stock. Need delivery before Diwali.',
        'First time ordering. Need guidance.',
        'Urgent exhibition requirement. Need within 5 days.',
    ]
    
    for _ in range(25):
        d = random.choice(dealers)
        status = random.choices(statuses, weights=weights, k=1)[0]
        lat, lng = 19.0760 + random.uniform(-0.05, 0.05), 72.8777 + random.uniform(-0.05, 0.05)
        cr = (datetime.now() - timedelta(days=random.randint(0, 60))).isoformat()
        
        cursor.execute("""
            INSERT INTO inquiries (user_id, dealer_name, shop_name, phone, gst_number,
                                   address, city, state, pincode, latitude, longitude,
                                   notes, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            d['id'],
            d['full_name'],
            d['business_name'],
            d['phone'],
            d['gst_number'] or '',
            d['address'] or '',
            d['city'] or '',
            d['state'] or '',
            d['pincode'] or '',
            lat,
            lng,
            random.choice(notes_list) if random.random() > 0.3 else '',
            status,
            cr
        ))
        inq_id = cursor.lastrowid
        
        for item in random.sample(products, min(random.randint(1, 4), len(products))):
            cursor.execute("""
                INSERT INTO inquiry_items (inquiry_id, product_id, product_name, quantity, size, color, price)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                inq_id,
                item['id'],
                item['name'],
                random.choice([10, 20, 25, 30, 50, 100, 200]),
                random.choice(['7', '8', '9', '10']),
                random.choice(['Black', 'White', 'Brown', 'Blue']),
                item['price']
            ))
    
    conn.commit()
    print(f"✅ 25 inquiries seeded")

def seed_banners(conn):
    print("🖼️  Seeding banners...")
    cursor = conn.cursor()
    banners = [
        ('School Shoe Mega Sale', 'Up to 40% off on bulk orders!', '/category/school-shoes', 'offer', 1),
        ("New Arrivals - Men's Collection", 'Latest formal and casual range', '/category/mens', 'home', 2),
        ('Festival Special Offer', 'Diwali bulk discounts on all categories!', '/products', 'festival', 3),
        ('Winter Collection Launch', 'Boots, woolen socks & winter footwear', '/category/boots', 'seasonal', 4),
        ('Become a Dealer Today', 'Join 500+ dealers across India!', '/register', 'home', 5),
        ('Kids Collection 2024', 'New designs, same great prices', '/category/kids', 'home', 6),
        ('Clearance Sale', 'Last season stock at factory price!', '/products?sort=price_asc', 'offer', 7),
    ]
    for title, sub, link, btype, sort in banners:
        cursor.execute("INSERT INTO banners (title, subtitle, image_path, link_url, type, sort_order, is_active) VALUES (?, ?, ?, ?, ?, ?, 1)",
                       (title, sub, f'banners/{title.lower().replace(" ","_")}.jpg', link, btype, sort))
    conn.commit()
    print(f"✅ {len(banners)} banners seeded")

def seed_catalogues(conn):
    print("📑 Seeding catalogues...")
    cursor = conn.cursor()
    catalogues = [
        ('KicksHub Catalog 2024', 'Complete catalog all categories', 1),
        ('School Shoes Collection', 'Complete school range', 1),
        ("Men's Footwear Range", 'Formal, casual, sports for men', 2),
        ("Women's Collection", 'Heels, flats, sneakers for women', 3),
        ('Kids & Baby Collection', 'Newborn to teens footwear', 4),
        ('EVA & Hawai Range', 'Slippers and sandals bulk catalog', 7),
        ('Socks & Accessories', 'Socks and shoe care catalog', 5),
    ]
    for title, desc, cat_id in catalogues:
        cursor.execute("INSERT INTO catalogues (title, description, category_id, pdf_path, cover_image, is_active) VALUES (?, ?, ?, ?, ?, 1)",
                       (title, desc, cat_id, f'catalogues/{title.lower().replace(" ","_")}.pdf', None))
    conn.commit()
    print(f"✅ {len(catalogues)} catalogues seeded")

def seed_settings(conn):
    print("⚙️  Seeding settings...")
    cursor = conn.cursor()
    settings = [
        ('site_name', 'KicksHub Wholesale'),
        ('site_email', 'info@kickshub.in'),
        ('site_phone', '+91 98765 43210'),
        ('site_whatsapp', '919876543210'),
        ('site_address', '123, Footwear Market, BKC Complex, Mumbai - 400051'),
        ('gst_number', '27ABCDE1234F1Z5'),
        ('delivery_charges', '0'),
        ('free_delivery_min', '5000'),
        ('currency', 'INR'),
        ('admin_email', 'admin@kickshub.in'),
    ]
    for key, val in settings:
        cursor.execute("INSERT OR IGNORE INTO settings (setting_key, setting_value) VALUES (?, ?)", (key, val))
    conn.commit()
    print(f"✅ {len(settings)} settings seeded")


# ─── MAIN ─────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='KicksHub SQLite Seed Script')
    parser.add_argument('--force', action='store_true', help='Delete and reseed all data')
    args = parser.parse_args()
    
    if args.force:
        if os.path.exists(DB_PATH):
            os.remove(DB_PATH)
            print("🗑️  Deleted existing database file")
    
    conn = get_conn()
    conn.row_factory = dict_factory
    
    print(f"\n{'='*55}")
    print(f"   🌟 KicksHub SQLite Database Seeder")
    print(f"   📁 DB: {DB_PATH}")
    print(f"{'='*55}\n")
    
    # Create tables
    create_tables(conn)
    print("✅ Tables created/verified")
    
    # Seed data
    seed_categories(conn)
    seed_brands(conn)
    seed_colors(conn)
    seed_sizes(conn)
    seed_users(conn)
    seed_products(conn)
    seed_inquiries(conn)
    seed_banners(conn)
    seed_catalogues(conn)
    seed_settings(conn)
    
    # Summary
    cursor = conn.cursor()
    tables = ['users', 'categories', 'brands', 'colors', 'sizes', 'products',
              'product_images', 'product_variants', 'product_colors', 'product_sizes',
              'inquiries', 'inquiry_items', 'banners', 'catalogues', 'contact_messages', 'settings']
    print(f"\n{'='*55}")
    print(f"   ✅ Seeding Complete!")
    print(f"{'='*55}")
    print(f"\n📊 Summary:")
    for table in tables:
        cursor.execute(f"SELECT COUNT(*) as cnt FROM {table}")
        try:
            count = cursor.fetchone()
            if isinstance(count, dict):
                count = count['cnt']
            elif isinstance(count, (list, tuple)):
                count = count[0]
            else:
                count = count
            print(f"   {table}: {count}")
        except:
            pass
    
    print(f"\n🔑 Admin Login:")
    print(f"   Email:    admin@kickshub.in")
    print(f"   Password: admin123")
    print(f"\n🔑 Dealer Login:")
    print(f"   Email:    rajesh@kicksfootwear.in / priya@stepso.in / amit@hammyspot.in")
    print(f"   Password: dealer123")
    print(f"\n📁 Database file: {DB_PATH}")
    print(f"\n🎉 Now run 'npm run dev' to start the frontend!\n")
    
    conn.close()

if __name__ == '__main__':
    main()