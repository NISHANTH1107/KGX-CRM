from django.core.management.base import BaseCommand
from kgx_app.models import Holiday  # Import the Holiday model here
import kgx_app.generate_pdf
import kgx_app.email_service
from kgx_app.utils import generate_wifi_report
from django.utils import timezone
import pytz
from datetime import timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger


class Command(BaseCommand):
    help = 'Run scheduled jobs to process holidays and WiFi reports'

    def get_ist_now(self):
        ist = pytz.timezone('Asia/Kolkata')
        return timezone.now().astimezone(ist)

    def is_tomorrow_public_holiday(self):
        public_holidays = [
            "2024-01-01", "2024-10-18",  # Add all relevant dates
        ]
        ist_now = self.get_ist_now()
        tomorrow = ist_now.date() + timedelta(days=1)
        tomorrow_str = tomorrow.strftime('%Y-%m-%d')
        return tomorrow_str in public_holidays

    def job_holiday_email(self):
        self.stdout.write("Holiday email job started")
        if self.is_tomorrow_public_holiday():
            self.stdout.write("Tomorrow is a public holiday")
            ist_now = self.get_ist_now()
            today = ist_now.date()
            data = Holiday.objects.filter(date_submitted__date=today)
            if data.exists():
                self.stdout.write("Records exist. Generating PDF and sending holiday email.")
                pdf_filename = kgx_app.generate_pdf.generate_pdf(data)
                kgx_app.email_service.send_email(pdf_filename)
            else:
                self.stdout.write("No holiday records found for today.")
        else:
            self.stdout.write("Tomorrow is not a public holiday.")

    def job_wifi_report(self):
        self.stdout.write("WiFi report job started")
        pdf_filename = generate_wifi_report()
        kgx_app.email_service.send_email(pdf_filename)

    def handle(self, *args, **options):
        self.stdout.write("Starting the scheduler...")

        # Initialize the background scheduler
        scheduler = BackgroundScheduler(timezone="Asia/Kolkata")

        # Schedule the holiday email job at 12:00 AM every day
        scheduler.add_job(
            self.job_holiday_email,
            trigger=CronTrigger(hour=0, minute=0),
            id='holiday_email_job',
            replace_existing=True
        )

        # Schedule the WiFi report job at 12:30 AM every day
        scheduler.add_job(
            self.job_wifi_report,
            trigger=CronTrigger(hour=0, minute=30),
            id='wifi_report_job',
            replace_existing=True
        )

        scheduler.start()
        self.stdout.write("Scheduler started with holiday and WiFi report jobs.")

        try:
            # Keep the command running to allow the scheduler to run
            while True:
                pass
        except (KeyboardInterrupt, SystemExit):
            scheduler.shutdown()
            self.stdout.write("Scheduler stopped.")
