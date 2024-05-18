from datetime import datetime
import sys
import utils

from storage import Database
from order import Order
from report import Report


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

    def print_header(self, choice, section_name):
        print(f"\nCurrent choice: {section_name} ({choice})")
        print("Enter new order details\n")

    def start(self):
        self.print_main_menu()
        self.choice = input("Enter your choice (1-6): ")

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

            self.choice = input("Enter your choice (1-6): ")
        else:
            print("Exiting...")
            sys.exit()

    def insert_order(self):
        self.print_header(1, "INSERT ORDER")
        order_type_input = input("Takeaway ? (Y/N): ").upper()

        order_type = "DINE-IN"

        if order_type_input == "Y":
            order_type = "TAKEAWAY"
        elif order_type_input == "N":
            order_type = "DINE-IN"

        card_number = int(input("Enter card number: "))
        order_items = input("Enter order items: ")
        total_amount_in_RM = float(input("Enter total amount : RM"))
        payment_status = input("Enter payment status (PAID/UNPAID): ").upper()

        total_amount = utils.to_cents(total_amount_in_RM)

        order = Order(order_type, card_number, order_items,
                      total_amount, payment_status)
        self.db.insert_order(order)
        print("Order inserted successfully!")

    def search_order(self):
        self.print_header(2, "SEARCH ORDER")
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
        self.print_header(3, "UPDATE ORDER")
        card_number = int(input("Enter card number: "))

        order_type = "DINE-IN"

        if order_type_input == "Y":
            order_type = "TAKEAWAY"
        elif order_type_input == "N":
            order_type = "DINE-IN"

        order_items = input("Enter new order items: ")
        total_amount_in_RM = float(input("Enter new total amount: RM"))
        payment_status = input(
            "Enter new payment status (PAID/UNPAID): ").upper()

        total_amount = utils.to_cents(total_amount_in_RM)

        order = Order(order_type, card_number, order_items,
                      total_amount, payment_status)
        self.db.update_order(self.db.get_latest_order_id(card_number), order)
        # TODO: delete
        print("Order updated successfully!")

    def delete_order(self):
        self.print_header(4, "DELETE ORDER")
        card_number = int(input("Enter card number: "))
        self.db.delete_order(self.db.get_latest_order_id(card_number))
        # TODO: delete
        print("Order deleted successfully!")

    def print_report(self, orders):
        total_amount = 0
        total_orders = len(orders)

        for order in orders:
            total_amount += order[0]

        print(f"""
        Total orders: {total_orders}
        Total amount: RM{utils.to_RM(total_amount)}
        """)

    def generate_report(self):
        self.print_header(5, "VIEW REPORT")

        today_order = self.db.get_all_order_today()
        today_amount = utils.to_RM(sum([order[0] for order in today_order]))

        this_week_order = self.db.get_all_order_this_week()
        this_week_amount = utils.to_RM(
            sum([order[0] for order in this_week_order]))

        this_month_order = self.db.get_all_order_this_month()
        this_month_amount = utils.to_RM(
            sum([order[0] for order in this_month_order]))

        total_order = self.db.get_all_orders()

        today_date = datetime.now().isoformat()

        report = Report(today_date)
        report.generate_report_today(today_order, today_amount)

    # TODO: delete
    print("Report generated successfully!")


def main():
    app = App()
    app.start()


if __name__ == "__main__":
    main()
