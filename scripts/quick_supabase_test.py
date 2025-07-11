#!/usr/bin/env python3
"""
Quick Supabase Connection Test
"""

import os
import sys
import django
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add project to path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))
sys.path.append(str(project_root / 'mood_tracker'))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mood_tracker.mood_tracker.settings')

def quick_test():
    print("🧪 Quick Supabase Connection Test")
    print("=" * 40)
    
    # Check DATABASE_URL
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        print("❌ DATABASE_URL not found")
        return False
        
    print(f"✅ DATABASE_URL found: {db_url[:50]}...")
    
    # Initialize Django
    try:
        django.setup()
        print("✅ Django initialized")
    except Exception as e:
        print(f"❌ Django setup failed: {e}")
        return False
    
    # Quick DB test
    try:
        from django.db import connection
        cursor = connection.cursor()
        cursor.execute("SELECT version()")
        version = cursor.fetchone()[0]
        print(f"✅ Database connected: {version[:50]}...")
        return True
    except Exception as e:
        print(f"❌ Database connection failed: {e}")
        return False

if __name__ == '__main__':
    success = quick_test()
    if success:
        print("\n🎉 Supabase connection working!")
        print("Ready to migrate!")
    else:
        print("\n❌ Connection issues found")
        print("Check your configuration")
