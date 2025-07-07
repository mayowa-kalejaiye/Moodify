import os
import django
import sys
from pathlib import Path

def fix_migrations():
    """Fix migration issues and create proper migrations"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mood_tracker.mood_tracker.settings')
    django.setup()
    
    # Delete the problematic migration file
    problematic_migration = Path('mood_tracker/tracker/migrations/000X_ai_feedback.py')
    if problematic_migration.exists():
        print(f"Deleting problematic migration: {problematic_migration}")
        problematic_migration.unlink()
    
    # Create new migrations
    from django.core.management import call_command
    
    print("Creating new migrations...")
    call_command('makemigrations', 'tracker', '--name', 'add_ai_feedback_model')
    
    print("Applying migrations...")
    call_command('migrate')
    
    print("Migration fix complete!")

if __name__ == "__main__":
    fix_migrations()
