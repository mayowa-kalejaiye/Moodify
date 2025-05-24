import os
import sys
import django

def setup_test_database():
    """Set up a clean test database with the latest schema"""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mood_tracker.mood_tracker.settings')
    django.setup()
    
    # Delete the test database if it exists
    if os.path.exists('db.sqlite3'):
        print("Removing existing database...")
        os.rename('db.sqlite3', 'db.sqlite3.bak')
    
    # Run migrations to create a fresh database
    from django.core.management import call_command
    print("Creating migrations...")
    call_command('makemigrations')
    print("Applying migrations...")
    call_command('migrate')
    
    print("\nDatabase setup complete. You can now run tests.")

if __name__ == "__main__":
    setup_test_database()
