# 🧪 Tests Directory

This directory contains all test scripts for the MoodSync 2.0 platform, organized by functionality and purpose.

## Test Categories

### 🤖 **AI & Behavior Engine Tests**
- `test_ai_behavior_engine.py` - AI behavior engine functionality
- `test_ai_connection.py` - AI service connectivity and endpoints
- `test_behavior_engine.py` - Core behavior engine logic and gamification
- `test_time_consciousness.py` - Time-aware behavior testing across 7 periods

### 🗄️ **Database & ORM Tests**
- `test_database_schema.py` - Database schema validation and integrity
- `test_django_models.py` - Django model functionality and relationships
- `test_django_orm.py` - ORM operations and queries
- `test_exact_query.py` - Specific query testing and optimization
- `test_challenge_model.py` - Challenge model tests
- `test_challenge_schema.py` - Challenge schema validation

### 🌐 **API & Endpoints Tests**
- `test_api_endpoint.py` - Individual API endpoint testing
- `test_api_endpoints.py` - Comprehensive API testing suite
- `test_live_api.py` - Live production API testing
- `test_production_status.py` - Production deployment status verification

### 📚 **Documentation & Schema Tests**
- `test_json_schema.py` - JSON schema validation

### ⚙️ **Configuration & System Tests**
- `test_config.py` - Configuration validation and environment setup
- `test_django_system.py` - Django system integration
- `test_static_files.py` - Static file serving and collection
- `test_content.py` - Content rendering and templates

### 🔧 **Utility & Quick Tests**
- `test_quick.py` - Quick functionality tests
- `test_simple.py` - Simple integration tests
- `test_runner.py` - Enhanced test runner utilities
- `test_comment_fix.py` - Comment functionality and coin rewards

## Usage Examples

### Run All Tests
```bash
# Run the comprehensive test suite
python tests/test_runner.py

# Or use Django's test runner
python manage.py test tests/

# Or use pytest
pytest tests/
```

### Run Specific Test Categories
```bash
# Test AI functionality
python tests/test_ai_behavior_engine.py
python tests/test_ai_connection.py

# Test API endpoints
python tests/test_api_endpoints.py
python tests/test_live_api.py

# Test database operations
python tests/test_database_schema.py
python tests/test_django_models.py

# Test production deployment
python tests/test_production_status.py
```

### Quick Testing & Debugging
```bash
# Quick system check
python tests/test_quick.py

# Simple integration test
python tests/test_simple.py

# Configuration validation
python tests/test_config.py

# Static files verification
python tests/test_static_files.py
```

### Documentation & API Testing
```bash
# Test JSON schemas (if available)
python tests/test_json_schema.py

# Content and templates (if available)
python tests/test_content.py
```

## Test Environment Setup

Before running tests, ensure you have:

1. **Virtual Environment**: Activated Python virtual environment
2. **Dependencies**: All requirements installed (`pip install -r requirements.txt`)
3. **Environment Variables**: Proper `.env` file configuration
4. **Database**: Test database accessible (SQLite or Supabase)
5. **AI Service**: AI service endpoint configured and accessible

## Test Coverage

These tests provide comprehensive coverage of:
- ✅ **Time-consciousness features** - All 7 time periods and awareness
- ✅ **Gamification mechanics** - Coins, streaks, challenges, rewards
- ✅ **Database integrity** - Schema, models, relationships, queries
- ✅ **API functionality** - All endpoints, authentication, responses
- ✅ **AI integrations** - Behavior engine, mood analysis, recommendations
- ✅ **Documentation** - API schemas and endpoint documentation (Swagger available in development only)
- ✅ **Production readiness** - Deployment verification, performance
- ✅ **System configuration** - Settings, environment, static files

## Continuous Integration

These tests are designed to work with:
- Local development testing
- CI/CD pipeline integration
- Production health monitoring
- API documentation verification
- Automated deployment validation

## Adding New Tests

When adding new tests:
1. Follow the naming convention: `test_[functionality].py`
2. Include proper docstrings and comments
3. Add test description to this README in the appropriate category
4. Ensure tests are independent and can run in any order
5. Include both positive and negative test cases
