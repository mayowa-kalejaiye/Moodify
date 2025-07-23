# 📁 MoodSync Project Structure

## 🏗️ **Root Directory Overview**

```
moodify/
├── 📄 README.md                    # Main project overview
├── 📄 LICENSE                      # MIT License
├── 📄 requirements.txt             # Python dependencies
├── 📄 manage.py                    # Django management utility
├── 📄 Dockerfile                   # Docker container configuration
├── 📄 docker-compose.yml           # Docker Compose setup
├── 📄 Procfile                     # Heroku/Render deployment config
├── 📄 pytest.ini                   # Pytest configuration
├── 📄 .env                         # Environment variables (not in version control)
├── � CODEBASE_CLEANUP_REPORT.md   # Latest cleanup documentation
├── �📁 mood_tracker/                # Main Django project
├── 📁 staticfiles/                 # Collected static files
├── 📁 docs/                        # Documentation
│   ├── 📄 api_examples.md          # API usage examples
│   ├── 📄 BEHAVIOR_ENGINE.md       # Behavior engine technical details
│   ├── 📄 DEPLOYMENT.md            # Deployment instructions
│   ├── 📄 PSYCHOLOGICAL_FOUNDATIONS.md # Theory behind features
│   ├── 📄 PROJECT_STRUCTURE.md     # This file
│   ├── 📄 README.md                # Documentation overview
│   └── 📁 summaries/               # Development summaries
├── 📁 postman/                     # Postman configuration files
│   ├── 📄 postman-collections-post-response.instructions.md
│   ├── 📄 postman-collections-pre-request.instructions.md
│   ├── 📄 postman-folder-post-response.instructions.md
│   ├── 📄 postman-folder-pre-request.instructions.md
│   ├── 📄 postman-http-request-post-response.instructions.md
│   └── 📄 postman-http-request-pre-request.instructions.md
├── 📁 tests/                       # All test files
│   ├── 📄 test_ai_behavior_engine.py
│   ├── 📄 test_api_endpoints.py
│   ├── 📄 test_behavior_engine.py
│   ├── 📄 test_database_schema.py
│   ├── 📄 test_time_consciousness.py
│   ├── 📄 final_schema_test.py
│   ├── 📄 profile_update_test.py
│   ├── 📄 simple_django_test.py
│   └── 📄 README.md                # Testing guidelines
├── 📁 tools/                       # Development tools
│   ├── 📄 comprehensive_schema_check.py
│   ├── 📄 demo_time_consciousness.py
│   ├── 📄 inspect_project.py
│   ├── 📄 clean_swagger.py         # Swagger cleanup script
│   ├── 📄 clean_swagger_careful.py # Careful Swagger cleanup
│   ├── 📄 comment_swagger.py       # Swagger comment script
│   ├── 📄 fix_views.py             # Views repair utility
│   ├── 📄 FINAL_RESOLUTION_COMPLETE.py
│   ├── 📄 FINAL_RESOLUTION_REPORT.py
│   ├── 📄 README.md                # Tools documentation
│   └── 📁 legacy/                  # Deprecated tools
└── 📁 scripts/                     # Utility scripts
    ├── 📄 create_migration.py      # Migration helper
    ├── 📄 generate_secret_key.py   # Secret key generator
    ├── 📄 setup_test_db.py         # Test database setup
    ├── 📄 run_tests.py             # Test runner script
    ├── 📄 setup_production_db.py   # Production database setup
    ├── 📄 quick_migrate.py         # Quick migration utility
    └── 📄 README.md                # Scripts documentation
```

## 📚 **Directory Purposes**

### 🎯 **Core Application**
- **`mood_tracker/`** - Main Django project with all application code
  - **`mood_tracker/mood_tracker/`** - Django project settings
  - **`mood_tracker/tracker/`** - Main app with models, views, etc.
- **`staticfiles/`** - Production static files (CSS, JS, images)

### 📖 **Documentation**
- **`docs/`** - Comprehensive project documentation
  - **`API_DOCUMENTATION.md`** - Complete API documentation
  - **`BEHAVIOR_ENGINE.md`** - Technical details of the behavior engine
  - **`DEPLOYMENT.md`** - Deployment instructions
  - **`PROJECT_STRUCTURE.md`** - Project structure documentation
  - **`PSYCHOLOGICAL_FOUNDATIONS.md`** - Theory behind features
  - **`SUPABASE_SETUP.md`** - Database setup guide
  - **`summaries/`** - Development history and implementation guides
  - **`postman/`** - API examples and Postman collections

### 🧪 **Testing & Development**
- **`tests/`** - All test files for validating application functionality
- **`tools/`** - Debugging utilities and development tools
- **`scripts/`** - Database management and deployment scripts

### ⚙️ **Configuration**
- **`.env`** - Environment variables (not in version control)
- **`requirements.txt`** - Python package dependencies
- **`docker-compose.yml`** - Development environment setup
- **`Dockerfile`** - Container configuration

## 🔍 **Main Application Structure**

### 🗂️ **Models**
- **`mood_tracker/tracker/models.py`** - Data models including:
  - **`Mood`** - Core mood entries
  - **`Comment`** - Reflective comments on moods
  - **`Profile`** - Extended user profiles
  - **`Challenge`** - Behavior challenges
  - **`CoinTransaction`** - Coin economy system
  - **`Nudge`** - Contextual reminders

### 🖥️ **Views**
- **`mood_tracker/tracker/views.py`** - API views including:
  - Authentication (registration, login, logout)
  - Mood tracking (creation, history, analysis)
  - Profile management
  - Behavior engine features

### 🔌 **APIs**
- **`mood_tracker/tracker/urls.py`** - API endpoint definitions
- **`mood_tracker/tracker/serializers.py`** - Data serialization/deserialization

### 🧠 **Behavior Engine**
- **`mood_tracker/tracker/time_context.py`** - Time-awareness system
- Task scheduling and behavior reinforcement logic

## 🚀 **Development Workflow**

1. **Setup Environment**
   ```bash
   # Clone repository
   git clone https://github.com/yourusername/moodify.git
   cd moodify

   # Create virtual environment
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate

   # Install dependencies
   pip install -r requirements.txt

   # Configure environment
   cp .env.example .env  # Then edit .env with your settings
   ```

2. **Database Setup**
   ```bash
   # Setup local database
   python scripts/setup_test_db.py

   # Run migrations
   python manage.py migrate
   ```

3. **Run Development Server**
   ```bash
   python manage.py runserver
   ```

4. **Running Tests**
   ```bash
   # Run all tests
   python scripts/run_tests.py

   # Run specific tests
   pytest tests/test_api_endpoints.py
   ```
