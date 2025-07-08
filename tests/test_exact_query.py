#!/usr/bin/env python
"""
Test the exact same query that's failing in views.py
"""
import os
import sys
import django

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mood_tracker.mood_tracker.settings')
django.setup()

from mood_tracker.tracker.models import Challenge, Profile

print("=== TESTING EXACT FAILING QUERY ===")

try:
    # Get a profile first
    profiles = Profile.objects.all()
    if not profiles.exists():
        print("❌ No profiles found!")
        exit(1)
    
    profile = profiles.first()
    print(f"✅ Using profile ID: {profile.id}")
    
    # This is the exact query from views.py line 857-860
    active_challenge = Challenge.objects.filter(
        profile=profile,
        settled=False
    ).first()
    
    print(f"✅ Query executed successfully!")
    print(f"   Active challenge: {active_challenge}")
    
    # Test the opposite
    settled_challenges = Challenge.objects.filter(
        profile=profile,
        settled=True
    ).count()
    
    print(f"✅ Settled challenges count: {settled_challenges}")
    
    # Test all challenges for this profile
    all_challenges = Challenge.objects.filter(profile=profile).count()
    print(f"✅ All challenges for profile: {all_challenges}")
    
except Exception as e:
    print(f"❌ Error executing query: {e}")
    import traceback
    traceback.print_exc()
    
    # Try to get more info about the error
    print("\n=== DEBUGGING INFO ===")
    
    try:
        from django.db import connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT sql FROM sqlite_master WHERE type='table' AND name='tracker_challenge'")
            result = cursor.fetchone()
            if result:
                print(f"Table SQL: {result[0]}")
            else:
                print("Table not found!")
    except Exception as e2:
        print(f"Error getting table info: {e2}")
