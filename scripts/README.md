# 📜 Scripts Directory

This directory contains utility scripts for database management, testing, and deployment tasks.

## Available Scripts

### 🗄️ **Database Scripts**

- `create_migration.py` - Create custom Django migrations
- `reset_migrations.py` - Reset migration state (use with caution)
- `setup_test_db.py` - Set up test database environment
- `setup_production_db.py` - Set up production database with migrations and superuser
- `quick_migrate.py` - Quick migration utility

### 🧪 **Testing Scripts**

- `run_tests.py` - Python test runner with custom options
- `run_tests.bat` - Windows batch file for running tests

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
