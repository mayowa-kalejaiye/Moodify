import sqlite3
import os

# Path to the SQLite database
db_path = os.path.join('mood_tracker', 'db.sqlite3')

def fix_database():
    """Fix the database schema by adding missing columns"""
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # First, let's check the current schema
        cursor.execute("PRAGMA table_info(tracker_profile)")
        columns = [col[1] for col in cursor.fetchall()]
        print("Current columns in tracker_profile:", columns)
        
        # Add missing columns one by one
        missing_columns = {
            'coin_balance': 'INTEGER DEFAULT 0',
            'clarity_score': 'INTEGER DEFAULT 100',
            'streak_count': 'INTEGER DEFAULT 0',
            'last_mood_log': 'DATE',
            'streak_last_updated': 'DATE'
        }
        
        for col_name, col_definition in missing_columns.items():
            if col_name not in columns:
                try:
                    cursor.execute(f"ALTER TABLE tracker_profile ADD COLUMN {col_name} {col_definition}")
                    print(f"Added column: {col_name}")
                except Exception as e:
                    print(f"Error adding column {col_name}: {e}")
            else:
                print(f"Column {col_name} already exists")
        
        # Create new tables
        print("\nCreating new tables...")
        
        # Challenge table
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
        
        # Coin transaction table
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
        
        # Nudge table
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
        
        # Commit changes
        conn.commit()
        print("\nDatabase schema updated successfully!")
        
        # Show the updated schema
        cursor.execute("PRAGMA table_info(tracker_profile)")
        columns = [col[1] for col in cursor.fetchall()]
        print("Updated columns in tracker_profile:", columns)
        
    except Exception as e:
        print(f"Error: {e}")
        conn.rollback()
    finally:
        conn.close()

if __name__ == "__main__":
    fix_database()
