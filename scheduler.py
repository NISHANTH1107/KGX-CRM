import sys
import os
import django
import schedule
import time
from datetime import datetime, timedelta
import logging
from kgx_app.models import Holiday
import kgx_app.generate_pdf
import kgx_app.email_service

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

LOCK_FILE = "scheduler.lock"

def is_tomorrow_public_holiday():
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
        "2024-12-08", "2024-12-15", "2024-12-22", "2024-12-29", "2024-08-21"
    ]
    tomorrow = datetime.now().date() + timedelta(days=1)
    return tomorrow.strftime('%Y-%m-%d') in public_holidays

def create_lock_file():
    with open(LOCK_FILE, 'w') as f:
        f.write("This file prevents multiple executions of the job.")
    logging.info("Lock file created.")

def remove_lock_file():
    if os.path.exists(LOCK_FILE):
        os.remove(LOCK_FILE)
        logging.info("Lock file removed.")

def job():
    logging.info("Job started.")
    if os.path.exists(LOCK_FILE):
        logging.warning("Lock file exists. Exiting to prevent duplicate execution.")
        return

    create_lock_file()
    try:
        if is_tomorrow_public_holiday():
            logging.info("Tomorrow is a public holiday.")
            today = datetime.now().date()
            data = Holiday.objects.filter(date=today)
            logging.info(f"Found {data.count()} holiday records for today.")
            if data.exists():
                pdf_filename = kgx_app.generate_pdf.generate_pdf(data)
                kgx_app.email_service.send_email(pdf_filename)
        else:
            logging.info("Tomorrow is not a public holiday.")
    finally:
        remove_lock_file()

# Schedule the job to run daily at a specific time
schedule_time = "11:48"  # Set the time you want the job to run in HH:MM format
schedule.every().day.at(schedule_time).do(job)

if __name__ == "__main__":
    logging.info("Scheduler started.")
    while True:
        schedule.run_pending()
        time.sleep(1)
