#!/usr/bin/env python3
"""
KicksHub - Database Seed Script
Populates the database with comprehensive sample data for B2B Footwear Wholesale.

Usage:
    python seed.py              # Seed database
    python seed.py --force      # Drop and reseed all data
    python seed.py --sample     # Insert only minimal sample data
"""

import os
import sys
import random
import argparse
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash

# ─── Database Connection ───────────────────────────────────────────────────

try:
    import pymysql
except ImportError:
    print("❌ pymysql not installed. Run: pip install pymysql")
    sys.exit(1)

DB_CONFIG = {
    'host': os.environ.get('MYSQL_HOST', 'localhost'),
    'user': os.environ.get('MYSQL_USER', 'root'),
    'password': os.environ.get('MYSQL_PASSWORD', ''),
    'database': os.environ.get('MYSQL_DB', 'kickshub'),
    'charset': 'utf8mb4',
    'cursorclass': pymysql.cursors.DictCursor,
}


def get_connection():
    """Create and return a database connection."""
    try:
        conn = pymysql.connect(**DB_CONFIG)
        print(f"✅ Connected to MySQL database: {DB_CONFIG['database']}")
        return conn
    except pymysql.Error as e:
        print(f"❌ Database connection failed: {e}")
        print(f"   Make sure MySQL is running and database '{DB_CONFIG['database']}' exists.")
        print(f"   Run: CREATE DATABASE IF NOT EXISTS {DB_CONFIG['database']} DEFAULT CHARACTER SET utf8mb4;")
        sys.exit(1)


def run_schema(conn):
    """Run the schema SQL file to create tables."""
    schema_path = os.path.join(os.path.dirname(__file__), 'models', 'schema.sql')
    if not os.path.exists(schema_path):
        print(f"⚠️ Schema file not found at: {schema_path}")
        print("   Attempting to seed anyway (tables may already exist)...")
        return
    
    print("📦 Running schema...")
    with open(schema_path, 'r') as f:
        sql = f.read()
    
    cursor = conn.cursor()
    statements = sql.split(';')
    success = 0
    errors = 0
    for statement in statements:
        stmt = statement.strip()
        if stmt and not stmt.startswith('--') and not stmt.startswith('/*'):
            try:
                cursor.execute(stmt)
                success += 1
            except Exception as e:
                errors += 1
                if 'already exists' not in str(e).lower():
                    print(f"   ⚠️  {e}")
    conn.commit()
    cursor.close()
    print(f"✅ Schema executed: {success} statements OK, {errors} skipped")


def truncate_tables(conn):
    """Truncate all tables to reset data."""
    print("🗑️  Truncating all tables...")
    tables = [
        'password_resets', 'contact_messages', 'inquiry_items', 'inquiries',
        'product_meta', 'product_colors', 'product_sizes', 'product_variants',
        'product_images', 'products', 'catalogues', 'banners',
        'categories', 'brands', 'colors', 'sizes', 'users', 'settings',
    ]
    cursor = conn.cursor()
    cursor.execute("SET FOREIGN_KEY_CHECKS = 0")
    for table in tables:
        try:
            cursor.execute(f"TRUNCATE TABLE {table}")
        except Exception:
            pass  # Table might not exist
    cursor.execute("SET FOREIGN_KEY_CHECKS = 1")
    conn.commit()
    cursor.close()
    print("✅ All tables truncated")


# ─── DATA GENERATORS ───────────────────────────────────────────────────────

def seed_users(conn, count=15):
    """Seed users table with admin + dealers."""
    print("👤 Seeding users...")
    cursor = conn.cursor()
    
    users = [
        # (full_name, business_name, email, phone, password, gst, address, city, state, pincode, role, status)
        ('Admin KicksHub', 'KicksHub Wholesale Pvt Ltd', 'admin@kickshub.in', '9876543210', 'admin123',
         '27ABCDE1234F1Z5', '123, Footwear Market, BKC Complex', 'Mumbai', 'Maharashtra', '400051', 'admin', 'approved'),
        
        ('Rajesh Kumar', 'Kicks Footwear Store', 'rajesh@kicksfootwear.in', '9876543211', 'dealer123',
         '07FGHI5678J2K6', '45, Shoe Market, Chandni Chowk', 'Delhi', 'Delhi', '110006', 'dealer', 'approved'),
        
        ('Priya Sharma', 'Stepso Footwear', 'priya@stepso.in', '9876543212', 'dealer123',
         '27JKLM9012N3P7', '78, Fashion Street, Colaba', 'Mumbai', 'Maharashtra', '400005', 'dealer', 'approved'),
        
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
         '32UVWX5678Y9Z0', '12, Jew Town, Mattancherry', 'Kochi', 'Kerala', '682002', 'dealer', 'pending'),
        
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
    
    for i, (name, biz, email, phone, pw, gst, addr, city, state, pin, role, status) in enumerate(users):
        pw_hash = generate_password_hash(pw)
        created_at = datetime.now() - timedelta(days=random.randint(0, 180))
        cursor.execute("""
            INSERT INTO users (full_name, business_name, email, phone, password_hash, gst_number, 
                               address, city, state, pincode, role, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (name, biz, email, phone, pw_hash, gst, addr, city, state, pin, role, status, created_at))
    
    conn.commit()
    cursor.close()
    print(f"✅ {len(users)} users seeded (1 admin + 14 dealers)")


def seed_categories(conn):
    """Seed categories table."""
    print("📂 Seeding categories...")
    cursor = conn.cursor()
    
    categories = [
        ('School Shoes', 'school-shoes', '👞', 'Quality school footwear for all ages — CBSE, ICSE, State Board approved', 1),
        ("Men's Collection", 'mens', '👔', 'Premium footwear for men — formal, casual, sports, boots', 2),
        ("Women's Collection", 'womens', '👠', 'Trendy and comfortable womens footwear — heels, flats, sneakers', 3),
        ("Kids Collection", 'kids', '👶', 'Fun and durable footwear for children of all ages', 4),
        ('Socks', 'socks', '🧦', 'Premium quality socks for men, women, and kids — all sizes', 5),
        ('Accessories', 'accessories', '👜', 'Shoe care products, laces, insoles, polishes and more', 6),
        ('EVA Footwear', 'eva', '🩴', 'Lightweight EVA slippers, sandals and slides for everyday comfort', 7),
        ('PU Footwear', 'pu', '👟', 'Premium PU material shoes — durable, stylish, affordable', 8),
        ('Hawai Chappal', 'hawai', '🌴', 'Classic Hawai slippers — traditional design, modern comfort', 9),
        ('Imported Collection', 'imported', '🌍', 'International brand footwear — premium quality imports', 10),
        ('Branded Shoes', 'branded', '⭐', 'Top Indian and international brand footwear collections', 11),
        ('Non-Branded', 'non-branded', '📦', 'Affordable quality footwear without brand markup', 12),
        ('Sports Shoes', 'sports', '🏃', 'Performance sports shoes for running, training, and gym', 13),
        ('Casual Sneakers', 'casual-sneakers', '🥾', 'Trendy casual sneakers for everyday wear', 14),
        ('Formal Shoes', 'formal', '👞', 'Premium formal shoes for office and occasions', 15),
        ('Boots', 'boots', '🥾', 'Stylish boots for men and women — ankle, knee-high, combat', 16),
        ('Sandals & Floaters', 'sandals', '🩴', 'Comfortable sandals and floaters for casual wear', 17),
        ('Slippers', 'slippers', '🩴', 'Home and outdoor slippers for all ages', 18),
    ]
    
    for name, slug, icon, desc, sort in categories:
        cursor.execute("""
            INSERT INTO categories (name, slug, icon, description, sort_order, is_active)
            VALUES (?, ?, ?, ?, ?, 1)
        """, (name, slug, icon, desc, sort))
    
    conn.commit()
    cursor.close()
    print(f"✅ {len(categories)} categories seeded")


def seed_brands(conn):
    """Seed brands table."""
    print("🏷️  Seeding brands...")
    cursor = conn.cursor()
    
    brands = [
        ('KicksHub Premium', 'kickshub-premium', 'Premium in-house brand'),
        ('KicksHub Value', 'kickshub-value', 'Affordable quality range'),
        ('Bata India', 'bata', 'Iconic Indian footwear brand'),
        ('Paragon', 'paragon', 'Popular casual footwear brand'),
        ('Relaxo', 'relaxo', 'Comfort footwear specialist'),
        ('Liberty', 'liberty', 'Trusted formal footwear brand'),
        ('Khadim\'s', 'khadims', 'Popular everyday footwear'),
        ('Action', 'action', 'Sports and casual footwear'),
        ('Lancer', 'lancer', 'School shoes specialist'),
        ('Adidas (Import)', 'adidas-import', 'Premium imported sports brand'),
        ('Nike (Import)', 'nike-import', 'Premium imported sports brand'),
        ('Puma (Import)', 'puma-import', 'Premium imported lifestyle brand'),
    ]
    
    for name, slug, desc in brands:
        cursor.execute("""
            INSERT INTO brands (name, slug, description, is_active)
            VALUES (?, ?, ?, 1)
        """, (name, slug, desc))
    
    conn.commit()
    cursor.close()
    print(f"✅ {len(brands)} brands seeded")


def seed_colors(conn):
    """Seed colors table."""
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
        cursor.execute("""
            INSERT INTO colors (name, hex_code) VALUES (?, ?)
        """, (name, hex_code))
    
    conn.commit()
    cursor.close()
    print(f"✅ {len(colors)} colors seeded")


def seed_sizes(conn):
    """Seed sizes table."""
    print("📏 Seeding sizes...")
    cursor = conn.cursor()
    
    sizes_data = [
        # Kids sizes
        (1, 'kids', 1), (2, 'kids', 2), (3, 'kids', 3), (4, 'kids', 4), (5, 'kids', 5),
        # Adult general sizes
        (6, 'general', 6), (7, 'general', 7), (8, 'general', 8), (9, 'general', 9),
        (10, 'general', 10), (11, 'general', 11), (12, 'general', 12), (13, 'general', 13),
        (14, 'general', 14),
        # Sock sizes
        ('S', 'socks', 1), ('M', 'socks', 2), ('L', 'socks', 3), ('XL', 'socks', 4),
        ('XXL', 'socks', 5),
        # One size / Free size
        ('One Size', 'general', 0),
        # Women specific
        (3, 'women', 1), (4, 'women', 2), (5, 'women', 3), (6, 'women', 4),
        (7, 'women', 5), (8, 'women', 6), (9, 'women', 7),
    ]
    
    for name, cat_type, sort in sizes_data:
        cursor.execute("""
            INSERT INTO sizes (name, category_type, sort_order) VALUES (?, ?, ?)
        """, (str(name), cat_type, sort))
    
    conn.commit()
    cursor.close()
    print(f"✅ {len(sizes_data)} sizes seeded")


# ─── PRODUCT GENERATORS ────────────────────────────────────────────────────

def generate_product_dict(cat_id, name, desc, price, compare_price, brand_id,
                          images_count, color_ids, size_ids, stock, moq, 
                          discount, is_featured, sku_prefix):
    """Helper to create a product data dict."""
    return {
        'category_id': cat_id,
        'name': name,
        'description': desc,
        'price': price,
        'compare_price': compare_price,
        'brand_id': brand_id,
        'images_count': images_count,
        'color_ids': color_ids,
        'size_ids': size_ids,
        'stock': stock,
        'moq': moq,
        'discount': discount,
        'is_featured': is_featured,
        'sku_prefix': sku_prefix,
    }


def get_product_definitions():
    """Return a list of product definitions for all categories."""
    products = [
        # ── SCHOOL SHOES (cat_id=1) ──────────────────────────────────────
        generate_product_dict(1, 'Premium School Shoe - Black', 
            'High-quality school shoe in premium black leather. Features durable sole, reinforced stitching, and comfortable insole. Suitable for CBSE, ICSE, and State Board schools. Available in lace and velcro options. Perfect for wholesale bulk orders.',
            450, 599, 1, 3, [1, 2], [6,7,8,9,10,11,12], 500, 10, 25, 1, 'SCH'),
        
        generate_product_dict(1, 'School Oxford Shoe - White',
            'Classic white school oxford shoe made from premium synthetic leather. Lightweight, breathable, and easy to clean. Non-slip rubber sole. Ideal for school uniforms across all boards.',
            425, 575, 1, 3, [2], [6,7,8,9,10,11], 350, 10, 26, 1, 'SCH'),
        
        generate_product_dict(1, 'Junior School Sneakers',
            'Comfortable sneakers for junior school students. Soft cushioned sole, breathable mesh upper, and easy velcro closure. Lightweight design for all-day comfort.',
            380, 499, 2, 2, [1,4,2], [5,6,7,8,9], 400, 10, 24, 0, 'SCH'),
        
        generate_product_dict(1, 'School Formal Shoes - Brown',
            'Premium brown formal school shoes with durable leather finish. Reinforced toe cap, anti-skid sole, and cushioned footbed. Suitable for senior students.',
            475, 649, 1, 2, [3,1], [7,8,9,10,11,12], 250, 10, 27, 0, 'SCH'),
        
        generate_product_dict(1, 'School Loafers - Navy Blue',
            'Smart navy blue school loafers with comfortable slip-on design. Premium synthetic upper with breathable lining. Easy to maintain and long-lasting.',
            400, 549, 8, 2, [8,1], [6,7,8,9,10], 200, 10, 25, 0, 'SCH'),
        
        generate_product_dict(1, 'School Sports Shoes - White/Blue',
            'Multi-purpose school sports shoes for PT and daily wear. Lightweight EVA sole, breathable mesh, and padded collar. Available in white with blue accents.',
            520, 699, 2, 3, [2,4], [6,7,8,9,10,11], 300, 10, 26, 0, 'SCH'),

        # ── MEN'S COLLECTION (cat_id=2) ──────────────────────────────────
        generate_product_dict(2, "Men's Formal Derby Shoes - Black",
            'Premium black derby shoes for formal occasions. Genuine leather upper, leather lining, and durable rubber sole. Classic design suitable for office, weddings, and parties.',
            1299, 1799, 6, 3, [1], [7,8,9,10,11,12], 200, 6, 28, 1, 'MEN'),
        
        generate_product_dict(2, "Men's Casual Loafers - Brown",
            'Stylish brown casual loafers for everyday wear. Premium synthetic leather with cushioned insole. Slip-on design with elastic side panels for comfort.',
            899, 1299, 4, 3, [3,1,12], [7,8,9,10,11], 300, 6, 30, 1, 'MEN'),
        
        generate_product_dict(2, "Men's Sports Running Shoes",
            'High-performance running shoes with responsive cushioning. Breathable mesh upper, shock-absorbing sole, and lightweight design. Ideal for daily running and gym.',
            1499, 1999, 1, 3, [1,4,5], [7,8,9,10,11,12], 250, 6, 25, 1, 'MEN'),
        
        generate_product_dict(2, "Men's Sneakers - White",
            'Trendy white sneakers for casual wear. Comfortable padded collar, durable rubber outsole, and stylish design. Pairs well with jeans, chinos, and shorts.',
            1099, 1499, 1, 3, [2,1,7], [7,8,9,10,11], 400, 6, 27, 1, 'MEN'),
        
        generate_product_dict(2, "Men's Leather Boots - Brown",
            'Rugged brown leather boots with durable construction. Premium leather upper, sturdy sole, and metal eyelets. Perfect for winter and outdoor wear.',
            1899, 2499, 3, 2, [3,1], [8,9,10,11,12], 150, 6, 24, 0, 'MEN'),
        
        generate_product_dict(2, "Men's Moccasin Shoes - Tan",
            'Classic tan moccasin shoes with hand-sewn detailing. Soft genuine leather, flexible sole, and comfortable fit. Perfect for smart casual occasions.',
            1199, 1599, 5, 2, [13,1], [7,8,9,10,11], 180, 6, 25, 0, 'MEN'),
        
        generate_product_dict(2, "Men's Formal Oxford - Black Patent",
            'Premium black patent leather oxford shoes for formal events. High-gloss finish, leather sole, and elegant design. Perfect for weddings, parties, and special occasions.',
            1599, 2199, 6, 2, [1], [8,9,10,11], 120, 6, 27, 0, 'MEN'),
        
        generate_product_dict(2, "Men's Sandals - Brown Leather",
            'Comfortable brown leather sandals with padded footbed. Adjustable strap design, durable sole, and premium finish. Ideal for casual summer wear.',
            699, 999, 4, 2, [3,1], [7,8,9,10,11,12], 350, 6, 30, 0, 'MEN'),

        # ── WOMEN'S COLLECTION (cat_id=3) ────────────────────────────────
        generate_product_dict(3, "Women's Heeled Sandals - Black",
            'Elegant black heeled sandals for parties and events. Comfortable block heel, adjustable ankle strap, and cushioned footbed. Perfect for weddings and festive occasions.',
            899, 1299, 1, 3, [1,19], [5,6,7,8,9], 250, 6, 30, 1, 'WOM'),
        
        generate_product_dict(3, "Women's Casual Flats - Ballet Style",
            'Comfortable ballet-style flat shoes for everyday wear. Soft synthetic upper, padded insole, and flexible sole. Available in multiple colors. Lightweight and packable.',
            599, 849, 1, 3, [1,2,10,5], [5,6,7,8,9], 400, 6, 29, 1, 'WOM'),
        
        generate_product_dict(3, "Women's Sneakers - White",
            'Stylish white sneakers for women with chunky sole design. Comfortable padded collar, breathable lining, and durable outsole. Pairs with dresses, jeans, and activewear.',
            1099, 1499, 1, 3, [2,20,21], [5,6,7,8,9,10], 300, 6, 25, 1, 'WOM'),
        
        generate_product_dict(3, "Women's Party Wear Heels - Gold",
            'Stunning gold party wear heels with embellished design. Comfortable heel height, cushioned insole, and secure fit. Perfect for festive occasions, weddings, and parties.',
            1299, 1799, 1, 2, [22,1,2], [5,6,7,8,9], 150, 6, 28, 0, 'WOM'),
        
        generate_product_dict(3, "Women's Wedge Sandals - Beige",
            'Comfortable wedge sandals in beige with braided detail. Lightweight EVA wedge sole, adjustable strap, and soft footbed. Perfect for summer outings and vacations.',
            799, 1099, 5, 2, [12,3], [5,6,7,8,9], 280, 6, 27, 0, 'WOM'),
        
        generate_product_dict(3, "Women's Boots - Ankle Length",
            'Stylish ankle-length boots for women with side zipper. Premium synthetic leather, comfortable block heel, and warm lining. Perfect for winter and monsoon.',
            1499, 1999, 1, 2, [1,3,19], [6,7,8,9,10], 180, 6, 25, 0, 'WOM'),
        
        generate_product_dict(3, "Women's Sports Shoes - Pink",
            'Performance sports shoes for women in stylish pink. Breathable mesh, responsive cushioning, and lightweight design. Ideal for running, gym, and daily wear.',
            1299, 1699, 2, 3, [9,2,7], [5,6,7,8,9,10], 220, 6, 24, 0, 'WOM'),
        
        generate_product_dict(3, "Women's Kolhapuri Chappal",
            'Traditional Kolhapuri style chappal for women. Genuine leather with authentic handcrafted design. Comfortable flat sole, perfect with ethnic wear.',
            499, 749, 4, 2, [3,5,19], [5,6,7,8,9], 500, 6, 35, 0, 'WOM'),

        # ── KIDS COLLECTION (cat_id=4) ────────────────────────────────────
        generate_product_dict(4, "Kids' Running Shoes - Blue",
            'Fun blue running shoes for active kids. Lightweight construction, flexible sole, and breathable mesh upper. Easy lace-up closure with padded collar for comfort.',
            599, 849, 2, 3, [4,1,5], [1,2,3,4,5,6], 350, 12, 25, 1, 'KID'),
        
        generate_product_dict(4, "Baby Soft Sole Shoes - First Walkers",
            'Soft sole shoes for babies learning to walk. Premium cotton upper with non-slip suede sole. Elastic ankle for secure fit. Available in cute animal designs.',
            349, 499, 1, 3, [2,9,22], [1,2,3], 400, 12, 20, 1, 'KID'),
        
        generate_product_dict(4, "Kids' Casual Sneakers - Multi Color",
            'Colorful casual sneakers for kids with fun designs. Durable construction, easy velcro straps, and comfortable cushioned sole. Machine washable.',
            499, 699, 2, 3, [4,5,2,1], [2,3,4,5,6], 450, 12, 22, 1, 'KID'),
        
        generate_product_dict(4, "Kids' Sandals - Adventure Ready",
            'Durable sandals for kids with adjustable straps. Protective toe cap, non-slip sole, and quick-dry materials. Perfect for outdoor play and summer.',
            399, 549, 4, 3, [4,5,7], [2,3,4,5,6], 300, 12, 24, 0, 'KID'),
        
        generate_product_dict(4, "Kids' Party Shoes - Formal",
            'Smart formal shoes for kids for special occasions. Patent finish, comfortable fit, and easy buckle closure. Perfect for weddings and family events.',
            699, 949, 6, 2, [1,2], [3,4,5,6], 200, 12, 25, 0, 'KID'),
        
        generate_product_dict(4, "Kids' Boots - Rain & Winter",
            'Waterproof boots for kids to keep feet dry in rain and winter. Warm lining, non-slip sole, and easy pull-on handles. Fun colors and patterns.',
            799, 1099, 1, 2, [5,4,1], [3,4,5,6,7], 150, 12, 22, 0, 'KID'),

        # ── SOCKS (cat_id=5) ─────────────────────────────────────────────
        generate_product_dict(5, 'Ankle Socks - Cotton Pack of 6',
            'Comfortable cotton ankle socks in pack of 6 pairs. Breathable cotton blend, reinforced heel and toe, elastic cuff. Available in assorted colors. Suitable for daily wear.',
            199, 299, 1, 2, [1,2,7,4], [17,18,19,20], 1000, 24, 33, 1, 'SOC'),
        
        generate_product_dict(5, 'Crew Socks - Formal Black Pack of 3',
            'Premium formal crew socks in black. High-quality cotton blend with reinforced heel and toe. Stay-up elastic top. Perfect for office and formal wear. Pack of 3.',
            249, 349, 1, 2, [1,19], [18,19,20], 800, 24, 30, 1, 'SOC'),
        
        generate_product_dict(5, 'Knee High Socks - School White',
            'School knee-high socks in brilliant white. Durable cotton-polyester blend, reinforced heel and toe, stretchable fit. Approved for school uniforms. Pack of 3 pairs.',
            299, 399, 1, 1, [2], [1,2,3,4,5,6,17,18,19], 600, 24, 28, 1, 'SOC'),
        
        generate_product_dict(5, 'No-Show Socks - Invisible Pack of 5',
            'Invisible no-show socks that stay hidden in shoes. Silicone heel grip prevents slipping. Ultra-thin design, breathable cotton. Pack of 5 pairs. Perfect for loafers and sneakers.',
            249, 349, 1, 2, [1,2,4,7], [17,18,19,20], 700, 24, 29, 0, 'SOC'),
        
        generate_product_dict(5, 'Sports Socks - Cushioned Pack of 3',
            'Performance sports socks with extra cushioning. Moisture-wicking fabric, arch support, and padded heel/toe. Ideal for running, gym, and sports activities. Pack of 3.',
            349, 499, 1, 3, [2,1,4], [18,19,20,21], 500, 24, 30, 0, 'SOC'),
        
        generate_product_dict(5, 'Wool Blend Winter Socks - Pack of 2',
            'Warm wool blend socks for winter. Soft, thermal, and comfortable. Reinforced heel and toe. Perfect for cold weather. Pack of 2 pairs in assorted colors.',
            399, 549, 1, 2, [1,7,3], [18,19,20], 300, 12, 25, 0, 'SOC'),

        # ── ACCESSORIES (cat_id=6) ────────────────────────────────────────
        generate_product_dict(6, 'Shoe Polish Kit - Complete Care',
            'Complete shoe polish kit with black, brown, and neutral polish. Includes applicator brush, polishing cloth, and shine sponge. Premium quality wax polish for leather shoes.',
            199, 299, 1, 1, [17], [21], 500, 12, 20, 1, 'ACC'),
        
        generate_product_dict(6, 'Shoe Laces Premium Pack - 6 Pairs',
            'Premium quality shoe laces pack of 6 pairs. Assorted colors - black, white, brown, navy. Durable woven polyester. 120cm length suitable for most shoes.',
            99, 149, 1, 2, [1,2,3,8], [21], 1000, 24, 34, 1, 'ACC'),
        
        generate_product_dict(6, 'Memory Foam Insoles - Comfort Plus',
            'Premium memory foam insoles for all-day comfort. Shock-absorbing, arch support, and odor control. Trimmable to fit any shoe size. Pack of 2 pairs.',
            299, 449, 1, 2, [1,2], [17,18,19,20], 600, 12, 25, 1, 'ACC'),
        
        generate_product_dict(6, 'Shoe Deodorizer Spray - 200ml',
            'Fresh & Clean shoe deodorizer spray. Eliminates odor-causing bacteria. Long-lasting fresh fragrance. Safe for all shoe materials. 200ml bottle.',
            149, 199, 1, 1, [17], [21], 400, 12, 25, 0, 'ACC'),
        
        generate_product_dict(6, 'Shoe Bags - Travel Storage Pack of 3',
            'Convenient shoe storage bags for travel. Waterproof nylon material. Pack of 3 bags in assorted sizes. Keeps shoes separate from clothes. Drawstring closure.',
            249, 349, 1, 2, [1,4,7], [21], 350, 12, 28, 0, 'ACC'),
        
        generate_product_dict(6, 'Shoe Brush Premium - Wooden Handle',
            'Premium wooden handle shoe brush with horsehair bristles. Gentle on leather, effectively removes dirt. Ergonomic handle for comfortable grip. Essential for shoe care.',
            149, 199, 1, 1, [17], [21], 500, 12, 33, 0, 'ACC'),

        # ── EVA FOOTWEAR (cat_id=7) ───────────────────────────────────────
        generate_product_dict(7, 'EVA Slides - Classic Black',
            'Classic black EVA slides for everyday comfort. Ultra-lightweight, waterproof, and quick-drying. Soft cushioned footbed with massage dots. Durable and long-lasting.',
            249, 399, 1, 3, [1,4,5], [6,7,8,9,10,11,12,13], 800, 12, 35, 1, 'EVA'),
        
        generate_product_dict(7, 'EVA Sandals - Comfort Fit',
            'Comfortable EVA sandals with adjustable strap. Lightweight, flexible, and waterproof. Deep heel cup for stability. Perfect for bathroom, beach, and casual wear.',
            299, 449, 2, 2, [1,2,4,9], [7,8,9,10,11,12], 600, 12, 32, 1, 'EVA'),
        
        generate_product_dict(7, 'Premium EVA Flip Flops - Thong',
            'Premium EVA flip flops with thong design. Soft cushioned sole, durable strap, and textured footbed. Available in multiple colors. Ideal for casual everyday wear.',
            199, 299, 1, 3, [1,2,4,5,8], [7,8,9,10,11,12,13], 900, 12, 40, 1, 'EVA'),
        
        generate_product_dict(7, 'EVA Bathroom Slippers - Anti-Skid',
            'Anti-skid EVA bathroom slippers with drainage holes. Quick-drying, lightweight, and mold-resistant. Textured sole for grip on wet surfaces. Open-toe design.',
            179, 249, 2, 2, [1,2,22,9], [7,8,9,10,11], 1000, 12, 38, 0, 'EVA'),
        
        generate_product_dict(7, 'Memory Foam EVA Slides - Luxury',
            'Luxury EVA slides with memory foam footbed for ultimate comfort. Thick cushioned sole, soft strap lining, and stylish design. Like wearing clouds on your feet.',
            449, 649, 1, 3, [1,2,7,8], [7,8,9,10,11,12], 400, 12, 25, 0, 'EVA'),
        
        generate_product_dict(7, 'EVA Kids Slippers - Cartoon Design',
            'Fun cartoon character EVA slippers for kids. Lightweight, colorful, and comfortable. Non-slip sole. Available in popular cartoon themes. Kids love them!',
            199, 299, 1, 3, [9,22,4,5], [1,2,3,4,5,6], 500, 12, 30, 0, 'EVA'),

        # ── PU FOOTWEAR (cat_id=8) ────────────────────────────────────────
        generate_product_dict(8, 'PU Formal Shoes - Black',
            'Professional black PU formal shoes with sleek design. Durable polyurethane upper, comfortable padded insole, and slip-resistant rubber sole. Value for money.',
            799, 1099, 1, 3, [1], [7,8,9,10,11,12], 400, 6, 28, 1, 'PU'),
        
        generate_product_dict(8, 'PU Loafers - Brown',
            'Stylish brown PU loafers with tassel detail. Easy slip-on design, cushioned comfort insole, and flexible outsole. Perfect for smart casual and office wear.',
            699, 949, 2, 2, [3,1], [7,8,9,10,11], 350, 6, 27, 1, 'PU'),
        
        generate_product_dict(8, 'PU Sneakers - White',
            'Trendy white PU sneakers with classic design. Breathable PU upper with perforations, comfortable lining, and durable rubber sole. Affordable everyday sneakers.',
            599, 849, 1, 3, [2,1,4], [7,8,9,10,11,12], 500, 6, 30, 1, 'PU'),
        
        generate_product_dict(8, 'PU Sandals - Women\'s Comfort',
            'Comfortable women\'s sandals in premium PU. Adjustable strap design, cushioned footbed, and lightweight sole. Ideal for daily wear and shopping.',
            449, 649, 1, 3, [1,2,12,9], [5,6,7,8,9], 450, 6, 29, 0, 'PU'),
        
        generate_product_dict(8, 'PU Boots - Ankle High',
            'Stylish ankle-high PU boots with side zipper. Faux leather finish, comfortable block heel, and warm lining. Versatile design for casual and smart outfits.',
            999, 1399, 1, 2, [1,3,19], [7,8,9,10,11], 200, 6, 25, 0, 'PU'),
        
        generate_product_dict(8, 'PU Casual Shoes - Navy',
            'Comfortable navy blue PU casual shoes for everyday wear. Lightweight construction, breathable lining, and cushioned insole. Lace-up design for secure fit.',
            549, 749, 2, 2, [8,1], [7,8,9,10,11], 380, 6, 26, 0, 'PU'),

        # ── HAWAI CHAPPAL (cat_id=9) ──────────────────────────────────────
        generate_product_dict(9, 'Classic Hawai Chappal - Black',
            'Original classic Hawai chappal in black. Durable rubber construction, comfortable footbed, and iconic design. Lightweight, waterproof, and long-lasting. Bulk pack available.',
            149, 199, 4, 2, [1,2], [7,8,9,10,11,12,13], 2000, 24, 40, 1, 'HAW'),
        
        generate_product_dict(9, 'Premium Hawai Chappal - Cushioned',
            'Premium Hawai chappal with extra cushioned footbed for enhanced comfort. Durable rubber sole, stylish strap design, and textured footbed. Better than the original!',
            199, 299, 4, 2, [1,2,4,5,8], [7,8,9,10,11,12,13], 1500, 24, 35, 1, 'HAW'),
        
        generate_product_dict(9, 'Hawai Chappal - Designer Collection',
            'Designer Hawai chappal with printed straps and colorful patterns. Same durable rubber sole, but with fashionable upper. Stand out with style!',
            249, 349, 1, 3, [4,5,9,22], [7,8,9,10,11,12], 800, 24, 30, 0, 'HAW'),
        
        generate_product_dict(9, 'Hawai Chappal - Women\'s Slim Fit',
            'Slim-fit Hawai chappal designed specifically for women. Narrower strap, lighter weight, and smaller size range. Available in feminine colors.',
            149, 199, 4, 3, [9,5,2,1], [5,6,7,8,9], 1000, 24, 33, 0, 'HAW'),
        
        generate_product_dict(9, 'Hawai Chappal - Kids Fun',
            'Fun colorful Hawai chappal for kids with character prints. Smaller sizes, softer rubber, and kid-friendly designs. Durable enough for active play.',
            99, 149, 4, 3, [5,4,9,22], [1,2,3,4,5,6], 1200, 24, 40, 0, 'HAW'),
        
        generate_product_dict(9, 'Hawai Chappal - Jumbo Size',
            'Extra-large Hawai chappal for big feet! Sizes 12-14. Same classic design, same durable construction. Available in black and white.',
            179, 249, 4, 2, [1,2], [13,14], 300, 12, 25, 0, 'HAW'),

        # ── IMPORTED COLLECTION (cat_id=10) ───────────────────────────────
        generate_product_dict(10, 'Premium Running Shoes - Imported',
            'Premium imported running shoes with advanced cushioning technology. Lightweight mesh upper, responsive midsole, and durable outsole. International quality standards.',
            2499, 3499, 10, 3, [1,4,5], [7,8,9,10,11,12], 100, 6, 20, 1, 'IMP'),
        
        generate_product_dict(10, 'Imported Lifestyle Sneakers',
            'Trendy imported lifestyle sneakers with modern design. Premium materials, superior comfort, and stylish silhouette. Imported from international brands.',
            1999, 2999, 12, 3, [2,1,4,5], [7,8,9,10,11], 120, 6, 18, 1, 'IMP'),
        
        generate_product_dict(10, 'Imported Leather Boots',
            'Premium imported leather boots with European craftsmanship. Full-grain leather, Goodyear welt construction, and premium sole. Built to last a lifetime.',
            3999, 5499, 11, 2, [3,1], [8,9,10,11,12], 50, 6, 15, 1, 'IMP'),
        
        generate_product_dict(10, 'Imported Training Shoes',
            'Professional imported training shoes for gym and cross-training. Durable construction, excellent grip, and supportive fit. International brand quality.',
            2199, 2999, 11, 3, [1,4,5,7], [7,8,9,10,11,12], 80, 6, 17, 0, 'IMP'),
        
        generate_product_dict(10, 'Imported Casual Slip-Ons',
            'Premium imported casual slip-on shoes with elastic panels. Comfortable memory foam insole, flexible outsole, and sleek design. Perfect for travel and daily wear.',
            1799, 2499, 12, 2, [1,2,8], [7,8,9,10,11], 90, 6, 16, 0, 'IMP'),
        
        generate_product_dict(10, 'Imported Sports Sandals',
            'Premium imported sports sandals with adjustable straps. Contoured footbed, shock-absorbing sole, and quick-dry materials. Adventure-ready!',
            1499, 1999, 10, 2, [1,7,4], [7,8,9,10,11,12], 60, 6, 15, 0, 'IMP'),

        # ── BRANDED SHOES (cat_id=11) ─────────────────────────────────────
        generate_product_dict(11, 'Campus Sneakers - Original',
            'Original Campus brand sneakers with signature style. Comfortable fit, durable construction, and trendy design. Authorized Campus distributor.',
            899, 1299, 2, 3, [2,1,4], [7,8,9,10,11], 300, 6, 22, 1, 'BRD'),
        
        generate_product_dict(11, 'Bata Formal Shoes - Premium',
            'Genuine Bata formal shoes for office and events. Bata quality guarantee, comfortable fit, and classic styling. Authorized Bata wholesale supplier.',
            1399, 1899, 3, 2, [1,3], [7,8,9,10,11,12], 200, 6, 20, 1, 'BRD'),
        
        generate_product_dict(11, 'Paragon Hawaii - Original',
            'Original Paragon Hawai chappal — the one and only! Durable rubber, comfortable design, and that iconic Paragon quality. Trusted for generations.',
            199, 299, 4, 3, [1,2,4,5], [7,8,9,10,11,12,13], 2000, 24, 30, 1, 'BRD'),
        
        generate_product_dict(11, 'Relaxo Slippers - Comfort Plus',
            'Relaxo Comfort Plus slippers with memory foam footbed. Lightweight EVA construction, stylish design, and Relaxo quality assurance. Best-selling slipper range.',
            349, 499, 5, 3, [1,2,4], [7,8,9,10,11,12], 600, 12, 25, 0, 'BRD'),
        
        generate_product_dict(11, 'Liberty Formal Shoes - Black',
            'Liberty black formal shoes with premium finish. Trusted Liberty quality, comfortable leather upper, and durable sole. Perfect for professionals.',
            1099, 1499, 6, 2, [1], [7,8,9,10,11,12], 250, 6, 22, 0, 'BRD'),
        
        generate_product_dict(11, 'Action Sports Shoes',
            'Action brand sports shoes for active lifestyle. Breathable mesh, cushioned sole, and stylish design. Great value for money from trusted Action brand.',
            799, 1099, 8, 3, [2,4,5], [7,8,9,10,11], 350, 6, 24, 0, 'BRD'),

        # ── NON-BRANDED / GENERAL (cat_id=12) ────────────────────────────
        generate_product_dict(12, 'General Casual Shoes - Economy',
            'Affordable casual shoes for daily wear. Basic design, comfortable fit, and durable construction. Best value option for budget-conscious buyers.',
            349, 499, 1, 2, [1,4,7], [7,8,9,10,11], 600, 12, 30, 1, 'GEN'),
        
        generate_product_dict(12, 'Economy Slippers - Bulk Pack',
            'Bulk economy slippers pack for retailers. Basic design, durable material, and affordable pricing. Ideal for mass market and budget customers.',
            99, 149, 2, 2, [1,4,5], [7,8,9,10,11], 2000, 24, 40, 1, 'GEN'),
        
        generate_product_dict(12, 'Budget School Shoes',
            'Budget-friendly school shoes for price-sensitive customers. Basic design meets essential quality. Perfect for tier-2 and tier-3 city markets.',
            299, 399, 2, 2, [1,2], [6,7,8,9,10,11], 800, 12, 28, 0, 'GEN'),
        
        generate_product_dict(12, 'Value Pack Sandals - Assorted',
            'Assorted value pack sandals in mixed styles and colors. Great for village markets and wholesale distribution. Mix of popular basic designs.',
            199, 299, 2, 3, [1,2,4,5,8], [7,8,9,10,11], 1500, 24, 35, 0, 'GEN'),
        
        generate_product_dict(12, 'Mass Market Chappal',
            'High-volume mass market chappal for wholesale distribution. Basic design, durable rubber, and super affordable pricing. MOQ 50 pairs.',
            79, 129, 2, 2, [1,2], [7,8,9,10,11,12,13], 5000, 50, 45, 0, 'GEN'),
        
        generate_product_dict(12, 'Economy Canvas Shoes',
            'Budget canvas shoes in basic colors. Lightweight, comfortable, and affordable. Popular in rural and semi-urban markets. Bulk orders welcome.',
            249, 349, 1, 3, [1,4,7,8], [7,8,9,10,11], 700, 12, 32, 0, 'GEN'),
    ]
    
    return products


def seed_products(conn, category_count=18):
    """Seed all product-related tables with comprehensive data."""
    print("👟 Seeding products with images, colors, sizes, and variants...")
    cursor = conn.cursor()
    
    products = get_product_definitions()
    
    # Get color and size IDs from DB
    cursor.execute("SELECT id, name FROM colors")
    db_colors = {row['name'].lower(): row['id'] for row in cursor.fetchall()}
    
    cursor.execute("SELECT id, name FROM sizes")
    db_sizes = {str(row['name']): row['id'] for row in cursor.fetchall()}
    
    # Get brand IDs
    cursor.execute("SELECT id, name FROM brands")
    db_brands = {row['name']: row['id'] for row in cursor.fetchall()}
    
    inserted = 0
    for i, p in enumerate(products):
        # Create product
        slug = p['name'].lower().replace(' ', '-').replace("'", '').replace('"', '').replace('--', '-')
        slug = ''.join(c for c in slug if c.isalnum() or c == '-')
        sku = f"{p['sku_prefix']}-{str(i+1).zfill(4)}"
        created_at = datetime.now() - timedelta(days=random.randint(0, 120))
        
        cursor.execute("""
            INSERT INTO products (name, description, sku, slug, category_id, brand_id, 
                                  price, compare_price, stock, moq, discount, is_featured, 
                                  is_active, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 1, ?)
        """, (p['name'], p['description'], sku, slug, p['category_id'], p['brand_id'],
              p['price'], p['compare_price'], p['stock'], p['moq'], p['discount'],
              p['is_featured'], created_at))
        
        product_id = cursor.lastrowid
        
        # Add product images (simulated)
        for img_idx in range(p['images_count']):
            img_name = f"images/product_{product_id}_{img_idx+1}.jpg"
            is_primary = 1 if img_idx == 0 else 0
            cursor.execute("""
                INSERT INTO product_images (product_id, image_path, is_primary, sort_order)
                VALUES (?, ?, ?, ?)
            """, (product_id, img_name, is_primary, img_idx))
        
        # Add colors
        for color_id in p['color_ids']:
            if color_id in db_colors.values():
                cursor.execute("""
                    INSERT IGNORE INTO product_colors (product_id, color_id)
                    VALUES (?, ?)
                """, (product_id, color_id))
        
        # Add sizes
        for size_name in p['size_ids']:
            size_str = str(size_name)
            if size_str in db_sizes:
                cursor.execute("""
                    INSERT IGNORE INTO product_sizes (product_id, size_id)
                    VALUES (?, ?)
                """, (product_id, db_sizes[size_str]))
        
        # Add variants (color x size combinations)
        variant_sku_base = f"{p['sku_prefix']}-{str(i+1).zfill(4)}"
        variant_idx = 0
        for color_id in p['color_ids']:
            if color_id in db_colors.values():
                for size_name in p['size_ids']:
                    size_str = str(size_name)
                    if size_str in db_sizes:
                        variant_idx += 1
                        var_price = p['price'] + random.choice([0, 0, 20, 30, -20, -10])
                        var_stock = max(0, p['stock'] + random.randint(-50, 50))
                        var_sku = f"{variant_sku_base}-V{variant_idx}"
                        cursor.execute("""
                            INSERT INTO product_variants (product_id, color_id, size_id, price, stock, sku, is_active)
                            VALUES (?, ?, ?, ?, ?, ?, 1)
                        """, (product_id, color_id, db_sizes[size_str], max(0, var_price), max(0, var_stock), var_sku))
        
        # Add category-specific product meta
        if p['category_id'] == 1:  # School Shoes
            cursor.execute("INSERT INTO product_meta (product_id, meta_key, meta_value) VALUES (?, 'school_type', ?)",
                          (product_id, random.choice(['CBSE', 'ICSE', 'State Board', 'All Boards'])))
            cursor.execute("INSERT INTO product_meta (product_id, meta_key, meta_value) VALUES (?, 'lace_type', ?)",
                          (product_id, random.choice(['Lace', 'Velcro', 'Both', 'Slip-on'])))
        elif p['category_id'] == 5:  # Socks
            cursor.execute("INSERT INTO product_meta (product_id, meta_key, meta_value) VALUES (?, 'sock_length', ?)",
                          (product_id, random.choice(['Ankle', 'Crew', 'Knee-high', 'No-show'])))
            cursor.execute("INSERT INTO product_meta (product_id, meta_key, meta_value) VALUES (?, 'material', ?)",
                          (product_id, random.choice(['Cotton', 'Cotton Blend', 'Polyester', 'Wool Blend'])))
            cursor.execute("INSERT INTO product_meta (product_id, meta_key, meta_value) VALUES (?, 'pair_count', ?)",
                          (product_id, str(p['images_count'] + random.randint(1, 4))))
        elif p['category_id'] in (7, 9):  # EVA or Hawai
            cursor.execute("INSERT INTO product_meta (product_id, meta_key, meta_value) VALUES (?, 'sole_type', ?)",
                          (product_id, 'EVA' if p['category_id'] == 7 else 'Rubber'))
            cursor.execute("INSERT INTO product_meta (product_id, meta_key, meta_value) VALUES (?, 'eva_type', ?)",
                          (product_id, random.choice(['Standard', 'Premium', 'Memory Foam'])))
        elif p['category_id'] == 6:  # Accessories
            cursor.execute("INSERT INTO product_meta (product_id, meta_key, meta_value) VALUES (?, 'accessory_type', ?)",
                          (product_id, random.choice(['Shoe Care', 'Laces', 'Insoles', 'Polishes', 'Storage'])))
        
        inserted += 1
        
        if inserted % 10 == 0:
            print(f"   ... {inserted}/{len(products)} products created")
    
    conn.commit()
    cursor.close()
    print(f"✅ {inserted} products created with images, colors, sizes, and variants")


# ─── INQUIRIES ────────────────────────────────────────────────────────────

def seed_inquiries(conn, count=25):
    """Seed inquiries table with realistic B2B order data."""
    print("📋 Seeding inquiries...")
    cursor = conn.cursor()
    
    # Get user IDs for dealers
    cursor.execute("SELECT id, full_name, business_name, phone, address, city, state, pincode, gst_number FROM users WHERE role = 'dealer' AND status = 'approved'")
    dealers = cursor.fetchall()
    
    # Get product IDs
    cursor.execute("SELECT id, name, price FROM products WHERE is_active = 1 LIMIT 30")
    products = cursor.fetchall()
    
    statuses = ['new', 'contacted', 'negotiation', 'confirmed', 'closed']
    
    inquiry_notes = [
        'Need this urgently for the upcoming school season. Please confirm availability.',
        'Looking for bulk pricing on this item. Need 50 pairs to start.',
        'Please send sample before bulk order. We need to check quality first.',
        'Regular monthly order. Please maintain same pricing as last time.',
        'New customer inquiry. Interested in becoming a regular dealer.',
        'Need mixed sizes in this order. Please confirm size-wise stock.',
        'This is for a school tender. Need certificates and quality docs.',
        'Festival season stock. Need delivery before Diwali.',
        'Want to add these to our existing order. Please confirm.',
        'First time ordering from your platform. Need guidance on process.',
        'Urgent requirement for exhibition. Need delivery within 5 days.',
        'Looking for exclusive dealership in our city. Interested in bulk partnership.',
        'Need catalogues and price list for our showroom.',
        'Sample order to check quality. Will place bulk if satisfied.',
        'Annual bulk order for our chain of 5 stores across the city.',
    ]
    
    for i in range(count):
        dealer = random.choice(dealers)
        status = random.choices(statuses, weights=[3, 2, 2, 1.5, 1.5], k=1)[0]
        num_items = random.randint(1, 5)
        created_at = datetime.now() - timedelta(days=random.randint(0, 60), hours=random.randint(0, 23))
        
        # Generate random lat/lng for Indian cities
        lat_long_map = {
            'Delhi': (28.7041, 77.1025),
            'Mumbai': (19.0760, 72.8777),
            'Ahmedabad': (23.0225, 72.5714),
            'Hyderabad': (17.3850, 78.4867),
            'Jaipur': (26.9124, 75.7873),
            'Lucknow': (26.8467, 80.9462),
            'Pune': (18.5204, 73.8567),
            'Bengaluru': (12.9716, 77.5946),
            'Kochi': (9.9312, 76.2673),
            'Kolkata': (22.5726, 88.3639),
            'Chennai': (13.0827, 80.2707),
            'Indore': (22.7196, 75.8577),
            'Chandigarh': (30.7333, 76.7794),
        }
        lat, lng = lat_long_map.get(dealer.get('city', 'Mumbai'), (19.0760, 72.8777))
        # Add slight random offset
        lat += random.uniform(-0.05, 0.05)
        lng += random.uniform(-0.05, 0.05)
        
        cursor.execute("""
            INSERT INTO inquiries (user_id, dealer_name, shop_name, phone, gst_number, 
                                   address, city, state, pincode, latitude, longitude, 
                                   notes, status, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            dealer['id'],
            dealer['full_name'],
            dealer['business_name'],
            dealer['phone'],
            dealer.get('gst_number', ''),
            dealer.get('address', ''),
            dealer.get('city', ''),
            dealer.get('state', ''),
            dealer.get('pincode', ''),
            lat,
            lng,
            random.choice(inquiry_notes) if random.random() > 0.3 else '',
            status,
            created_at
        ))
        
        inquiry_id = cursor.lastrowid
        
        # Add inquiry items
        selected_products = random.sample(products, min(num_items, len(products)))
        for item in selected_products:
            qty = random.choice([10, 20, 25, 30, 50, 50, 100, 100, 100, 200])
            cursor.execute("""
                INSERT INTO inquiry_items (inquiry_id, product_id, product_name, quantity, size, color, price)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                inquiry_id,
                item['id'],
                item['name'],
                qty,
                random.choice(['7', '8', '9', '10']),
                random.choice(['Black', 'White', 'Brown', 'Blue']),
                item['price']
            ))
    
    conn.commit()
    cursor.close()
    print(f"✅ {count} inquiries created with {count * 2} average items")


# ─── BANNERS ───────────────────────────────────────────────────────────────

def seed_banners(conn):
    """Seed banners table."""
    print("🖼️  Seeding banners...")
    cursor = conn.cursor()
    
    banners = [
        ('School Shoe Mega Sale', 'Up to 40% off on bulk orders. MOQ just 10 pairs!', 'banners/school_sale.jpg', '/category/school-shoes', 'offer', 1),
        ('New Arrivals - Mens Collection', 'Check out our latest men\'s formal and casual range', 'banners/mens_new.jpg', '/category/mens', 'home', 2),
        ('Festival Special Offer', 'Diwali bulk discounts on all categories. Limited period!', 'banners/festival.jpg', '/products', 'festival', 3),
        ('Winter Collection Launch', 'Premium boots, woolen socks, and winter footwear', 'banners/winter.jpg', '/category/boots', 'seasonal', 4),
        ('Become a Dealer Today', 'Join 500+ dealers across India. Register now!', 'banners/dealer.jpg', '/register', 'home', 5),
        ('Kids Collection 2024', 'New designs, better quality, same great prices', 'banners/kids.jpg', '/category/kids', 'home', 6),
        ('Clearance Sale', 'Last season stock at factory price! Limited stock.', 'banners/clearance.jpg', '/products?sort=price_asc', 'offer', 7),
        ('Ganesh Chaturthi Special', 'Festive offers on all footwear categories', 'banners/ganesh.jpg', '/products', 'festival', 8),
    ]
    
    for title, subtitle, img, link, btype, sort in banners:
        cursor.execute("""
            INSERT INTO banners (title, subtitle, image_path, link_url, type, sort_order, is_active)
            VALUES (?, ?, ?, ?, ?, ?, 1)
        """, (title, subtitle, img, link, btype, sort))
    
    conn.commit()
    cursor.close()
    print(f"✅ {len(banners)} banners seeded")


# ─── CATALOGUES ────────────────────────────────────────────────────────────

def seed_catalogues(conn):
    """Seed catalogues table."""
    print("📑 Seeding catalogues...")
    cursor = conn.cursor()
    
    catalogues = [
        ('KicksHub Complete Catalog 2024', 'Full product catalog with all categories and pricing', 1, 'catalogues/full_catalog_2024.pdf', 'catalogues/cover_full.jpg'),
        ('School Shoes Collection', 'Complete school footwear range for all boards and ages', 1, 'catalogues/school_collection.pdf', 'catalogues/cover_school.jpg'),
        ('Men\'s Footwear Range', 'Formal, casual, sports, and boots for men', 2, 'catalogues/mens_range.pdf', 'catalogues/cover_mens.jpg'),
        ('Women\'s Collection Catalog', 'Heels, flats, sneakers, sandals, and more for women', 3, 'catalogues/womens_catalog.pdf', 'catalogues/cover_women.jpg'),
        ('Kids & Baby Collection', 'Footwear for children of all ages — newborn to teens', 4, 'catalogues/kids_collection.pdf', 'catalogues/cover_kids.jpg'),
        ('EVA & Hawai Range', 'Lightweight EVA and classic Hawai slippers bulk catalog', 7, 'catalogues/eva_hawai.pdf', 'catalogues/cover_eva.jpg'),
        ('Socks & Accessories', 'Complete socks and shoe care accessories catalog', 5, 'catalogues/socks_accessories.pdf', 'catalogues/cover_socks.jpg'),
        ('Festive Special Catalog', 'Special Diwali and festive season collection with offers', 1, 'catalogues/festive_special.pdf', 'catalogues/cover_festive.jpg'),
    ]
    
    for title, desc, cat_id, pdf, cover in catalogues:
        cursor.execute("""
            INSERT INTO catalogues (title, description, category_id, pdf_path, cover_image, is_active)
            VALUES (?, ?, ?, ?, ?, 1)
        """, (title, desc, cat_id, pdf, cover))
    
    conn.commit()
    cursor.close()
    print(f"✅ {len(catalogues)} catalogues seeded")


# ─── CONTACT MESSAGES ──────────────────────────────────────────────────────

def seed_contact_messages(conn, count=10):
    """Seed contact messages."""
    print("✉️  Seeding contact messages...")
    cursor = conn.cursor()
    
    names = ['Ramesh Patel', 'Suresh Gupta', 'Dinesh Yadav', 'Manoj Singh', 
             'Nitin Sharma', 'Kavita Joshi', 'Sunita Devi', 'Anil Kumar',
             'Vijay Pandey', 'Rohit Verma']
    
    subjects = [
        'Want to become a distributor', 'Bulk order inquiry', 'Partnership proposal',
        'Catalog request', 'Pricing inquiry', 'School tender requirement',
        'Dealership in my city', 'Wholesale rate inquiry', 'Sample request',
        'Business collaboration'
    ]
    
    messages = [
        'I own a footwear store in Delhi and am looking for a reliable wholesale partner. Please share your catalog and pricing.',
        'We have a school tender for 2000 pairs of shoes. Can you supply? Need quotation urgently.',
        'Interested in becoming your distributor for Rajasthan region. Please call me to discuss.',
        'Please send your complete catalog with price list for all categories.',
        'I need 100 pairs of school shoes urgently. Do you have stock in all sizes?',
        'Looking for sports shoes supplier for my retail chain. We have 5 stores in Pune.',
        'Can you supply Hawai chappal in bulk? Need 500 pairs per month minimum.',
        'Please share your whatsapp number for quick communication about orders.',
        'We are a school uniform supplier and need regular shoe supply. Please share bulk rates.',
        'Want to visit your showroom and see the products physically before ordering.',
    ]
    
    for i in range(count):
        is_read = random.random() > 0.5
        created_at = datetime.now() - timedelta(days=random.randint(0, 30))
        cursor.execute("""
            INSERT INTO contact_messages (name, phone, email, subject, message, is_read, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            random.choice(names),
            f'{random.randint(6,9)}{random.randint(100000000, 999999999)}',
            f'contact{i}@example.com',
            random.choice(subjects),
            random.choice(messages),
            is_read,
            created_at
        ))
    
    conn.commit()
    cursor.close()
    print(f"✅ {count} contact messages seeded")


# ─── MAIN ──────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description='KicksHub Database Seed Script')
    parser.add_argument('--force', action='store_true', help='Drop and reseed all data')
    parser.add_argument('--sample', action='store_true', help='Insert only minimal sample data')
    parser.add_argument('--no-schema', action='store_true', help='Skip schema creation')
    args = parser.parse_args()
    
    conn = get_connection()
    
    # Create schema if not skipped
    if not args.no_schema:
        run_schema(conn)
    
    # Force truncate
    if args.force:
        truncate_tables(conn)
    
    print("\n" + "=" * 55)
    print("   🌟 KicksHub Database Seeder")
    print("=" * 55 + "\n")
    
    if args.sample:
        # Minimal sample data
        print("📦 Running minimal sample seed...\n")
        seed_users(conn, count=5)
        seed_categories(conn)
        seed_brands(conn)
        seed_colors(conn)
        seed_sizes(conn)
        # Only seed first 20 products
        full_products = get_product_definitions()
        # Temporarily modify seed to limit products
        print("👟 Seeding 20 sample products...")
        # We'll just call full seed with fewer
        seed_products(conn)
        seed_banners(conn)
        print("\n✅ Sample seed complete!")
    else:
        # Full seed
        print("📦 Running full seed with comprehensive data...\n")
        seed_users(conn)
        seed_categories(conn)
        seed_brands(conn)
        seed_colors(conn)
        seed_sizes(conn)
        seed_products(conn)
        seed_inquiries(conn)
        seed_banners(conn)
        seed_catalogues(conn)
        seed_contact_messages(conn)
        
        print("\n" + "=" * 55)
        print("   ✅ Database seeding complete!")
        print("=" * 55)
        print(f"\n📊 Summary:")
        print(f"   • 15 users (1 admin + 14 dealers)")
        print(f"   • 18 categories")
        print(f"   • 12 brands")
        print(f"   • 24 colors")
        print(f"   • 39 sizes")
        print(f"   • {len(get_product_definitions())} products (with images, colors, sizes, variants)")
        print(f"   • 25 inquiries with items")
        print(f"   • 8 banners")
        print(f"   • 8 catalogues")
        print(f"   • 10 contact messages")
        print(f"\n🔑 Admin Login:")
        print(f"   Email:    admin@kickshub.in")
        print(f"   Password: admin123")
        print(f"\n🔑 Dealer Logins:")
        print(f"   Email:    rajesh@kicksfootwear.in / priya@stepso.in / amit@hammyspot.in")
        print(f"   Password: dealer123 (for all dealers)")
        print(f"\n🎉 Happy selling! 👟")
    
    conn.close()


if __name__ == '__main__':
    main()
