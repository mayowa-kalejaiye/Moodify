#!/usr/bin/env python3
"""
Direct Database Fix for CoinTransaction Description Field
"""
import os
import sys
import django
import sqlite3

# Add the project directory to the Python path
sys.path.insert(0, os.path.abspath('.'))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mood_tracker.mood_tracker.settings')
django.setup()

from django.conf import settings

def fix_database_schema():
    """Fix the database schema directly"""
    print("🔧 FIXING DATABASE SCHEMA DIRECTLY")
    print("=" * 50)
    
    # Get the database path
    db_path = settings.DATABASES['default']['NAME']
    print(f"📋 Database path: {db_path}")
    
    try:
        # Connect to the database
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        # Check if the description column exists
        cursor.execute("PRAGMA table_info(tracker_cointransaction)")
        columns = cursor.fetchall()
        column_names = [column[1] for column in columns]
        
        print(f"📊 Current columns in tracker_cointransaction: {column_names}")
        
        if 'description' not in column_names:
            print("➕ Adding description column...")
            cursor.execute("""
                ALTER TABLE tracker_cointransaction 
                ADD COLUMN description VARCHAR(255) NULL
            """)
            print("✅ Description column added successfully!")
        else:
            print("✅ Description column already exists!")
        
        # Check if the challenge column exists
        if 'challenge_id' not in column_names:
            print("➕ Adding challenge_id column...")
            cursor.execute("""
                ALTER TABLE tracker_cointransaction 
                ADD COLUMN challenge_id INTEGER NULL
            """)
            print("✅ Challenge_id column added successfully!")
        else:
            print("✅ Challenge_id column already exists!")
        
        # Commit the changes
        conn.commit()
        
        # Test creating a CoinTransaction
        print("\n🧪 Testing CoinTransaction creation...")
        from mood_tracker.tracker.models import Profile, CoinTransaction
        from django.contrib.auth.models import User
        
        # Try to create a test user and profile
        test_user, created = User.objects.get_or_create(
            username='test_schema_user',
            defaults={'email': 'test@example.com'}
        )
        
        profile, created = Profile.objects.get_or_create(user=test_user)
        
        # Try to create a CoinTransaction with description
        transaction = CoinTransaction.objects.create(
            profile=profile,
            transaction_type='earn_mood',
            amount=1,
            balance_after=profile.coin_balance + 1,
            description="Test transaction to verify schema fix"
        )
        
        print("✅ CoinTransaction created successfully!")
        print(f"   Transaction ID: {transaction.id}")
        print(f"   Description: {transaction.description}")
        
        # Clean up test data
        transaction.delete()
        if created:
            test_user.delete()
            
        print("\n🎉 Database schema is now fixed!")
        
        # Close the connection
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"❌ Database fix failed: {e}")
        if 'conn' in locals():
            conn.close()
        return False

if __name__ == "__main__":
    success = fix_database_schema()
    if success:
        print("\n💡 You can now create comments without IntegrityError!")
        print("🚀 Try creating a comment through the API again!")
    else:
        print("\n⚠️  There was an issue with the database fix. Please check the error above.")
