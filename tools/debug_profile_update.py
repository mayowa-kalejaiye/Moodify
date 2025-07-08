#!/usr/bin/env python3
"""
Test script to debug the Profile PATCH request issue
"""
import os
import sys
import django
from django.conf import settings
import json

# Add the project root to Python path
sys.path.insert(0, os.path.abspath('.'))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mood_tracker.settings')

# Initialize Django
django.setup()

from django.contrib.auth.models import User
from mood_tracker.tracker.models import Profile, get_or_create_profile
from mood_tracker.tracker.serializers import UserSerializer

def test_profile_update():
    """Test profile update scenarios"""
    print("🔧 TESTING PROFILE UPDATE SCENARIOS")
    print("=" * 50)
    
    # Find or create a test user
    test_user, created = User.objects.get_or_create(
        username='testuser',
        defaults={
            'email': 'test@example.com',
            'first_name': 'Test',
            'last_name': 'User'
        }
    )
    
    if created:
        print(f"✅ Created test user: {test_user.username}")
    else:
        print(f"✅ Using existing test user: {test_user.username}")
    
    # Ensure profile exists
    profile = get_or_create_profile(test_user)
    print(f"📋 Current profile age: {profile.age}")
    
    # Test 1: Direct age update via nested profile data
    print("\n🧪 TEST 1: Nested profile data structure")
    test_data_1 = {
        'profile': {
            'age': 25
        }
    }
    
    serializer_1 = UserSerializer(test_user, data=test_data_1, partial=True)
    if serializer_1.is_valid():
        serializer_1.save()
        profile.refresh_from_db()
        print(f"✅ SUCCESS: Age updated to {profile.age}")
    else:
        print(f"❌ VALIDATION ERROR: {serializer_1.errors}")
    
    # Test 2: Flat age structure (what might be sent from frontend)
    print("\n🧪 TEST 2: Flat age structure")
    test_data_2 = {
        'age': 30
    }
    
    serializer_2 = UserSerializer(test_user, data=test_data_2, partial=True)
    if serializer_2.is_valid():
        serializer_2.save()
        profile.refresh_from_db()
        print(f"✅ SUCCESS: Age updated to {profile.age}")
    else:
        print(f"❌ VALIDATION ERROR: {serializer_2.errors}")
    
    # Test 3: Check what the current serializer returns
    print("\n📊 CURRENT SERIALIZER OUTPUT:")
    current_serializer = UserSerializer(test_user)
    print(json.dumps(current_serializer.data, indent=2))
    
    print("\n🔍 DEBUGGING INFO:")
    print(f"User ID: {test_user.id}")
    print(f"Profile exists: {hasattr(test_user, 'profile')}")
    print(f"Profile age: {profile.age}")
    print(f"Profile coin_balance: {profile.coin_balance}")
    
    return profile.age

if __name__ == "__main__":
    try:
        final_age = test_profile_update()
        print(f"\n✅ TEST COMPLETED - Final age: {final_age}")
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
