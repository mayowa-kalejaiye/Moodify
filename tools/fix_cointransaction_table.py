#!/usr/bin/env python
"""
Fix the missing balance_after column in tracker_cointransaction table
"""

import sqlite3
import os

def fix_cointransaction_table():
    """Add the missing balance_after column to the CoinTransaction table"""
    db_path = os.path.join('mood_tracker', 'db.sqlite3')
    
    if not os.path.exists(db_path):
        print("❌ Database file not found!")
        return False

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Check current schema
        cursor.execute("PRAGMA table_info(tracker_cointransaction)")
        columns = [col[1] for col in cursor.fetchall()]
        print("Current tracker_cointransaction columns:", columns)
        
        if 'balance_after' not in columns:
            print("Adding missing balance_after column...")
            
            # Add the missing column
            cursor.execute("ALTER TABLE tracker_cointransaction ADD COLUMN balance_after INTEGER DEFAULT 0")
            print("✅ Added balance_after column")
            
            # Also check if challenge column exists (foreign key)
            if 'challenge_id' not in columns:
                cursor.execute("ALTER TABLE tracker_cointransaction ADD COLUMN challenge_id INTEGER")
                print("✅ Added challenge_id column")
            
            conn.commit()
            
            # Verify the update
            cursor.execute("PRAGMA table_info(tracker_cointransaction)")
            new_columns = [col[1] for col in cursor.fetchall()]
            print("Updated tracker_cointransaction columns:", new_columns)
            
            print("\n✅ CoinTransaction table schema fixed!")
            return True
        else:
            print("✅ balance_after column already exists")
            return True
            
    except Exception as e:
        print(f"❌ Error fixing table: {e}")
        conn.rollback()
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    print("Fixing tracker_cointransaction table schema...")
    success = fix_cointransaction_table()
    
    if success:
        print("\n🎉 Fix completed successfully!")
        print("The /api/coins/balance/ endpoint should now work correctly.")
    else:
        print("\n❌ Fix failed!")
