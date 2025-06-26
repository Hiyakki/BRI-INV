# File: database.py (VERSI FINAL dengan Implementasi Lengkap)
import mysql.connector
from mysql.connector import Error
import configparser
import os
import bcrypt
from datetime import datetime
import sys
import logging
import certifi

# --- Fungsi Konfigurasi dan Koneksi ---

def get_base_path():
    """Mendapatkan path dasar aplikasi, baik saat dijalankan sebagai script atau .exe."""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    else:
        return os.path.dirname(os.path.abspath(__file__))

log_file_path = os.path.join(get_base_path(), 'debug_log.txt')
logging.basicConfig(filename=log_file_path, level=logging.INFO, 
                    format='%(asctime)s - %(levelname)s - %(message)s',
                    filemode='w')

def get_config_value(section, key):
    config = configparser.ConfigParser()
    base_path = get_base_path()
    config_file_path = os.path.join(base_path, 'config.ini')
    
    if not os.path.exists(config_file_path):
        error_msg = f"File 'config.ini' tidak ditemukan di path: {config_file_path}"
        logging.error(error_msg)
        raise FileNotFoundError(error_msg)
        
    config.read(config_file_path)
    try:
        return config.get(section, key)
    except (configparser.NoSectionError, configparser.NoOptionError) as e:
        error_msg = f"Konfigurasi tidak ditemukan: {e}"
        logging.error(error_msg)
        raise KeyError(error_msg)

def create_connection():
    """Membuat koneksi ke database MySQL di Aiven."""
    conn = None
    try:
        base_path = get_base_path()
        ssl_ca_path = os.path.join(base_path, 'ca.pem')

        if not os.path.exists(ssl_ca_path):
            error_msg = f"File sertifikat 'ca.pem' tidak ditemukan di: {ssl_ca_path}."
            logging.error(error_msg)
            raise FileNotFoundError(error_msg)

        conn = mysql.connector.connect(
            host=get_config_value('Database', 'Host'),
            user=get_config_value('Database', 'User'),
            password=get_config_value('Database', 'Password'),
            database=get_config_value('Database', 'DatabaseName'),
            port=int(get_config_value('Database', 'Port')),
            ssl_ca=ssl_ca_path,
            ssl_verify_cert=True
        )
    except Error as e:
        logging.error(f"Error connecting to Aiven MySQL database: {e}")
        raise e
    return conn

# --- Fungsi-fungsi Inisialisasi dan CRUD (Implementasi Lengkap) ---

def create_tables():
    try:
        conn = create_connection()
        if not (conn and conn.is_connected()): return
        cursor = conn.cursor()
        cursor.execute("CREATE TABLE IF NOT EXISTS users (user_id INT AUTO_INCREMENT PRIMARY KEY, nama VARCHAR(255) NOT NULL, personal_number VARCHAR(255) UNIQUE NOT NULL, password TEXT NOT NULL, role VARCHAR(50) NOT NULL DEFAULT 'superadmin') ENGINE=InnoDB;")
        cursor.execute("CREATE TABLE IF NOT EXISTS categories (category_id INT AUTO_INCREMENT PRIMARY KEY, category_name VARCHAR(255) UNIQUE NOT NULL) ENGINE=InnoDB;")
        cursor.execute("CREATE TABLE IF NOT EXISTS items (item_id INT AUTO_INCREMENT PRIMARY KEY, item_name VARCHAR(255) NOT NULL, description TEXT, stock INT NOT NULL DEFAULT 0, date_added DATETIME NOT NULL, category_id INT, image_url VARCHAR(255), FOREIGN KEY (category_id) REFERENCES categories(category_id) ON DELETE SET NULL) ENGINE=InnoDB;")
        cursor.execute("CREATE TABLE IF NOT EXISTS history_log (log_id INT AUTO_INCREMENT PRIMARY KEY, item_id INT, taker_name VARCHAR(255) NOT NULL, quantity_taken INT NOT NULL, date_taken DATETIME NOT NULL, FOREIGN KEY (item_id) REFERENCES items(item_id) ON DELETE SET NULL) ENGINE=InnoDB;")
        logging.info("Pengecekan dan pembuatan tabel selesai.")
        conn.commit()
    except (Error, KeyError) as e:
        logging.error(f"Error saat membuat tabel: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def setup_default_admin():
    try:
        conn = create_connection()
        if conn and conn.is_connected():
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users")
            if cursor.fetchone()[0] == 0:
                pn = get_config_value('Admin', 'DefaultPersonalNumber')
                pw = get_config_value('Admin', 'DefaultPassword')
                hashed_pw = bcrypt.hashpw(pw.encode('utf-8'), bcrypt.gensalt())
                query = "INSERT INTO users (nama, personal_number, password, role) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, ('Default Admin', pn, hashed_pw, 'superadmin'))
                conn.commit()
                logging.info("Default admin created successfully.")
    except (Error, KeyError) as e:
        logging.error(f"Error setting up default admin: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def validate_admin(personal_number, password):
    user = None
    try:
        conn = create_connection()
        if conn and conn.is_connected():
            cursor = conn.cursor(dictionary=True)
            cursor.execute("SELECT password FROM users WHERE personal_number = %s", (personal_number,))
            result = cursor.fetchone()
            if result:
                stored_password_hash = result['password'].encode('utf-8')
                if bcrypt.checkpw(password.encode('utf-8'), stored_password_hash):
                    user = True
    except (Error, KeyError) as e:
        logging.error(f"Error dalam validate_admin: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
    return user

def add_category(name):
    try:
        conn = create_connection()
        if conn and conn.is_connected():
            cursor = conn.cursor()
            cursor.execute("INSERT INTO categories (category_name) VALUES (%s)", (name,))
            conn.commit()
    except (Error, KeyError) as e:
        logging.error(f"Error adding category: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def get_all_categories():
    categories = []
    try:
        conn = create_connection()
        if conn and conn.is_connected():
            cursor = conn.cursor()
            cursor.execute("SELECT category_id, category_name FROM categories ORDER BY category_name")
            categories = cursor.fetchall()
    except (Error, KeyError) as e:
        logging.error(f"Error getting categories: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
    return categories

def update_category(cat_id, new_name):
    try:
        conn = create_connection()
        if conn and conn.is_connected():
            cursor = conn.cursor()
            cursor.execute("UPDATE categories SET category_name = %s WHERE category_id = %s", (new_name, cat_id))
            conn.commit()
    except (Error, KeyError) as e:
        logging.error(f"Error updating category: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def delete_category(cat_id):
    try:
        conn = create_connection()
        if conn and conn.is_connected():
            cursor = conn.cursor()
            cursor.execute("UPDATE items SET category_id = NULL WHERE category_id = %s", (cat_id,))
            cursor.execute("DELETE FROM categories WHERE category_id = %s", (cat_id,))
            conn.commit()
    except (Error, KeyError) as e:
        logging.error(f"Error deleting category: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def add_item(name, desc, stock, cat_id, image_url=None):
    try:
        conn = create_connection()
        if conn and conn.is_connected():
            cursor = conn.cursor()
            date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            query = "INSERT INTO items (item_name, description, stock, date_added, category_id, image_url) VALUES (%s, %s, %s, %s, %s, %s)"
            cursor.execute(query, (name, desc, stock, date, cat_id, image_url))
            conn.commit()
    except (Error, KeyError) as e:
        logging.error(f"Error adding item: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def update_item(item_id, name, desc, stock, cat_id, image_url=None):
    try:
        conn = create_connection()
        if conn and conn.is_connected():
            cursor = conn.cursor()
            query = "UPDATE items SET item_name = %s, description = %s, stock = %s, category_id = %s, image_url = %s WHERE item_id = %s"
            cursor.execute(query, (name, desc, stock, cat_id, image_url, item_id))
            conn.commit()
    except (Error, KeyError) as e:
        logging.error(f"Error updating item: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()

def delete_item(item_id):
    try:
        conn = create_connection()
        if conn and conn.is_connected():
            cursor = conn.cursor()
            cursor.execute("DELETE FROM items WHERE item_id = %s", (item_id,))
            conn.commit()
    except (Error, KeyError) as e:
        logging.error(f"Error deleting item: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
    
def take_item(item_id, quantity, taker_name):
    success = False
    try:
        conn = create_connection()
        if conn and conn.is_connected():
            cursor = conn.cursor()
            cursor.execute("SELECT stock FROM items WHERE item_id = %s FOR UPDATE", (item_id,))
            result = cursor.fetchone()
            if result:
                current_stock = result[0]
                if current_stock >= quantity:
                    new_stock = current_stock - quantity
                    cursor.execute("UPDATE items SET stock = %s WHERE item_id = %s", (new_stock, item_id))
                    date_taken = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    query = "INSERT INTO history_log (item_id, taker_name, quantity_taken, date_taken) VALUES (%s, %s, %s, %s)"
                    cursor.execute(query, (item_id, taker_name, quantity, date_taken))
                    conn.commit()
                    success = True
                else:
                    conn.rollback()
    except (Error, KeyError) as e:
        logging.error(f"Error in take_item: {e}")
        if conn and conn.is_connected(): conn.rollback()
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
    return success
    
def get_history():
    history = []
    try:
        conn = create_connection()
        if conn and conn.is_connected():
            cursor = conn.cursor()
            query = "SELECT h.date_taken, i.item_name, h.quantity_taken, h.taker_name FROM history_log h LEFT JOIN items i ON h.item_id = i.item_id ORDER BY h.log_id DESC"
            cursor.execute(query)
            history = cursor.fetchall()
    except (Error, KeyError) as e:
        logging.error(f"Error getting history: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
    return history

def get_history_by_date_range(start_date, end_date):
    history = []
    try:
        end_date_inclusive = f"{end_date} 23:59:59"
        conn = create_connection()
        if conn and conn.is_connected():
            cursor = conn.cursor()
            query = "SELECT h.date_taken, i.item_name, h.quantity_taken, h.taker_name FROM history_log h LEFT JOIN items i ON h.item_id = i.item_id WHERE h.date_taken BETWEEN %s AND %s ORDER BY h.log_id DESC"
            cursor.execute(query, (start_date, end_date_inclusive))
            history = cursor.fetchall()
    except (Error, KeyError) as e:
        logging.error(f"Error getting history by date range: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
    return history

def get_all_items_with_category():
    items = []
    try:
        conn = create_connection()
        if conn and conn.is_connected():
            cursor = conn.cursor()
            query = "SELECT i.item_id, i.item_name, c.category_name, i.stock, i.description, i.date_added, i.image_url FROM items i LEFT JOIN categories c ON i.category_id = c.category_id ORDER BY i.item_name"
            cursor.execute(query)
            items = cursor.fetchall()
    except (Error, KeyError) as e:
        logging.error(f"Error in get_all_items_with_category: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
    return items

def get_items_by_category(category_id):
    items = []
    try:
        conn = create_connection()
        if conn and conn.is_connected():
            cursor = conn.cursor()
            query = "SELECT i.item_id, i.item_name, c.category_name, i.stock, i.description, i.date_added, i.image_url FROM items i LEFT JOIN categories c ON i.category_id = c.category_id WHERE i.category_id = %s ORDER BY i.item_name"
            cursor.execute(query, (category_id,))
            items = cursor.fetchall()
    except (Error, KeyError) as e:
        logging.error(f"Error in get_items_by_category: {e}")
    finally:
        if conn and conn.is_connected():
            cursor.close()
            conn.close()
    return items

if __name__ == '__main__':
    logging.info("Menjalankan database.py secara manual untuk Aiven.")
    print("Mempersiapkan database...")
    create_tables()
    print("Mempersiapkan admin default...")
    setup_default_admin()
    print("Proses selesai.")
