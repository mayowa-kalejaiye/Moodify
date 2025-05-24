from django.apps import AppConfig

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
        pass
