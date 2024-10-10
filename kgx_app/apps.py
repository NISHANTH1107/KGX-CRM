from django.apps import AppConfig
import threading 

class KgxAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'kgx_app'

    def ready(self):
        from .utils import start_scheduler
        start_scheduler()