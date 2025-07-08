#!/usr/bin/env python
import os
import sys
import django

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mood_tracker.mood_tracker.settings')
django.setup()

from mood_tracker.tracker.models import Challenge, Profile

print("Testing Challenge model...")

try:
    # Test querying the Challenge model
    challenges = Challenge.objects.all()
    print(f"✅ Challenge.objects.all() works! Count: {challenges.count()}")
    
    # Test the settled field specifically
    settled_challenges = Challenge.objects.filter(settled=True)
    print(f"✅ Challenge.objects.filter(settled=True) works! Count: {settled_challenges.count()}")
    
    # Test creating a new challenge
    profiles = Profile.objects.all()
    if profiles.exists():
        profile = profiles.first()
        
        # Create a test challenge
        test_challenge = Challenge(
            profile=profile,
            challenge_type='daily_mood',
            stake=10,
            start_date='2024-01-01',
            end_date='2024-01-07',
            completed=False,
            settled=False
        )
        
        # Don't save it, just test validation
        test_challenge.full_clean()
        print("✅ Challenge model validation works!")
        
        print("\nAll Challenge model tests passed!")
        
    else:
        print("❌ No profiles found - cannot test challenge creation")
        
except Exception as e:
    print(f"❌ Error testing Challenge model: {e}")
    import traceback
    traceback.print_exc()
