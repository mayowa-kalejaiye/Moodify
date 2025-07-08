# 🧪 Tests Directory

This directory contains various test files used during development and validation of the MoodSync behavior engine.

## Test Categories

### 🔧 **Core Functionality Tests**
- `test_time_consciousness.py` - Validates time-aware features across all 7 periods
- `test_behavior_engine.py` - Tests gamification mechanics (coins, streaks, challenges)
- `test_comment_fix.py` - Validates comment system and coin rewards

### 🌐 **API Tests**
- `test_api_endpoints.py` - Comprehensive API endpoint testing
- `test_live_api.py` - Live API integration tests
- `test_runner.py` - Custom test runner with enhanced features

### 🗄️ **Database Tests**
- `test_database_schema.py` - Schema validation and integrity tests
- `test_django_models.py` - Model relationship and validation tests
- `test_challenge_schema.py` - Challenge model specific tests

### 🤖 **AI Integration Tests**
- `test_ai_behavior_engine.py` - AI service integration validation

### 🔗 **Configuration & Connectivity Tests**
- `test_ai_connection.py` - Validates AI service endpoints and connectivity
- `test_config.py` - Tests Django configuration and environment setup
- `test_swagger_access.py` - Tests Swagger/API documentation accessibility
- `test_swagger_auth_fix.py` - Verifies Swagger authentication fix works

## Running Tests

### Configuration Tests
```bash
# Test AI service connectivity
python tests/test_ai_connection.py

# Test Django configuration
python tests/test_config.py

# Test Swagger API documentation access
python tests/test_swagger_access.py

# Verify Swagger authentication fix
python tests/test_swagger_auth_fix.py
```

### Individual Tests
```bash
# Run specific test file
python manage.py test tests.test_time_consciousness

# Run with custom runner
python tests/test_runner.py --reset-db
```

### All Tests
```bash
# Run all tests in this directory
python manage.py test tests/

# Or use pytest
pytest tests/
```

## Test Coverage

These tests provide comprehensive coverage of:
- ✅ Time-consciousness features
- ✅ Gamification mechanics  
- ✅ Database integrity
- ✅ API functionality
- ✅ AI integrations

**Note**: These are development tests. The main Django app tests are located in `mood_tracker/tracker/tests/`.
