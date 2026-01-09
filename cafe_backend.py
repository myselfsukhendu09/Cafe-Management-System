import sqlite3
from datetime import datetime

class CafeBackend:
    def __init__(self, db_name="cafe.db"):
        self.db_name = db_name
        self.init_db()

    def init_db(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            # Menu Table
            cursor.execute('''CREATE TABLE IF NOT EXISTS menu (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                name TEXT NOT NULL,
                                price REAL NOT NULL,
                                category TEXT
                            )''')
            # Orders Table
            cursor.execute('''CREATE TABLE IF NOT EXISTS orders (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                total REAL DEFAULT 0,
                                timestamp TEXT,
                                status TEXT DEFAULT 'Completed'
                            )''')
            # Order Items Table
            cursor.execute('''CREATE TABLE IF NOT EXISTS order_items (
                                id INTEGER PRIMARY KEY AUTOINCREMENT,
                                order_id INTEGER,
                                menu_id INTEGER,
                                quantity INTEGER,
                                subtotal REAL,
                                FOREIGN KEY(order_id) REFERENCES orders(id),
                                FOREIGN KEY(menu_id) REFERENCES menu(id)
                            )''')
            
            # Seed menu if empty
            cursor.execute("SELECT COUNT(*) FROM menu")
            if cursor.fetchone()[0] == 0:
                items = [
                    ('Espresso', 2.50, 'Coffee'),
                    ('Cappuccino', 3.50, 'Coffee'),
                    ('Latte', 3.75, 'Coffee'),
                    ('Blueberry Muffin', 2.95, 'Bakery'),
                    ('Croissant', 2.50, 'Bakery'),
                    ('Green Tea', 2.25, 'Tea')
                ]
                cursor.executemany("INSERT INTO menu (name, price, category) VALUES (?, ?, ?)", items)
            conn.commit()

    def get_menu(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.execute("SELECT * FROM menu")
            return cursor.fetchall()

    def add_menu_item(self, name, price, category):
        with sqlite3.connect(self.db_name) as conn:
            conn.execute("INSERT INTO menu (name, price, category) VALUES (?, ?, ?)", (name, price, category))
            return True, "Item added to menu!"

    def create_order(self, items):
        """items: list of (menu_id, quantity)"""
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.cursor()
            # Create order record
            cursor.execute("INSERT INTO orders (timestamp) VALUES (?)", (datetime.now().strftime("%Y-%m-%d %H:%M:%S"),))
            order_id = cursor.lastrowid
            
            total = 0
            for menu_id, qty in items:
                cursor.execute("SELECT price FROM menu WHERE id = ?", (menu_id,))
                price = cursor.fetchone()[0]
                subtotal = price * qty
                total += subtotal
                cursor.execute("INSERT INTO order_items (order_id, menu_id, quantity, subtotal) VALUES (?, ?, ?, ?)",
                               (order_id, menu_id, qty, subtotal))
            
            cursor.execute("UPDATE orders SET total = ? WHERE id = ?", (total, order_id))
            conn.commit()
            return order_id, total

    def get_orders(self):
        with sqlite3.connect(self.db_name) as conn:
            cursor = conn.execute("SELECT * FROM orders ORDER BY id DESC")
            return cursor.fetchall()

    def get_order_details(self, order_id):
        with sqlite3.connect(self.db_name) as conn:
            query = '''SELECT m.name, i.quantity, i.subtotal 
                       FROM order_items i 
                       JOIN menu m ON i.menu_id = m.id 
                       WHERE i.order_id = ?'''
            cursor = conn.execute(query, (order_id,))
            return cursor.fetchall()

    def get_analytics(self):
        with sqlite3.connect(self.db_name) as conn:
            # Sales by Category
            cursor = conn.execute('''SELECT m.category, SUM(i.subtotal) 
                                   FROM order_items i 
                                   JOIN menu m ON i.menu_id = m.id 
                                   GROUP BY m.category''')
            return cursor.fetchall()
