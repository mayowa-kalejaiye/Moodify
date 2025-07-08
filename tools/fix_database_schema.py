#!/usr/bin/env python3
"""
Migration Script to Fix CoinTransaction Description Field
"""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.insert(0, os.path.abspath('.'))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mood_tracker.mood_tracker.settings')
django.setup()

from django.core.management import execute_from_command_line

def run_migration():
    """Run the migration to fix the database schema"""
    print("🔧 FIXING DATABASE SCHEMA")
    print("=" * 50)
    
    try:
        print("📋 Running migration to add description field...")
        execute_from_command_line(['manage.py', 'migrate', 'tracker', '0003'])
        print("✅ Migration completed successfully!")
        
        print("\n🧪 Testing CoinTransaction creation...")
        from mood_tracker.tracker.models import Profile, CoinTransaction
        from django.contrib.auth.models import User
        
        # Try to create a test user and profile
        test_user, created = User.objects.get_or_create(
            username='test_migration_user',
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
        
    except Exception as e:
        print(f"❌ Migration failed: {e}")
        return False
    
    return True

if __name__ == "__main__":
    success = run_migration()
    if success:
        print("\n💡 You can now create comments without IntegrityError!")
    else:
        print("\n⚠️  There was an issue with the migration. Please check the error above.")
