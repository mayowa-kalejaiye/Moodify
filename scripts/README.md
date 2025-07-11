# 📜 Scripts Directory

This directory contains utility scripts for database management, testing, deployment, and production maintenance.

## Available Scripts

### 🗄️ **Database Scripts**

- `create_migration.py` - Create custom Django migrations
- `reset_migrations.py` - Reset migration state (use with caution)
- `setup_test_db.py` - Set up test database environment
- `setup_production_db.py` - Set up production database with migrations and superuser
- `quick_migrate.py` - Quick migration utility
- `migrate_to_supabase.py` - **NEW** - Helper for migrating to Supabase PostgreSQL
- `quick_supabase_test.py` - **NEW** - Quick Supabase connection testing
- `verify_supabase_setup.py` - **NEW** - Comprehensive Supabase setup verification

### 🧪 **Testing Scripts**

- `run_tests.py` - Python test runner with custom options
- `run_tests.bat` - Windows batch file for running tests

### 🔧 **Utility Scripts**

- `generate_secret_key.py` - **NEW** - Generate secure Django secret keys

### 🚀 **Production & Keep-Alive Scripts**

- `keep_alive.py` - Advanced keep-alive service for Render free tier (LOCAL VERSION)
- `simple_keep_alive.py` - Simple keep-alive script
- `start_keep_alive.bat` - Windows launcher for keep-alive service

## Keep-Alive Service

Render free tier apps sleep after 15 minutes of inactivity and take ~50 seconds to wake up. Use these scripts to keep your app active:

### Quick Start (Recommended)
```bash
# Simple keep-alive (pings every 10 minutes)
python scripts/simple_keep_alive.py
```

### Windows Users
Double-click `scripts/start_keep_alive.bat`

### Advanced Usage
```bash
# Advanced keep-alive with more features
python scripts/keep_alive.py

# Run in background mode
python scripts/keep_alive.py --background
```

## Usage Examples

### Database Management

```bash
# Create a new migration
python scripts/create_migration.py

# Set up test database
python scripts/setup_test_db.py

# Quick migration (development)
python scripts/quick_migrate.py

# Set up production database (deployment)
python scripts/setup_production_db.py

# Migrate to Supabase (one-time setup)
python scripts/migrate_to_supabase.py fresh
```

### Testing

```bash
# Run tests with Python script
python scripts/run_tests.py

# Run tests with batch file (Windows)
scripts\run_tests.bat
```

## Safety Notes

- ⚠️ **Migration scripts**: Always backup your database before running migration utilities
- 🧪 **Test environment**: Use `setup_test_db.py` for isolated testing
- 📋 **Documentation**: Each script includes usage instructions in comments

## Integration

These scripts are designed to work with the main Django project structure and should be run from the project root directory.

## 🚀 **Automatic Server-Side Keep-Alive (NEW - Recommended)**

The production app now includes a **built-in keep-alive service** that runs automatically on the server. This is the preferred method as it doesn't require any local setup.

**Features:**
- ✅ Automatically starts when the app deploys
- ✅ Runs in the background without user intervention  
- ✅ Only active in production (disabled in DEBUG mode)
- ✅ Prevents Render free tier cold starts
- ✅ Logs activity for monitoring

**Control Commands:**
```bash
# Check if keep-alive is running
python manage.py keep_alive status

# Manually start keep-alive (usually not needed)
python manage.py keep_alive start

# Stop keep-alive service  
python manage.py keep_alive stop
```

The local keep-alive scripts (`keep_alive.py`, `simple_keep_alive.py`) are now backup options only.
