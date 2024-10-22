from django.apps import AppConfig
import logging
import os

logger = logging.getLogger(__name__)

class KgxAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'kgx_app'

    def ready(self):
        # Ensure the scheduler starts only once (in the main process)
        if os.environ.get('RUN_MAIN', None) != 'true':
            from kgx_app.scheduler import start_scheduler

            try:
                # Start the scheduler when the application is ready
                start_scheduler()
                logger.info("Scheduler started successfully.")
            except Exception as e:
                logger.error(f"Error starting the scheduler: {e}")
