from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3

DB_PATH = r'D:\Antony\footwear-option2\backend\kickshub.db'

new_hash = generate_password_hash('admin123')
print("New hash:", new_hash)

conn = sqlite3.connect(DB_PATH, timeout=30)
conn.execute("PRAGMA journal_mode=DELETE")
conn.execute("UPDATE users SET password_hash = ? WHERE role = 'admin'", (new_hash,))
conn.commit()

row = conn.execute("SELECT password_hash FROM users WHERE role = 'admin'").fetchone()
print("Verify:", check_password_hash(row[0], 'admin123'))
conn.close()
print("Done!")