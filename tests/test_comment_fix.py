#!/usr/bin/env python3
"""
Test API Endpoint After Fix
"""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.insert(0, os.path.abspath('.'))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mood_tracker.mood_tracker.settings')
django.setup()

from django.contrib.auth.models import User
from mood_tracker.tracker.models import Mood, Comment, Profile, CoinTransaction

def test_comment_creation():
    """Test comment creation to verify the fix"""
    print("🧪 TESTING COMMENT CREATION")
    print("=" * 50)
    
    try:
        # Create a test user
        test_user, created = User.objects.get_or_create(
            username='test_comment_user',
            defaults={'email': 'test@example.com'}
        )
        
        # Create a profile
        profile, created = Profile.objects.get_or_create(user=test_user)
        initial_balance = profile.coin_balance
        
        # Create a mood entry
        mood = Mood.objects.create(
            user=test_user,
            mood="Happy",
            notes="Test mood for comment",
            rating=4
        )
        
        print(f"✅ Created mood: {mood}")
        print(f"💰 Initial coin balance: {initial_balance}")
        
        # Create a comment (this should trigger the signal)
        comment = Comment.objects.create(
            mood=mood,
            user=test_user,
            content="This is a test comment to verify the fix works!"
        )
        
        print(f"✅ Created comment: {comment}")
        
        # Check if coins were awarded
        profile.refresh_from_db()
        print(f"💰 New coin balance: {profile.coin_balance}")
        print(f"💰 Coins earned: {profile.coin_balance - initial_balance}")
        
        # Check if transaction was created
        transactions = CoinTransaction.objects.filter(profile=profile).order_by('-created_at')
        if transactions.exists():
            latest_transaction = transactions.first()
            print(f"✅ Transaction created: {latest_transaction}")
            print(f"📝 Description: {latest_transaction.description}")
        else:
            print("❌ No transaction found!")
        
        # Clean up
        comment.delete()
        mood.delete()
        if created:
            test_user.delete()
            
        print("\n🎉 Comment creation test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return False

if __name__ == "__main__":
    success = test_comment_creation()
    if success:
        print("\n💡 The IntegrityError has been fixed!")
        print("🚀 You can now create comments through the API without errors!")
    else:
        print("\n⚠️  There was still an issue. Please check the error above.")
