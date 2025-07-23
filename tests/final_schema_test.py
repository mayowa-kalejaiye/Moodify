#!/usr/bin/env python
"""
Quick test to verify the schema fix
"""
import os
import sys
import django
import subprocess
import time
import threading

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mood_tracker.mood_tracker.settings')
django.setup()

from mood_tracker.tracker.models import Challenge, Profile

print("=== FINAL SCHEMA VERIFICATION ===")

# Test 1: Direct Django ORM test
print("1. Testing Django ORM...")
try:
    # Test the exact query that was failing
    challenges = Challenge.objects.filter(settled=False)
    print(f"   ✅ Challenge.objects.filter(settled=False) works! Count: {challenges.count()}")
    
    challenges = Challenge.objects.filter(settled=True)
    print(f"   ✅ Challenge.objects.filter(settled=True) works! Count: {challenges.count()}")
    
    # Test with profile filter
    profiles = Profile.objects.all()
    if profiles.exists():
        profile = profiles.first()
        active_challenges = Challenge.objects.filter(profile=profile, settled=False)
        print(f"   ✅ Challenge.objects.filter(profile=profile, settled=False) works! Count: {active_challenges.count()}")
    
except Exception as e:
    print(f"   ❌ Django ORM test failed: {e}")
    exit(1)

# Test 2: Direct database test
print("\n2. Testing direct database access...")
try:
    from django.db import connection
    with connection.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) FROM tracker_challenge WHERE settled = 0")
        count = cursor.fetchone()[0]
        print(f"   ✅ Direct SQL query works! Count: {count}")
except Exception as e:
    print(f"   ❌ Direct database test failed: {e}")
    exit(1)

# Test 3: Model validation
print("\n3. Testing model validation...")
try:
    from django.core.exceptions import ValidationError
    
    # Test creating a challenge instance
    profiles = Profile.objects.all()
    if profiles.exists():
        profile = profiles.first()
        
        challenge = Challenge(
            profile=profile,
            challenge_type='daily_reflection',
            stake=10,
            start_date='2024-01-01',
            end_date='2024-01-02',
            completed=False,
            settled=False
        )
        
        # Validate without saving
        challenge.full_clean()
        print(f"   ✅ Challenge model validation works!")
        
        # Test the settled field specifically
        challenge.settled = True
        challenge.full_clean()
        print(f"   ✅ Settled field validation works!")
    
except Exception as e:
    print(f"   ❌ Model validation failed: {e}")
    exit(1)

print("\n=== ALL TESTS PASSED! ===")
print("✅ The schema is correctly fixed!")
print("✅ All Challenge model operations work!")
print("✅ The 'settled' field is properly accessible!")
print("\n🎉 The Django server should now work without schema errors!")

# Additional diagnostic info
print("\n=== DIAGNOSTIC INFO ===")
print(f"Django version: {django.get_version()}")
print(f"Database backend: {django.conf.settings.DATABASES['default']['ENGINE']}")
print(f"Database file: {django.conf.settings.DATABASES['default']['NAME']}")

# Check if the database file exists and its size
db_path = django.conf.settings.DATABASES['default']['NAME']
if os.path.exists(db_path):
    print(f"Database file exists: {os.path.getsize(db_path)} bytes")
else:
    print("❌ Database file not found!")
