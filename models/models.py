"""
SQLite Database connection utilities
"""

import sqlite3
import os
from flask import g

DB_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'kickshub.db')
DB_PATH = os.path.normpath(DB_PATH)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def get_db():
    if 'db' not in g:
        conn = sqlite3.connect(DB_PATH)
        conn.row_factory = dict_factory
        conn.execute("PRAGMA foreign_keys = ON")
        conn.execute("PRAGMA journal_mode = WAL")
        g.db = conn
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def query(sql, params=(), one=False):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(sql, params)
    result = cursor.fetchone() if one else cursor.fetchall()
    cursor.close()
    return result

def execute(sql, params=()):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute(sql, params)
    conn.commit()
    last_id = cursor.lastrowid
    affected = cursor.rowcount
    cursor.close()
    return last_id or affected

def init_db():
    """Initialize the database by running schema.sql if tables don't exist."""
    schema_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'schema.sql')
    if not os.path.exists(schema_path):
        print(f"⚠️  schema.sql not found at {schema_path}")
        return

    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = dict_factory
    conn.execute("PRAGMA foreign_keys = ON")
    conn.execute("PRAGMA journal_mode = WAL")

    with open(schema_path, 'r', encoding='utf-8') as f:
        sql = f.read()

    # Execute schema (CREATE TABLE IF NOT EXISTS + INSERT OR IGNORE are idempotent)
    conn.executescript(sql)
    conn.commit()
    conn.close()
    print(f"✅ SQLite database initialized: {DB_PATH}")

def init_app(app):
    app.teardown_appcontext(close_db)