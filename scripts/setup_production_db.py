#!/usr/bin/env python3
"""
Production Database Setup Script

This script ensures the production database is properly migrated
and creates a superuser if needed.

Usage:
    python setup_production_db.py
"""
import os
import sys
import django
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the project directory to Python path
sys.path.append('.')

# Set up Django with production settings if available
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mood_tracker.mood_tracker.settings')

def setup_database():
    """Set up the production database"""
    try:
        django.setup()
        
        from django.core.management import execute_from_command_line
        from django.contrib.auth import get_user_model
        from django.db import connection
        
        print("🔧 Setting up production database...")
        
        # Test database connection
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            print("✅ Database connection successful")
        except Exception as e:
            print(f"❌ Database connection failed: {e}")
            return False
        
        # Run migrations
        print("📊 Running database migrations...")
        try:
            execute_from_command_line(['manage.py', 'migrate', '--noinput'])
            print("✅ Migrations completed successfully")
        except Exception as e:
            print(f"❌ Migration failed: {e}")
            return False
        
        # Check if superuser exists, create if not
        User = get_user_model()
        if not User.objects.filter(is_superuser=True).exists():
            print("👤 Creating superuser...")
            try:
                User.objects.create_superuser(
                    username='admin',
                    email='admin@moodsync.app',
                    password=os.environ.get('ADMIN_PASSWORD', 'admin123')
                )
                print("✅ Superuser created successfully")
                print("📝 Username: admin")
                print("📝 Password: Set ADMIN_PASSWORD env var or use default")
            except Exception as e:
                print(f"⚠️ Could not create superuser: {e}")
        else:
            print("✅ Superuser already exists")
        
        # Collect static files
        print("📁 Collecting static files...")
        try:
            execute_from_command_line(['manage.py', 'collectstatic', '--noinput'])
            print("✅ Static files collected")
        except Exception as e:
            print(f"⚠️ Static files collection warning: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Database setup failed: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main setup function"""
    print("🚀 PRODUCTION DATABASE SETUP")
    print("=" * 40)
    
    success = setup_database()
    
    if success:
        print("\n🎉 Production database setup completed successfully!")
        print("📝 Next steps:")
        print("  1. Your app should now work correctly")
        print("  2. Swagger should be accessible at /swagger/")
        print("  3. Admin panel at /admin/ (if superuser created)")
    else:
        print("\n❌ Database setup failed!")
        print("🔧 Troubleshooting:")
        print("  1. Check database connection")
        print("  2. Verify environment variables")
        print("  3. Check deployment logs")

if __name__ == "__main__":
    main()
