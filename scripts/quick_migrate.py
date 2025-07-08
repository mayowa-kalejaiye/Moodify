#!/usr/bin/env python
"""Quick migration script to fix database schema"""

import os
import sys

# Add the project directory to Python path
sys.path.insert(0, os.path.abspath('.'))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mood_tracker.mood_tracker.settings')

# Setup Django
import django
django.setup()

# Now run the migration
from django.core.management import call_command

try:
    print("Running migrations...")
    call_command('migrate', verbosity=2)
    print("Migrations completed successfully!")
except Exception as e:
    print(f"Error running migrations: {e}")
    
    # Try to manually apply the behavior engine migration
    print("Attempting to manually apply migration...")
    from django.db import connection
    
    # Get the SQL from our migration
    cursor = connection.cursor()
    
    # Add the missing columns to the profile table
    try:
        cursor.execute("ALTER TABLE tracker_profile ADD COLUMN coin_balance INTEGER DEFAULT 0")
        print("Added coin_balance column")
    except Exception as e:
        print(f"coin_balance column might already exist: {e}")
    
    try:
        cursor.execute("ALTER TABLE tracker_profile ADD COLUMN clarity_score INTEGER DEFAULT 100")
        print("Added clarity_score column")
    except Exception as e:
        print(f"clarity_score column might already exist: {e}")
    
    try:
        cursor.execute("ALTER TABLE tracker_profile ADD COLUMN streak_count INTEGER DEFAULT 0")
        print("Added streak_count column")
    except Exception as e:
        print(f"streak_count column might already exist: {e}")
        
    try:
        cursor.execute("ALTER TABLE tracker_profile ADD COLUMN last_mood_log DATE")
        print("Added last_mood_log column")
    except Exception as e:
        print(f"last_mood_log column might already exist: {e}")
        
    try:
        cursor.execute("ALTER TABLE tracker_profile ADD COLUMN streak_last_updated DATE")
        print("Added streak_last_updated column")
    except Exception as e:
        print(f"streak_last_updated column might already exist: {e}")
    
    # Create the new tables
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tracker_challenge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                profile_id INTEGER NOT NULL,
                challenge_type VARCHAR(50) NOT NULL,
                title VARCHAR(200) NOT NULL,
                description TEXT NOT NULL,
                stake INTEGER NOT NULL,
                start_date DATE NOT NULL,
                end_date DATE NOT NULL,
                completed BOOLEAN NOT NULL DEFAULT 0,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (profile_id) REFERENCES tracker_profile(id)
            )
        """)
        print("Created tracker_challenge table")
    except Exception as e:
        print(f"Error creating challenge table: {e}")
    
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tracker_cointransaction (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                profile_id INTEGER NOT NULL,
                transaction_type VARCHAR(50) NOT NULL,
                amount INTEGER NOT NULL,
                description TEXT NOT NULL,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (profile_id) REFERENCES tracker_profile(id)
            )
        """)
        print("Created tracker_cointransaction table")
    except Exception as e:
        print(f"Error creating coin transaction table: {e}")
    
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tracker_nudge (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                profile_id INTEGER NOT NULL,
                nudge_type VARCHAR(50) NOT NULL,
                message TEXT NOT NULL,
                tone VARCHAR(50) NOT NULL DEFAULT 'neutral',
                viewed BOOLEAN NOT NULL DEFAULT 0,
                created_at TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (profile_id) REFERENCES tracker_profile(id)
            )
        """)
        print("Created tracker_nudge table")
    except Exception as e:
        print(f"Error creating nudge table: {e}")
    
    print("Manual migration completed!")
