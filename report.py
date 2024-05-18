from datetime import datetime
import utils


class Report:
    today_date = None
    today_order = None
    today_amount = None
    this_week_order = None
    this_week_amount = None
    this_month_order = None
    this_month_amount = None

    def __init__(self, today_date):
        self.today_date = today_date

    def parse_date(self, date):
        parsed_date = datetime.fromisoformat(date)

        formatted_time = parsed_date.strftime("%I.%M%p").lower().replace(
            "am", " am").replace("pm", " pm")
        formatted_date = parsed_date.strftime("%-d %B %Y")

        return (formatted_date, formatted_time)

    def generate_report_today(self, today_order, today_amount):
        self.today_order = len(today_order)
        self.today_amount = today_amount

        today_date_formatted = self.parse_date(self.today_date)[0]
        time_generated_formatted = self.parse_date(self.today_date)[1]

        print(f"""
--------------------------------------------------

        PENANG SENTRAL RESTAURANT
        Sales Report

        Date : {today_date_formatted}
        Generated at : {time_generated_formatted}

        Total Orders: {self.today_order}
        Amount: RM{self.today_amount}

--------------------------------------------------
        """)
