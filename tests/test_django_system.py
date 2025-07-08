#!/usr/bin/env python
import os
import subprocess
import sys

# Add the project directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

print("=== TESTING DJANGO SERVER AND ENDPOINTS ===")

# Test Django check
print("1. Running Django check...")
try:
    result = subprocess.run([sys.executable, 'manage.py', 'check'], 
                          capture_output=True, text=True, cwd=os.path.dirname(__file__))
    if result.returncode == 0:
        print("   ✅ Django check passed!")
        print(f"   Output: {result.stdout.strip()}")
    else:
        print("   ❌ Django check failed!")
        print(f"   Error: {result.stderr.strip()}")
        exit(1)
except Exception as e:
    print(f"   ❌ Error running Django check: {e}")
    exit(1)

# Test Django migrations
print("\n2. Checking Django migrations...")
try:
    result = subprocess.run([sys.executable, 'manage.py', 'showmigrations'], 
                          capture_output=True, text=True, cwd=os.path.dirname(__file__))
    if result.returncode == 0:
        print("   ✅ Migrations check passed!")
        print("   Migration status:")
        for line in result.stdout.strip().split('\n'):
            if line.strip():
                print(f"     {line}")
    else:
        print("   ❌ Migrations check failed!")
        print(f"   Error: {result.stderr.strip()}")
except Exception as e:
    print(f"   ❌ Error checking migrations: {e}")

# Test Django collectstatic
print("\n3. Testing Django collectstatic...")
try:
    result = subprocess.run([sys.executable, 'manage.py', 'collectstatic', '--noinput'], 
                          capture_output=True, text=True, cwd=os.path.dirname(__file__))
    if result.returncode == 0:
        print("   ✅ Collectstatic passed!")
    else:
        print("   ❌ Collectstatic failed!")
        print(f"   Error: {result.stderr.strip()}")
except Exception as e:
    print(f"   ❌ Error running collectstatic: {e}")

# Test Django shell command
print("\n4. Testing Django shell command...")
try:
    django_command = """
import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mood_tracker.mood_tracker.settings')
import django
django.setup()
from mood_tracker.tracker.models import Challenge
print(f"Challenge model imported successfully. Count: {Challenge.objects.count()}")
"""
    result = subprocess.run([sys.executable, '-c', django_command], 
                          capture_output=True, text=True, cwd=os.path.dirname(__file__))
    if result.returncode == 0:
        print("   ✅ Django shell test passed!")
        print(f"   Output: {result.stdout.strip()}")
    else:
        print("   ❌ Django shell test failed!")
        print(f"   Error: {result.stderr.strip()}")
except Exception as e:
    print(f"   ❌ Error running Django shell test: {e}")

print("\n=== TESTING COMPLETE ===")
