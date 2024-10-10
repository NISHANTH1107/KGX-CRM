import pandas as pd
from django.utils import timezone
from apscheduler.schedulers.background import BackgroundScheduler
from django_apscheduler.jobstores import DjangoJobStore
from .models import Wifi
import os
from django.conf import settings

def generate_wifi_report():
    from .models import Wifi  # Move import here
    
    # Get today's date
    today = timezone.now().date()
    entries = Wifi.objects.filter(submitted_at__date=today)

    # Create a DataFrame if there are entries
    if entries.exists():
        data = []
        for entry in entries:
            data.append({
                'Roll No': entry.roll_no.roll_no,
                'MAC Address': entry.mac_address,
                'Screenshot': entry.screenshot.url if entry.screenshot else '',
                'Submitted At': entry.submitted_at,
            })

        df = pd.DataFrame(data)

        # Define the output directory for the report
        report_dir = os.path.join(settings.MEDIA_ROOT, 'reports')
        os.makedirs(report_dir, exist_ok=True)  # Create directory if it doesn't exist

        # Save the DataFrame to an Excel file
        excel_filename = os.path.join(report_dir, f'wifi_report_{today}.xlsx')
        df.to_excel(excel_filename, index=False, engine='openpyxl')

        print(f"Report generated: {excel_filename}")
    else:
        print("No entries for today to generate a report.")

def start_scheduler():
    scheduler = BackgroundScheduler()
    scheduler.add_jobstore(DjangoJobStore(), "default")

    # Schedule the job to run every day at midnight
    scheduler.add_job(generate_wifi_report, 'cron', hour=0, minute=0, id='wifi_report_job', replace_existing=True)

    scheduler.start()
