from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.cron import CronTrigger
from django.conf import settings
from kgx_app.management.commands.run_scheduled_job import Command
import logging

logger = logging.getLogger(__name__)

def start_scheduler():
    # Initialize the scheduler
    scheduler = BackgroundScheduler(timezone=settings.TIME_ZONE)

    # Add the holiday email job
    scheduler.add_job(
        Command().job_holiday_email,
        trigger=CronTrigger(hour=10, minute=26),
        id='holiday_email_job',
        replace_existing=True
    )

    # Add the WiFi report job
    scheduler.add_job(
        Command().job_wifi_report,
        trigger=CronTrigger(hour=10, minute=25),
        id='wifi_report_job',
        replace_existing=True
    )

    # Start the scheduler
    scheduler.start()
    logger.info("Scheduler started with holiday and WiFi report jobs.")

    # Shut down the scheduler when the application stops
    from apscheduler.events import EVENT_SCHEDULER_SHUTDOWN

    def shutdown(event):
        logger.info("Scheduler shut down.")

    scheduler.add_listener(shutdown, EVENT_SCHEDULER_SHUTDOWN)
