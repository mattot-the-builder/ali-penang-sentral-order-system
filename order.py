import utils
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
        Total amount: RM{utils.to_RM(self.total_amount)}
        Payment status: {self.payment_status}
        Created at: {datetime.fromisoformat(self.created_at).strftime("%-I.%M%p %d-%-m-%Y").lower()}
        Updated at: {datetime.fromisoformat(self.updated_at).strftime("%-I.%M%p %d-%-m-%Y").lower()}
        """)
