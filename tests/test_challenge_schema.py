#!/usr/bin/env python
"""
Django management command to test and fix schema issues
"""
import os
import sys
import django
from django.core.management.base import BaseCommand
from django.db import connection

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mood_tracker.mood_tracker.settings')
django.setup()

from mood_tracker.tracker.models import Challenge, Profile

class Command(BaseCommand):
    help = 'Test and fix Challenge model schema issues'

    def handle(self, *args, **options):
        print("=== TESTING CHALLENGE MODEL SCHEMA ===")
        
        # Test 1: Check database connection
        print("1. Testing database connection...")
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
                print("   ✅ Database connection successful")
        except Exception as e:
            print(f"   ❌ Database connection failed: {e}")
            return
        
        # Test 2: Check table structure
        print("2. Checking tracker_challenge table structure...")
        try:
            with connection.cursor() as cursor:
                cursor.execute("PRAGMA table_info(tracker_challenge)")
                columns = cursor.fetchall()
                column_names = [col[1] for col in columns]
                print(f"   ✅ Table exists with columns: {column_names}")
                
                if 'settled' in column_names:
                    print("   ✅ 'settled' column exists")
                else:
                    print("   ❌ 'settled' column missing")
                    return
        except Exception as e:
            print(f"   ❌ Error checking table structure: {e}")
            return
        
        # Test 3: Test Django ORM
        print("3. Testing Django ORM...")
        try:
            count = Challenge.objects.count()
            print(f"   ✅ Challenge.objects.count() = {count}")
        except Exception as e:
            print(f"   ❌ Error with Challenge.objects.count(): {e}")
            return
        
        # Test 4: Test settled field specifically
        print("4. Testing 'settled' field...")
        try:
            settled_count = Challenge.objects.filter(settled=True).count()
            print(f"   ✅ Challenge.objects.filter(settled=True).count() = {settled_count}")
        except Exception as e:
            print(f"   ❌ Error with settled filter: {e}")
            
            # Try to refresh the database connection
            print("   🔄 Refreshing database connection...")
            connection.close()
            
            try:
                settled_count = Challenge.objects.filter(settled=True).count()
                print(f"   ✅ After refresh: Challenge.objects.filter(settled=True).count() = {settled_count}")
            except Exception as e2:
                print(f"   ❌ Still failing after refresh: {e2}")
                return
        
        # Test 5: Test creating a challenge
        print("5. Testing challenge creation...")
        try:
            profiles = Profile.objects.all()
            if profiles.exists():
                profile = profiles.first()
                
                # Create a test challenge
                test_challenge = Challenge.objects.create(
                    profile=profile,
                    challenge_type='test',
                    stake=1,
                    start_date='2024-01-01',
                    end_date='2024-01-02',
                    completed=False,
                    settled=False
                )
                
                print(f"   ✅ Created test challenge with ID {test_challenge.id}")
                
                # Update settled field
                test_challenge.settled = True
                test_challenge.save()
                print(f"   ✅ Updated settled field to True")
                
                # Clean up
                test_challenge.delete()
                print(f"   ✅ Deleted test challenge")
            else:
                print("   ⚠️  No profiles found - skipping challenge creation test")
                
        except Exception as e:
            print(f"   ❌ Error creating challenge: {e}")
        
        print("\n=== TESTING COMPLETE ===")

if __name__ == '__main__':
    command = Command()
    command.handle()
