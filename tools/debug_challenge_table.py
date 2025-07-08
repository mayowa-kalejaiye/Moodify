#!/usr/bin/env python
import sqlite3
import os

# Connect to the database
db_path = os.path.join(os.path.dirname(__file__), 'mood_tracker', 'db.sqlite3')
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

print("=== CHECKING TRACKER_CHALLENGE TABLE STRUCTURE ===")

# Get table schema
cursor.execute("PRAGMA table_info(tracker_challenge)")
columns = cursor.fetchall()

print("Columns in tracker_challenge:")
for col in columns:
    print(f"  {col[1]} ({col[2]})")

print("\n=== CHECKING IF SETTLED COLUMN EXISTS ===")

# Check if settled column exists
settled_exists = any(col[1] == 'settled' for col in columns)
print(f"Settled column exists: {settled_exists}")

if settled_exists:
    print("\n=== TESTING SETTLED COLUMN ===")
    try:
        cursor.execute("SELECT id, settled FROM tracker_challenge LIMIT 5")
        rows = cursor.fetchall()
        print(f"Found {len(rows)} rows with settled values:")
        for row in rows:
            print(f"  ID {row[0]}: settled={row[1]}")
    except Exception as e:
        print(f"Error querying settled column: {e}")
        
print("\n=== CHECKING DATABASE FILE ===")
print(f"Database path: {db_path}")
print(f"Database exists: {os.path.exists(db_path)}")
print(f"Database size: {os.path.getsize(db_path)} bytes")

conn.close()
