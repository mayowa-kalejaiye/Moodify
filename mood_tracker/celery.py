"""
Celery configuration for MoodSync Behavior Engine
"""
from celery import Celery
from celery.schedules import crontab
import os

# Set the default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mood_tracker.settings')

# Create Celery app
app = Celery('mood_tracker')

# Configure Celery using Django settings
app.config_from_object('django.conf:settings', namespace='CELERY')

# Auto-discover tasks from all registered Django apps
app.autodiscover_tasks()

# Celery Beat Schedule for Behavior Engine
app.conf.beat_schedule = {
    'streak-evaluator': {
        'task': 'mood_tracker.tracker.tasks.streak_evaluator_task',
        'schedule': crontab(hour=1, minute=0),  # Daily at 1:00 AM
    },
    'challenge-settler': {
        'task': 'mood_tracker.tracker.tasks.challenge_settler_task',
        'schedule': crontab(minute=0),  # Every hour
    },
    'generate-nudges': {
        'task': 'mood_tracker.tracker.tasks.generate_contextual_nudges_task',
        'schedule': crontab(hour='*/6'),  # Every 6 hours
    },
}

app.conf.timezone = 'UTC'

@app.task(bind=True)
def debug_task(self):
    print(f'Request: {self.request!r}')
