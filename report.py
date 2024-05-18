from datetime import datetime


class Report:
    today_date = None
    today_order = None
    today_amount = None
    file_path = None

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

        self.file_path = f"reports/report - {today_date_formatted} - {
            time_generated_formatted}.txt"

        formatted_result = f"""
--------------------------------------------------

        PENANG SENTRAL RESTAURANT
        Today Sales Report

        Date : {today_date_formatted}
        Generated at : {time_generated_formatted}

        Total Orders: {self.today_order}
        Amount: RM{self.today_amount}

--------------------------------------------------
        """

        print(formatted_result)

        export_status = input("Export to text file ? (Y/N): ").upper()
        if export_status == "Y":
            self.export_to_file(self.file_path, formatted_result)

    def export_to_file(self, file_path, data):
        with open(file_path, "x") as file:
            file.write(data)
