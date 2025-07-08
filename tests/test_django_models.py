#!/usr/bin/env python
"""
Test Django models directly with correct settings
"""

import os
import sys
import django
from django.conf import settings

# Add the project directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Configure Django settings using the inner settings file directly
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mood_tracker.mood_tracker.settings')

try:
    django.setup()
    print("✅ Django setup successful")
    
    # Now we can import Django modules
    from django.contrib.auth.models import User
    from mood_tracker.tracker.models import Profile, Mood, Challenge, CoinTransaction, Nudge
    print("✅ Models imported successfully")
    
    # Test basic model operations
    # Check if we can query the models
    profile_count = Profile.objects.count()
    print(f"✅ Profile model accessible, contains {profile_count} records")
    
    # Test if we can access the new fields
    if profile_count > 0:
        profile = Profile.objects.first()
        print(f"✅ Profile fields accessible: coin_balance={profile.coin_balance}, clarity_score={profile.clarity_score}")
    
    # Test if we can create the other models
    challenge_count = Challenge.objects.count()
    transaction_count = CoinTransaction.objects.count()
    nudge_count = Nudge.objects.count()
    
    print(f"✅ Challenge model accessible, contains {challenge_count} records")
    print(f"✅ CoinTransaction model accessible, contains {transaction_count} records")
    print(f"✅ Nudge model accessible, contains {nudge_count} records")
    
    print("\n🎉 All Django models are working correctly!")
    
except Exception as e:
    print(f"❌ Django test failed: {e}")
    import traceback
    traceback.print_exc()
