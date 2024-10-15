from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
import pytz  # type: ignore
import os
import schedule
import time
from kgx_app.models import Holiday, Wifi  # Assuming Wifi model is imported
import kgx_app.generate_pdf
import kgx_app.email_service
from kgx_app.utils import generate_wifi_report  # Correctly import the function from utils.py
LOCK_FILE = "scheduler.lock"

class Command(BaseCommand):
    help = 'Run scheduled jobs to process holidays and WiFi reports'

    def get_ist_now(self):
        ist = pytz.timezone('Asia/Kolkata')
        return timezone.now().astimezone(ist)

    def is_tomorrow_public_holiday(self):
        public_holidays = [
            "2024-01-01", "2024-06-14", "2024-01-14", "2024-01-26", "2024-04-12",
            "2024-04-14", "2024-05-01", "2024-08-15", "2024-08-23", "2024-10-02",
            "2024-10-22", "2024-12-25", "2024-01-07", "2024-01-14", "2024-01-21",
            "2024-01-28", "2024-02-04", "2024-02-11", "2024-02-18", "2024-02-25",
            "2024-03-03", "2024-03-10", "2024-03-17", "2024-03-24", "2024-03-31",
            "2024-04-07", "2024-04-14", "2024-04-21", "2024-04-28", "2024-05-05",
            "2024-05-12", "2024-05-19", "2024-05-26", "2024-06-02", "2024-06-09",
            "2024-06-16", "2024-06-23", "2024-06-30", "2024-07-07", "2024-07-14",
            "2024-07-21", "2024-07-28", "2024-08-04", "2024-08-11", "2024-08-18",
            "2024-08-25", "2024-09-01", "2024-09-08", "2024-09-15", "2024-09-22",
            "2024-09-29", "2024-10-06", "2024-10-13", "2024-10-20", "2024-10-27",
            "2024-11-03", "2024-11-10", "2024-11-17", "2024-11-24", "2024-12-01",
            "2024-12-08", "2024-12-15", "2024-12-22", "2024-12-29", "2024-10-14"
        ]
        ist_now = self.get_ist_now()
        tomorrow = ist_now.date() + timedelta(days=1)
        tomorrow_str = tomorrow.strftime('%Y-%m-%d')
        self.stdout.write(f"Checking if {tomorrow_str} is a public holiday")
        return tomorrow_str in public_holidays

    def create_lock_file(self):
        with open(LOCK_FILE, 'w') as f:
            f.write("This file prevents multiple executions of the job.")
        self.stdout.write(f"Lock file created: {LOCK_FILE}")

    def remove_lock_file(self):
        if os.path.exists(LOCK_FILE):
            os.remove(LOCK_FILE)
            self.stdout.write(f"Lock file removed: {LOCK_FILE}")

    def job_holiday_email(self):
        self.stdout.write("Holiday email job started")

        if os.path.exists(LOCK_FILE):
            self.stdout.write("Lock file exists. Exiting to prevent duplicate execution.")
            return

        self.create_lock_file()
        try:
            if self.is_tomorrow_public_holiday():
                self.stdout.write("Tomorrow is a public holiday")

                ist_now = self.get_ist_now()
                today = ist_now.date()
                self.stdout.write(f"Today is {today}")

                data = Holiday.objects.filter(date_submitted__date=today)
                self.stdout.write(f"Found {data.count()} holiday records for today")

                if data.exists(): 
                    self.stdout.write("Records exist. Generating PDF and sending holiday email.")
                    pdf_filename = kgx_app.generate_pdf.generate_pdf(data)
                    kgx_app.email_service.send_email(pdf_filename)
                else:
                    self.stdout.write("No holiday records found for today.")
            else:
                self.stdout.write("Tomorrow is not a public holiday.")
        finally:
            self.remove_lock_file()

    def job_wifi_report(self):
        self.stdout.write("WiFi report job started")

        if os.path.exists(LOCK_FILE):
            self.stdout.write("Lock file exists. Exiting to prevent duplicate execution.")
            return

        self.create_lock_file()
        try:
            ist_now = self.get_ist_now()
            today = ist_now.date()
            self.stdout.write(f"Generating WiFi report for today: {today}")

            # Generate the WiFi report for today
            pdf_filename = generate_wifi_report()
            kgx_app.email_service.send_email(pdf_filename)

        finally:
            self.remove_lock_file()

    def handle(self, *args, **options):
        # Schedule holiday email job for the day before at 10 PM
        schedule.every().day.at("23:45").do(self.job_holiday_email)

        # Schedule WiFi report job for every day at 12 AM
        schedule.every().day.at("23:45").do(self.job_wifi_report)

        self.stdout.write("Scheduled jobs for holiday emails at 10 PM and WiFi reports at 12 AM")

        while True:
            schedule.run_pending()
            time.sleep(1)
