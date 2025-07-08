#!/usr/bin/env python
import os
import sys
import django
import requests
import json
from datetime import datetime

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mood_tracker.mood_tracker.settings')
django.setup()

from mood_tracker.tracker.models import Profile, Challenge

print("=== TESTING DJANGO ORM WITH CHALLENGE MODEL ===")

try:
    # Test basic Challenge model operations
    print("1. Testing Challenge.objects.all()...")
    challenges = Challenge.objects.all()
    print(f"   ✅ Success! Found {challenges.count()} challenges")
    
    print("2. Testing Challenge.objects.filter(settled=True)...")
    settled_challenges = Challenge.objects.filter(settled=True)
    print(f"   ✅ Success! Found {settled_challenges.count()} settled challenges")
    
    print("3. Testing Challenge.objects.filter(settled=False)...")
    unsettled_challenges = Challenge.objects.filter(settled=False)
    print(f"   ✅ Success! Found {unsettled_challenges.count()} unsettled challenges")
    
    # Test creating a challenge if we have profiles
    profiles = Profile.objects.all()
    if profiles.exists():
        profile = profiles.first()
        print(f"4. Testing Challenge creation with profile {profile.id}...")
        
        # Create a test challenge
        test_challenge = Challenge.objects.create(
            profile=profile,
            challenge_type='daily_mood',
            stake=10,
            start_date=datetime.now().date(),
            end_date=datetime.now().date(),
            completed=False,
            settled=False
        )
        
        print(f"   ✅ Success! Created challenge with ID {test_challenge.id}")
        
        # Update the settled field
        test_challenge.settled = True
        test_challenge.save()
        print(f"   ✅ Success! Updated settled field to True")
        
        # Delete the test challenge
        test_challenge.delete()
        print(f"   ✅ Success! Deleted test challenge")
        
    else:
        print("4. ❌ No profiles found - creating a test profile...")
        
        # Create a test profile
        from django.contrib.auth import get_user_model
        User = get_user_model()
        
        # Create a test user if none exists
        if not User.objects.filter(username='testuser').exists():
            test_user = User.objects.create_user(
                username='testuser',
                email='test@example.com',
                password='testpass123'
            )
            print(f"   ✅ Created test user: {test_user.username}")
        else:
            test_user = User.objects.get(username='testuser')
            print(f"   ✅ Using existing test user: {test_user.username}")
        
        # Create a test profile
        test_profile = Profile.objects.create(
            user=test_user,
            coin_balance=100,
            clarity_score=0.0,
            streak_count=0
        )
        print(f"   ✅ Created test profile with ID {test_profile.id}")
        
        # Now test challenge creation
        test_challenge = Challenge.objects.create(
            profile=test_profile,
            challenge_type='daily_mood',
            stake=10,
            start_date=datetime.now().date(),
            end_date=datetime.now().date(),
            completed=False,
            settled=False
        )
        
        print(f"   ✅ Success! Created challenge with ID {test_challenge.id}")
        
        # Update the settled field
        test_challenge.settled = True
        test_challenge.save()
        print(f"   ✅ Success! Updated settled field to True")
        
        # Clean up
        test_challenge.delete()
        test_profile.delete()
        test_user.delete()
        print(f"   ✅ Success! Cleaned up test data")
    
    print("\n=== ALL DJANGO ORM TESTS PASSED! ===")
    print("The Challenge model and database schema are working correctly.")
    
except Exception as e:
    print(f"❌ Error testing Django ORM: {e}")
    import traceback
    traceback.print_exc()
    
    # Try to diagnose the issue
    print("\n=== DIAGNOSTIC INFORMATION ===")
    print(f"Django version: {django.get_version()}")
    print(f"Database backend: {django.conf.settings.DATABASES['default']['ENGINE']}")
    print(f"Database path: {django.conf.settings.DATABASES['default']['NAME']}")
