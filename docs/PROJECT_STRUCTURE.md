# 📁 MoodSync Project Structure

## 🏗️ **Root Directory Overview**

```
mood_tracker/
├── 📄 README.md                    # Main project overview (MoodSync 2.0)
├── 📄 LICENSE                      # MIT License
├── 📄 requirements.txt             # Python dependencies
├── 📄 manage.py                    # Django management utility
├── 📄 Dockerfile                   # Docker container configuration
├── 📄 docker-compose.yml           # Docker Compose setup
├── 📄 Procfile                     # Heroku deployment config
├── 📄 pytest.ini                   # Pytest configuration
├── 📄 api_examples.md              # API usage examples
├── 📄 generate_secret_key.py       # Django secret key generator
├── 📄 .env.example                 # Environment variables template
├── 📁 mood_tracker/                # Main Django project
├── 📁 ai_service/                  # AI microservice
├── 📁 staticfiles/                 # Collected static files
├── 📁 docs/                        # Documentation
├── 📁 tests/                       # Development tests
├── 📁 tools/                       # Development utilities
├── 📁 scripts/                     # Utility scripts
└── 📁 venv/                        # Virtual environment (local)
```

## 📚 **Directory Purposes**

### 🎯 **Core Application**
- **`mood_tracker/`** - Main Django project with behavior engine
- **`ai_service/`** - Separate AI microservice for advanced processing
- **`staticfiles/`** - Production static files (CSS, JS, images)

### 📖 **Documentation**
- **`docs/`** - Comprehensive project documentation
- **`docs/BEHAVIOR_ENGINE.md`** - Complete technical specifications
- **`docs/summaries/`** - Development history and implementation guides

### 🧪 **Testing & Development**
- **`tests/`** - Organized development tests for validation
- **`tools/`** - Debugging utilities and development tools
- **`scripts/`** - Database management and deployment scripts

### ⚙️ **Configuration**
- **`.env.example`** - Environment variables template
- **`requirements.txt`** - Python package dependencies
- **`docker-compose.yml`** - Complete development environment setup

## 🎯 **Quick Start Paths**

### For Users
1. Read `README.md` for platform overview
2. Check `docs/` for detailed documentation

### For Developers
1. Follow setup in `README.md`
2. Review `docs/BEHAVIOR_ENGINE.md` for technical details
3. Use `scripts/` for database setup
4. Run `tests/` for validation

### For Deployment
1. Use `Dockerfile` for containerization
2. Configure with `.env` variables
3. Run with `docker-compose.yml`

## 🧹 **Clean Structure Benefits**

- ✅ **Organized**: Clear separation of concerns
- ✅ **Maintainable**: Easy to find and update components
- ✅ **Professional**: Production-ready structure
- ✅ **Scalable**: Room for future expansion
- ✅ **Documented**: Comprehensive documentation at every level

## 🔄 **Git Workflow Ready**

This clean structure is optimized for:
- **Branch management**: Clear feature separation
- **Code reviews**: Organized file changes
- **Collaboration**: Easy onboarding for new developers
- **Release management**: Clean version control
