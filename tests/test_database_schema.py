#!/usr/bin/env python
"""
Simple test to verify database schema is correct
"""

import sqlite3
import os

def test_database_schema():
    """Test that the database schema has been updated correctly"""
    db_path = os.path.join('mood_tracker', 'db.sqlite3')
    
    if not os.path.exists(db_path):
        print(f"Database file not found at {db_path}")
        return False
    
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Test 1: Check if new columns exist in tracker_profile
        cursor.execute("PRAGMA table_info(tracker_profile)")
        columns = [col[1] for col in cursor.fetchall()]
        
        required_columns = ['coin_balance', 'clarity_score', 'streak_count', 'last_mood_log', 'streak_last_updated']
        missing_columns = [col for col in required_columns if col not in columns]
        
        if missing_columns:
            print(f"❌ Missing columns in tracker_profile: {missing_columns}")
            return False
        else:
            print("✅ All required columns exist in tracker_profile")
        
        # Test 2: Check if new tables exist
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [row[0] for row in cursor.fetchall()]
        
        required_tables = ['tracker_challenge', 'tracker_cointransaction', 'tracker_nudge']
        missing_tables = [table for table in required_tables if table not in tables]
        
        if missing_tables:
            print(f"❌ Missing tables: {missing_tables}")
            return False
        else:
            print("✅ All required tables exist")
        
        # Test 3: Test basic operations
        # Check if we can query the profile table
        cursor.execute("SELECT COUNT(*) FROM tracker_profile")
        profile_count = cursor.fetchone()[0]
        print(f"✅ Profile table accessible, contains {profile_count} records")
        
        # Check if we can insert a test record (then delete it)
        cursor.execute("INSERT INTO tracker_profile (age, user_id, coin_balance, clarity_score, streak_count) VALUES (25, 999, 10, 100, 1)")
        cursor.execute("DELETE FROM tracker_profile WHERE user_id = 999")
        print("✅ Profile table insert/delete operations work")
        
        conn.commit()
        
        print("\n🎉 Database schema is correct and functional!")
        return True
        
    except Exception as e:
        print(f"❌ Database test failed: {e}")
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    test_database_schema()
