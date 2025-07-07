#!/usr/bin/env python
"""
Simple test script to verify MoodSync Behavior Engine implementation
"""
import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configure Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mood_tracker.settings')
django.setup()

# Now we can import Django modules
from django.contrib.auth.models import User
from mood_tracker.tracker.models import Profile, Mood, Challenge, CoinTransaction, Nudge
from datetime import date, timedelta

def test_behavior_engine():
    """Test basic behavior engine functionality"""
    print("🎮 Testing MoodSync Behavior Engine v1")
    print("=" * 50)
    
    # Create test user
    user, created = User.objects.get_or_create(
        username='test_behavior',
        defaults={
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
    )
    
    if created:
        print("✅ Created test user")
    
    # Get profile
    profile = Profile.objects.get(user=user)
    profile.age = 25
    profile.save()
    
    print(f"👤 Profile: {profile.user.username}")
    print(f"💰 Initial coin balance: {profile.coin_balance}")
    print(f"🎯 Initial clarity score: {profile.clarity_score}")
    print(f"🔥 Initial streak: {profile.streak_count}")
    
    # Test mood logging (should award coins)
    print("\n📝 Testing mood logging...")
    mood = Mood.objects.create(
        user=user,
        mood='happy',
        rating=4,
        notes='Testing the behavior engine!'
    )
    
    # Refresh profile to see changes
    profile.refresh_from_db()
    print(f"💰 Coin balance after mood log: {profile.coin_balance}")
    print(f"🔥 Streak after mood log: {profile.streak_count}")
    
    # Test coin transactions
    transactions = CoinTransaction.objects.filter(profile=profile)
    print(f"📊 Total transactions: {transactions.count()}")
    
    if transactions.exists():
        latest = transactions.first()
        print(f"   Latest: {latest.transaction_type} ({latest.amount:+d} coins)")
    
    # Test challenge creation (if user has enough coins)
    if profile.coin_balance >= 10:
        print("\n🎯 Testing challenge creation...")
        challenge = Challenge.objects.create(
            profile=profile,
            challenge_type='daily_reflection',
            stake=10,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=7)
        )
        print(f"✅ Created challenge: {challenge.challenge_type}")
        print(f"   Stake: {challenge.stake} coins")
        print(f"   Duration: {challenge.days_remaining} days")
        print(f"   Active: {challenge.is_active}")
    
    # Test nudge creation
    print("\n💬 Testing nudge creation...")
    nudge = Nudge.objects.create(
        profile=profile,
        nudge_type='time_reminder',
        message='Quick vibe check? How are you feeling today? 😊',
        tone='gen_z' if profile.age < 30 else 'professional'
    )
    print(f"✅ Created nudge: {nudge.nudge_type}")
    print(f"   Tone: {nudge.tone}")
    print(f"   Message: {nudge.message}")
    
    # Test profile methods
    print("\n🧪 Testing profile methods...")
    can_stake = profile.can_stake_coins()
    print(f"   Can stake coins: {can_stake}")
    
    # Update streak
    profile.update_streak()
    print(f"   Updated streak: {profile.streak_count}")
    
    print("\n🎉 Behavior Engine Test Complete!")
    print("=" * 50)
    
    # Display summary
    print("\n📋 SUMMARY")
    print(f"User: {user.username}")
    print(f"Coins: {profile.coin_balance}")
    print(f"Clarity Score: {profile.clarity_score}")
    print(f"Streak: {profile.streak_count}")
    print(f"Last Mood Log: {profile.last_mood_log}")
    print(f"Challenges: {Challenge.objects.filter(profile=profile).count()}")
    print(f"Nudges: {Nudge.objects.filter(profile=profile).count()}")
    print(f"Transactions: {CoinTransaction.objects.filter(profile=profile).count()}")
    
    return True

if __name__ == '__main__':
    try:
        test_behavior_engine()
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
