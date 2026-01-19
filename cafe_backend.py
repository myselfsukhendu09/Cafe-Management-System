
import sqlite3
import pandas as pd

def init_db():
    conn = sqlite3.connect('cafe.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS menu 
                 (id INTEGER PRIMARY KEY AUTO_INCREMENT, name TEXT, category TEXT, price REAL)''')
    c.execute('''CREATE TABLE IF NOT EXISTS orders 
                 (id INTEGER PRIMARY KEY AUTO_INCREMENT, items TEXT, total REAL, timestamp DATETIME DEFAULT CURRENT_TIMESTAMP)''')
    
    # Add dummy menu if empty
    c.execute("SELECT count(*) FROM menu")
    if c.fetchone()[0] == 0:
        menu_items = [
            ('Espresso', 'Coffee', 120),
            ('Cappuccino', 'Coffee', 180),
            ('Latte', 'Coffee', 200),
            ('Sandwich', 'Snacks', 150),
            ('Muffin', 'Bakery', 90),
            ('Green Tea', 'Tea', 100)
        ]
        c.executemany("INSERT INTO menu (name, category, price) VALUES (?, ?, ?)", menu_items)
    conn.commit()
    conn.close()

def get_menu():
    conn = sqlite3.connect('cafe.db')
    df = pd.read_sql_query("SELECT * FROM menu", conn)
    conn.close()
    return df

def place_order(items_str, total):
    conn = sqlite3.connect('cafe.db')
    c = conn.cursor()
    c.execute("INSERT INTO orders (items, total) VALUES (?, ?)", (items_str, total))
    conn.commit()
    conn.close()

def get_orders():
    conn = sqlite3.connect('cafe.db')
    df = pd.read_sql_query("SELECT * FROM orders", conn)
    conn.close()
    return df
