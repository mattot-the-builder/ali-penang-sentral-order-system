import sqlite3
from datetime import datetime


class Database:
    connection = None
    cursor = None

    def __init__(self):
        self.connect()
        self.create_table()

    def connect(self):
        self.connection = sqlite3.connect("penang_sentral.sqlite")
        self.cursor = self.connection.cursor()
        # TODO: delete
        print("connected to database")

    def create_table(self):
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                order_type TEXT CHECK(order_type IN ('DINE-IN', 'TAKEAWAY')),
                card_number INTEGER,
                order_items TEXT,
                total_amount INTEGER,
                payment_status TEXT CHECK(payment_status IN ('PAID', 'UNPAID')),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        # TODO: delete
        print("table created")

    def insert_order(self, order):
        current_timestamp = datetime.now().isoformat()
        self.cursor.execute("""
            INSERT INTO orders (order_type, card_number, order_items, total_amount, payment_status, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (order.order_type, order.card_number, order.order_items, order.total_amount, order.payment_status, current_timestamp, current_timestamp))
        self.connection.commit()
        # TODO: delete
        print("order inserted")

    def search_order(self, card_number):
        self.cursor.execute("""
            SELECT * FROM orders
            WHERE card_number = ?
        """, (card_number,))
        return self.cursor.fetchall()

    def update_order(self, order_id, order):
        current_timestamp = datetime.now().isoformat()
        self.cursor.execute("""
            UPDATE orders
            SET order_items = ?, total_amount = ?, payment_status = ?, updated_at = ?
            WHERE id = ?
        """, (order.order_items, order.total_amount, order.payment_status, current_timestamp, order_id))
        self.connection.commit()
        # TODO: delete
        print("order updated")

    def delete_order(self, order_id):
        self.cursor.execute("""
            DELETE FROM orders
            WHERE id = ?
        """, (order_id,))
        self.connection.commit()
        # TODO: delete
        print("order deleted")

    def get_latest_order_id(self, card_number):
        self.cursor.execute("""
            SELECT id FROM orders
            WHERE card_number = ?
            ORDER BY created_at DESC
            LIMIT 1
        """, (card_number,))
        return self.cursor.fetchone()[0]

    def get_all_orders(self):
        self.cursor.execute("""
            SELECT total_amount FROM orders
        """)
        return self.cursor.fetchall()

    def get_all_order_today(self):
        self.cursor.execute("""
            SELECT total_amount FROM orders
            WHERE DATE(created_at) = DATE('now')
        """)
        return self.cursor.fetchall()

    def get_all_order_this_week(self):
        self.cursor.execute("""
            SELECT total_amount FROM orders
            WHERE strftime('%W', created_at) = strftime('%W', 'now')
        """)
        return self.cursor.fetchall()

    def get_all_order_this_month(self):
        self.cursor.execute("""
            SELECT total_amount FROM orders
            WHERE strftime('%m', created_at) = strftime('%m', 'now')
        """)
        return self.cursor.fetchall()

    def get_unpaid_orders(self):
        self.cursor.execute("""
            SELECT total_amount FROM orders
            WHERE payment_status = 'UNPAID'
        """)
        return self.cursor.fetchall()
