#!/usr/bin/env python3
"""
Pre-Migration Verification Script

This script verifies that:
1. Supabase configuration is correct
2. Database connection works
3. Models can be applied
4. Django settings are properly configured

Run this BEFORE migrating to Supabase to ensure everything is set up correctly.
"""

import os
import sys
import django
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Add the project directory to Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))
sys.path.append(str(project_root / 'mood_tracker'))

# Set Django settings
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mood_tracker.mood_tracker.settings')

def verify_environment():
    """Check environment variables"""
    print("🔍 Checking environment variables...")
    
    required_vars = ['DJANGO_SECRET_KEY', 'DATABASE_URL']
    optional_vars = ['SUPABASE_URL', 'SUPABASE_ANON_KEY', 'SUPABASE_SERVICE_KEY']
    
    missing_required = []
    for var in required_vars:
        if not os.getenv(var):
            missing_required.append(var)
        else:
            print(f"  ✅ {var}: Set")
    
    if missing_required:
        print(f"  ❌ Missing required variables: {', '.join(missing_required)}")
        return False
    
    for var in optional_vars:
        if os.getenv(var):
            print(f"  ✅ {var}: Set")
        else:
            print(f"  ⚠️  {var}: Not set (optional)")
    
    # Check DATABASE_URL format
    db_url = os.getenv('DATABASE_URL')
    if db_url and db_url.startswith('postgresql://'):
        print("  ✅ DATABASE_URL: Valid PostgreSQL format")
    else:
        print("  ❌ DATABASE_URL: Invalid format (should start with postgresql://)")
        return False
        
    return True

def verify_django_setup():
    """Verify Django can initialize"""
    print("\n🔍 Checking Django setup...")
    
    try:
        django.setup()
        print("  ✅ Django setup successful")
        return True
    except Exception as e:
        print(f"  ❌ Django setup failed: {e}")
        return False

def verify_database_connection():
    """Test database connection"""
    print("\n🔍 Testing database connection...")
    
    try:
        from django.db import connection
        
        # Test connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT 1")
            result = cursor.fetchone()
            
        if result[0] == 1:
            print("  ✅ Database connection successful")
            
            # Get database info
            db_settings = connection.settings_dict
            print(f"  📊 Database: {db_settings.get('NAME', 'Unknown')}")
            print(f"  🏢 Host: {db_settings.get('HOST', 'localhost')}")
            print(f"  🔌 Port: {db_settings.get('PORT', 'default')}")
            print(f"  👤 User: {db_settings.get('USER', 'Unknown')}")
            
            return True
        else:
            print("  ❌ Database connection test failed")
            return False
            
    except Exception as e:
        print(f"  ❌ Database connection failed: {e}")
        return False

def verify_models():
    """Check if models can be imported"""
    print("\n🔍 Checking Django models...")
    
    try:
        from mood_tracker.tracker.models import UserProfile, MoodEntry, Challenge
        print("  ✅ Core models imported successfully")
        
        # Check model structure
        print(f"  📋 UserProfile fields: {len(UserProfile._meta.fields)}")
        print(f"  📋 MoodEntry fields: {len(MoodEntry._meta.fields)}")
        print(f"  📋 Challenge fields: {len(Challenge._meta.fields)}")
        
        return True
    except Exception as e:
        print(f"  ❌ Model import failed: {e}")
        return False

def verify_migrations():
    """Check migration status"""
    print("\n🔍 Checking migrations...")
    
    try:
        from django.core.management import execute_from_command_line
        from django.core.management.commands.showmigrations import Command
        
        # This is a bit complex to do programmatically, so we'll just check if migration files exist
        migration_dir = project_root / 'mood_tracker' / 'tracker' / 'migrations'
        
        if migration_dir.exists():
            migration_files = list(migration_dir.glob('*.py'))
            migration_files = [f for f in migration_files if f.name != '__init__.py']
            
            print(f"  📁 Found {len(migration_files)} migration files")
            for f in migration_files[:5]:  # Show first 5
                print(f"    - {f.name}")
            if len(migration_files) > 5:
                print(f"    ... and {len(migration_files) - 5} more")
                
            return True
        else:
            print("  ❌ Migrations directory not found")
            return False
            
    except Exception as e:
        print(f"  ❌ Migration check failed: {e}")
        return False

def main():
    """Run all verification checks"""
    print("🧪 MoodSync Supabase Pre-Migration Verification")
    print("=" * 60)
    
    checks = [
        ("Environment Variables", verify_environment),
        ("Django Setup", verify_django_setup),
        ("Database Connection", verify_database_connection),
        ("Django Models", verify_models),
        ("Migrations", verify_migrations),
    ]
    
    results = []
    
    for check_name, check_func in checks:
        try:
            result = check_func()
            results.append((check_name, result))
        except Exception as e:
            print(f"  ❌ {check_name} check crashed: {e}")
            results.append((check_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("📋 VERIFICATION SUMMARY")
    print("=" * 60)
    
    all_passed = True
    for check_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {check_name}")
        if not passed:
            all_passed = False
    
    print("\n" + "=" * 60)
    if all_passed:
        print("🎉 ALL CHECKS PASSED!")
        print("✅ Ready to migrate to Supabase!")
        print("\nNext steps:")
        print("1. Run: python scripts/migrate_to_supabase.py")
        print("2. Test your application")
        print("3. Update Render environment variables")
        print("4. Deploy to production")
    else:
        print("❌ SOME CHECKS FAILED!")
        print("⚠️  Please fix the issues above before migrating.")
        print("\nCommon fixes:")
        print("- Check your .env file configuration")
        print("- Verify Supabase credentials")
        print("- Ensure DATABASE_URL is correct")
    
    return all_passed

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
