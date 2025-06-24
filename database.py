# File: database.py
import sqlite3
import configparser
import os
import bcrypt
from datetime import datetime

# --- Fungsi Konfigurasi dan Koneksi ---

def get_config_value(section, key):
    """Membaca nilai spesifik dari file config.ini."""
    config = configparser.ConfigParser()
    config_file_path = os.path.join(os.path.dirname(__file__), 'config.ini')
    if not os.path.exists(config_file_path):
        raise FileNotFoundError("File 'config.ini' tidak ditemukan.")
    config.read(config_file_path)
    try:
        return config[section][key]
    except KeyError:
        raise KeyError(f"Konfigurasi '{key}' di bawah section '[{section}]' tidak ditemukan.")

def create_connection():
    """Membuat koneksi ke database SQLite."""
    conn = None
    db_path = get_config_value('Database', 'Path')
    try:
        db_folder = os.path.dirname(db_path)
        if db_folder and not os.path.exists(db_folder):
            os.makedirs(db_folder)
        conn = sqlite3.connect(db_path, timeout=10) # Timeout 10 detik untuk mengatasi lock
    except Exception as e:
        print(f"Error connecting to database: {e}")
    return conn

# --- Fungsi Inisialisasi ---

def create_tables():
    """Membuat semua tabel yang dibutuhkan jika belum ada."""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            
            # Tabel Users (Hanya untuk Admin)
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                user_id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama TEXT NOT NULL,
                personal_number TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL DEFAULT 'superadmin'
            );
            """)

            # Tabel Categories
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS categories (
                category_id INTEGER PRIMARY KEY AUTOINCREMENT,
                category_name TEXT UNIQUE NOT NULL
            );
            """)

            # Tabel Items
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS items (
                item_id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_name TEXT NOT NULL,
                description TEXT,
                stock INTEGER NOT NULL DEFAULT 0,
                date_added TEXT NOT NULL,
                category_id INTEGER,
                FOREIGN KEY (category_id) REFERENCES categories (category_id)
            );
            """)

            # Tabel History Log
            cursor.execute("""
            CREATE TABLE IF NOT EXISTS history_log (
                log_id INTEGER PRIMARY KEY AUTOINCREMENT,
                item_id INTEGER,
                taker_name TEXT NOT NULL,
                quantity_taken INTEGER NOT NULL,
                date_taken TEXT NOT NULL,
                FOREIGN KEY (item_id) REFERENCES items (item_id) ON DELETE SET NULL
            );
            """)
            
            conn.commit()
        except sqlite3.Error as e:
            print(f"Error creating tables: {e}")
        finally:
            conn.close()

def setup_default_admin():
    """Membuat admin default dari config.ini jika belum ada user sama sekali."""
    conn = create_connection()
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users")
            if cursor.fetchone()[0] == 0:
                pn = get_config_value('Admin', 'DefaultPersonalNumber')
                pw = get_config_value('Admin', 'DefaultPassword')
                hashed_pw = bcrypt.hashpw(pw.encode('utf-8'), bcrypt.gensalt())
                
                cursor.execute(
                    "INSERT INTO users (nama, personal_number, password, role) VALUES (?, ?, ?, ?)",
                    ('Default Admin', pn, hashed_pw, 'superadmin')
                )
                conn.commit()
                print("Default admin created successfully.")
        except sqlite3.Error as e:
            print(f"Error setting up default admin: {e}")
        finally:
            conn.close()

# --- Fungsi Otentikasi ---

def validate_admin(personal_number, password):
    """Memvalidasi login admin."""
    conn = create_connection()
    user = None
    if conn is not None:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT password FROM users WHERE personal_number = ?", (personal_number,))
            result = cursor.fetchone()
            if result:
                stored_password_hash = result[0]
                if isinstance(stored_password_hash, str):
                    stored_password_hash = stored_password_hash.encode('utf-8')

                if bcrypt.checkpw(password.encode('utf-8'), stored_password_hash):
                    user = True # Login sukses
        except sqlite3.Error as e:
            print(f"Error validating admin: {e}")
        finally:
            conn.close()
    return user

# --- Fungsi-fungsi CRUD (Create, Read, Update, Delete) ---

# Kategori
def add_category(name):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("INSERT INTO categories (category_name) VALUES (?)", (name,))
            conn.commit()
        finally:
            conn.close()

def get_all_categories():
    conn = create_connection()
    categories = []
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT category_id, category_name FROM categories ORDER BY category_name")
            categories = cursor.fetchall()
        finally:
            conn.close()
    return categories

def update_category(cat_id, new_name):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("UPDATE categories SET category_name = ? WHERE category_id = ?", (new_name, cat_id))
            conn.commit()
        finally:
            conn.close()

def delete_category(cat_id):
    conn = create_connection()
    if conn:
        try:
            # Set category_id to NULL for items in this category before deleting
            cursor = conn.cursor()
            cursor.execute("UPDATE items SET category_id = NULL WHERE category_id = ?", (cat_id,))
            cursor.execute("DELETE FROM categories WHERE category_id = ?", (cat_id,))
            conn.commit()
        finally:
            conn.close()

# Item
def add_item(name, desc, stock, cat_id):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            cursor.execute(
                "INSERT INTO items (item_name, description, stock, date_added, category_id) VALUES (?, ?, ?, ?, ?)",
                (name, desc, stock, date, cat_id)
            )
            conn.commit()
        finally:
            conn.close()

def get_all_items_with_category():
    conn = create_connection()
    items = []
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT i.item_id, i.item_name, c.category_name, i.stock, i.description, i.date_added
                FROM items i
                LEFT JOIN categories c ON i.category_id = c.category_id
                ORDER BY i.item_name
            """)
            items = cursor.fetchall()
        finally:
            conn.close()
    return items

def update_item(item_id, name, desc, stock, cat_id):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute(
                "UPDATE items SET item_name = ?, description = ?, stock = ?, category_id = ? WHERE item_id = ?",
                (name, desc, stock, cat_id, item_id)
            )
            conn.commit()
        finally:
            conn.close()

def delete_item(item_id):
    conn = create_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM items WHERE item_id = ?", (item_id,))
            conn.commit()
        finally:
            conn.close()

# Logika Pengambilan Barang
def take_item(item_id, quantity, taker_name):
    conn = create_connection()
    success = False
    if conn:
        try:
            cursor = conn.cursor()
            # Cek stok dulu
            cursor.execute("SELECT stock FROM items WHERE item_id = ?", (item_id,))
            current_stock = cursor.fetchone()[0]

            if current_stock >= quantity:
                # Kurangi stok
                new_stock = current_stock - quantity
                cursor.execute("UPDATE items SET stock = ? WHERE item_id = ?", (new_stock, item_id))
                
                # Catat ke history
                date_taken = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                cursor.execute(
                    "INSERT INTO history_log (item_id, taker_name, quantity_taken, date_taken) VALUES (?, ?, ?, ?)",
                    (item_id, taker_name, quantity, date_taken)
                )
                conn.commit()
                success = True
        except sqlite3.Error as e:
            print(f"Error taking item: {e}")
            conn.rollback()
        finally:
            conn.close()
    return success

# Histori
def get_history():
    conn = create_connection()
    history = []
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT h.date_taken, i.item_name, h.quantity_taken, h.taker_name
                FROM history_log h
                LEFT JOIN items i ON h.item_id = i.item_id
                ORDER BY h.log_id DESC
            """)
            history = cursor.fetchall()
        finally:
            conn.close()
    return history


# Fungsi utama untuk setup awal
if __name__ == '__main__':
    print("Mengecek dan menginisialisasi database...")
    create_tables()
    setup_default_admin()
    print("Setup selesai. Anda bisa menjalankan app.py")