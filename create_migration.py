import os
import django
import sys

def create_migration():
    """Create a migration for the activities field"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mood_tracker.mood_tracker.settings')
    django.setup()
    
    # Generate the migration
    from django.core.management import call_command
    call_command('makemigrations', 'tracker')
    print("Migration created. Now apply it with: python manage.py migrate")
    
if __name__ == "__main__":
    create_migration()
