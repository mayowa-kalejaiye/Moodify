from django.apps import AppConfig
import logging

logger = logging.getLogger(__name__)

class TrackerConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'mood_tracker.tracker'
    
    def ready(self):
        """
        Initialize app when it's ready.
        Import signals or perform other initialization here.
        """
        # Uncomment if you have signals to import
        # import mood_tracker.tracker.signals
        
        # Start the keep-alive service for production
        try:
            from .keep_alive_service import start_keep_alive_service
            start_keep_alive_service(ping_interval_minutes=10)
            logger.info("Keep-alive service initialization completed")
        except Exception as e:
            logger.error(f"Failed to start keep-alive service: {e}")
