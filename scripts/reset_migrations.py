import os
import django
from pathlib import Path

def reset_migrations():
    """Reset migrations completely"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mood_tracker.mood_tracker.settings')
    django.setup()
    
    # Delete all migration files except __init__.py
    migrations_dir = Path('mood_tracker/tracker/migrations')
    for migration_file in migrations_dir.glob('*.py'):
        if migration_file.name != '__init__.py':
            print(f"Deleting: {migration_file}")
            migration_file.unlink()
    
    # Delete database
    db_file = Path('db.sqlite3')
    if db_file.exists():
        print("Deleting database...")
        db_file.unlink()
    
    # Create fresh migrations
    from django.core.management import call_command
    
    print("Creating fresh migrations...")
    call_command('makemigrations', 'tracker')
    
    print("Applying migrations...")
    call_command('migrate')
    
    print("Creating superuser...")
    call_command('createsuperuser', '--noinput', 
                 username='admin', 
                 email='admin@example.com')
    
    print("Reset complete!")

if __name__ == "__main__":
    reset_migrations()
