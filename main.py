import sqlite3
import sys
from datetime import datetime


class Order:
    id = None
    order_type = None
    card_number = None
    order_items = None
    total_amount = None
    payment_status = None
    created_at = None
    updated_at = None

    def __init__(self, order_type, card_number, order_items, total_amount, payment_status):
        self.order_type = order_type
        self.card_number = card_number
        self.order_items = order_items
        self.total_amount = total_amount
        self.payment_status = payment_status

    def print_order(self):
        print(f"""
        Order ID: {self.id}
        Order type: {self.order_type}
        Card number: {self.card_number}
        Order items: {self.order_items}
        Total amount: RM{round(self.total_amount / 100, 2)}
        Payment status: {self.payment_status}
        Created at: {datetime.fromisoformat(self.created_at).strftime("%-I.%M%p %d-%-m-%Y").lower()}
        Updated at: {datetime.fromisoformat(self.updated_at).strftime("%-I.%M%p %d-%-m-%Y").lower()}
        """)


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
                order_type TEXT CHECK(order_type IN ('TAKEOUT', 'DELIVERY')),
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


class App:
    db = None
    choice = None

    def __init__(self):
        self.db = Database()

    def print_main_menu(self):
        print("""
        Penang Sentral Ordering System

        1. Insert Order
        2. Search Order
        3. Update Order
        4. Delete Order
        5. Generate Report
        6. Exit

        """)

    def start(self):
        self.print_main_menu()
        self.choice = input("Enter your choice: ")

        while (self.choice != "6"):

            if self.choice == "1":
                self.insert_order()
            elif self.choice == "2":
                self.search_order()
            elif self.choice == "3":
                self.update_order()
            elif self.choice == "4":
                self.delete_order()
            elif self.choice == "5":
                self.generate_report()
            else:
                print("Invalid choice. Please try again.")

            self.print_main_menu()

            self.choice = input("Enter your choice: ")
        else:
            print("Exiting...")
            sys.exit()

    def insert_order(self):
        print("\nCurrent choice: INSERT ORDER (2)")
        print("Enter order details\n")
        order_type = input("Enter order type (TAKEOUT/DELIVERY): ").upper()
        card_number = int(input("Enter card number: "))
        order_items = input("Enter order items: ")
        total_amount_in_RM = float(input("Enter total amount : RM"))
        payment_status = input("Enter payment status (PAID/UNPAID): ").upper()

        total_amount = total_amount_in_RM * 100

        order = Order(order_type, card_number, order_items,
                      total_amount, payment_status)
        self.db.insert_order(order)
        print("Order inserted successfully!")

    def search_order(self):
        card_number = int(input("Enter card number: "))
        search_result = self.db.search_order(card_number)

        # TODO: call print_order()
        for result in search_result:
            order = Order(result[1], result[2],
                          result[3], result[4], result[5])
            order.id = result[0]
            order.created_at = result[6]
            order.updated_at = result[7]
            order.print_order()
        return search_result

    def update_order(self):
        print("\nCurrent choice: INSERT ORDER (2)")
        print("Enter new order details\n")
        card_number = int(input("Enter card number: "))
        order_type = input("Enter new order type (TAKEOUT/DELIVERY): ").upper()
        order_items = input("Enter new order items: ")
        total_amount_in_RM = float(input("Enter new total amount: RM"))
        payment_status = input(
            "Enter new payment status (PAID/UNPAID): ").upper()

        total_amount = total_amount_in_RM * 100

        order = Order(order_type, card_number, order_items,
                      total_amount, payment_status)
        self.db.update_order(self.db.get_latest_order_id(card_number), order)
        # TODO: delete
        print("Order updated successfully!")

    def delete_order(self):
        card_number = int(input("Enter card number: "))
        self.db.delete_order(self.db.get_latest_order_id(card_number))
        # TODO: delete
        print("Order deleted successfully!")

    def generate_report(self):
        pass


def main():
    app = App()
    app.start()


if __name__ == "__main__":
    main()
