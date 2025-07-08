# 🛠️ Tools Directory

This directory contains utility scripts and debugging tools used during MoodSync development.

## Tool Categories

### 🔧 **Database Management**

- `fix_database.py` - General database repair utilities
- `fix_database_direct.py` - Direct database manipulation scripts
- `fix_database_schema.py` - Schema correction tools
- `fix_migrations.py` - Migration repair utilities
- `fix_challenge_table.py` - Challenge model specific fixes
- `fix_cointransaction_table.py` - CoinTransaction table repairs

### 🐛 **Debugging Tools**

- `debug_challenge_table.py` - Challenge model debugging
- `debug_profile_update.py` - Profile update issue debugging
- `profile_update_test.py` - Profile update validation testing

### ✅ **Verification Scripts**

- `final_database_verification.py` - Complete database integrity check
- `final_verification.py` - Final system verification
- `comprehensive_schema_check.py` - Comprehensive schema validation
- `check_import.py` - Import validation utility

### 📊 **API Testing Tools**

- `CHECK_SWAGGER_FINAL.py` - Swagger documentation validation
- `SIMPLE_SWAGGER_CHECK.py` - Basic Swagger functionality test
- `final_schema_test.py` - Final schema testing
- `FINAL_RESOLUTION_COMPLETE.py` - Complete resolution validation
- `FINAL_RESOLUTION_REPORT.py` - Final resolution reporting

### 🎯 **Development Utilities**

- `simple_django_test.py` - Basic Django functionality tests
- `simple_test.py` - Simple system tests
- `inspect_project.py` - Project structure inspection
- `demo_time_consciousness.py` - Time consciousness feature demo

## Usage

These tools are primarily for development and debugging purposes:

```bash
# Run a specific tool
python tools/demo_time_consciousness.py

# Check database integrity
python tools/final_database_verification.py

# Validate Swagger documentation
python tools/CHECK_SWAGGER_FINAL.py
```

## Important Notes

- ⚠️ **Use with caution**: These tools can modify database state
- 🔒 **Development only**: Not intended for production use
- 📋 **Documentation**: Each script contains inline documentation
- 🧪 **Testing**: Always test on development databases first

## Maintenance

These tools were created during the behavior engine development phase and may need updates for future versions of MoodSync.
