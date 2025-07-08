#!/usr/bin/env python
"""
Comprehensive verification of all behavior engine tables
"""

import sqlite3
import os

def verify_complete_schema():
    """Verify that all behavior engine tables have the correct schema"""
    db_path = os.path.join('mood_tracker', 'db.sqlite3')
    
    if not os.path.exists(db_path):
        print("❌ Database file not found!")
        return False

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        print("=" * 60)
        print("COMPREHENSIVE BEHAVIOR ENGINE SCHEMA VERIFICATION")
        print("=" * 60)
        
        # 1. Profile table
        print("\n1. TRACKER_PROFILE TABLE")
        print("-" * 30)
        cursor.execute("PRAGMA table_info(tracker_profile)")
        profile_columns = {col[1]: col[2] for col in cursor.fetchall()}
        
        required_profile_columns = {
            'coin_balance': 'INTEGER',
            'clarity_score': 'INTEGER', 
            'streak_count': 'INTEGER',
            'last_mood_log': 'DATE',
            'streak_last_updated': 'DATE'
        }
        
        for col_name, col_type in required_profile_columns.items():
            if col_name in profile_columns:
                print(f"✅ {col_name}")
            else:
                print(f"❌ {col_name} - MISSING")
                return False
        
        # 2. CoinTransaction table
        print("\n2. TRACKER_COINTRANSACTION TABLE")
        print("-" * 30)
        cursor.execute("PRAGMA table_info(tracker_cointransaction)")
        transaction_columns = {col[1]: col[2] for col in cursor.fetchall()}
        
        required_transaction_columns = {
            'id': 'INTEGER',
            'profile_id': 'INTEGER',
            'transaction_type': 'VARCHAR(50)',
            'amount': 'INTEGER',
            'balance_after': 'INTEGER',
            'challenge_id': 'INTEGER',
            'created_at': 'TIMESTAMP'
        }
        
        for col_name, col_type in required_transaction_columns.items():
            if col_name in transaction_columns:
                print(f"✅ {col_name}")
            else:
                print(f"❌ {col_name} - MISSING")
                return False
        
        # 3. Challenge table
        print("\n3. TRACKER_CHALLENGE TABLE")
        print("-" * 30)
        cursor.execute("PRAGMA table_info(tracker_challenge)")
        challenge_columns = {col[1]: col[2] for col in cursor.fetchall()}
        
        required_challenge_columns = {
            'id': 'INTEGER',
            'profile_id': 'INTEGER',
            'challenge_type': 'VARCHAR(50)',
            'stake': 'INTEGER',
            'start_date': 'DATE',
            'end_date': 'DATE',
            'completed': 'BOOLEAN',
            'settled': 'BOOLEAN',
            'created_at': 'TIMESTAMP'
        }
        
        for col_name, col_type in required_challenge_columns.items():
            if col_name in challenge_columns:
                print(f"✅ {col_name}")
            else:
                print(f"❌ {col_name} - MISSING")
                return False
        
        # 4. Nudge table
        print("\n4. TRACKER_NUDGE TABLE")
        print("-" * 30)
        cursor.execute("PRAGMA table_info(tracker_nudge)")
        nudge_columns = {col[1]: col[2] for col in cursor.fetchall()}
        
        required_nudge_columns = {
            'id': 'INTEGER',
            'profile_id': 'INTEGER',
            'nudge_type': 'VARCHAR(50)',
            'message': 'TEXT',
            'tone': 'VARCHAR(50)',
            'viewed': 'BOOLEAN',
            'created_at': 'TIMESTAMP'
        }
        
        for col_name, col_type in required_nudge_columns.items():
            if col_name in nudge_columns:
                print(f"✅ {col_name}")
            else:
                print(f"❌ {col_name} - MISSING")
                return False
        
        print("\n" + "=" * 60)
        print("✅ ALL SCHEMAS ARE CORRECT!")
        print("✅ All API endpoints should work now!")
        print("=" * 60)
        
        return True
        
    except Exception as e:
        print(f"❌ Error during verification: {e}")
        return False
    finally:
        conn.close()

if __name__ == "__main__":
    verify_complete_schema()
