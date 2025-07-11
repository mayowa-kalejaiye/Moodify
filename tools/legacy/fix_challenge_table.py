#!/usr/bin/env python
"""
Fix the tracker_challenge table schema to match the Django model
"""

import sqlite3
import os

def fix_challenge_table():
    """Fix the Challenge table schema to match the Django model exactly"""
    db_path = os.path.join('mood_tracker', 'db.sqlite3')
    
    if not os.path.exists(db_path):
        print("❌ Database file not found!")
        return False

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check current schema
        cursor.execute("PRAGMA table_info(tracker_challenge)")
        columns = [col[1] for col in cursor.fetchall()]
        print("Current tracker_challenge columns:", columns)
        
        # Add missing settled column
        if 'settled' not in columns:
            print("Adding missing settled column...")
            cursor.execute("ALTER TABLE tracker_challenge ADD COLUMN settled BOOLEAN DEFAULT 0")
            print("✅ Added settled column")
        else:
            print("✅ settled column already exists")
        
        # The model doesn't actually have title and description fields,
        # but they exist in the database. We'll leave them for now to avoid data loss.
        # They can be safely ignored by Django if they're not in the model.
        
        conn.commit()
        
        # Verify the update
        cursor.execute("PRAGMA table_info(tracker_challenge)")
        new_columns = [col[1] for col in cursor.fetchall()]
        print("Updated tracker_challenge columns:", new_columns)
        
        print("\n✅ Challenge table schema fixed!")
        
        # Test basic operation
        cursor.execute("SELECT COUNT(*) FROM tracker_challenge")
        count = cursor.fetchone()[0]
        print(f"✅ Challenge table accessible ({count} records)")
        
        return True
            
    except Exception as e:
        print(f"❌ Error fixing table: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    print("Fixing tracker_challenge table schema...")
    success = fix_challenge_table()
    
    if success:
        print("\n🎉 Fix completed successfully!")
        print("The /api/coins/stake/ endpoint should now work correctly.")
    else:
        print("\n❌ Fix failed!")
