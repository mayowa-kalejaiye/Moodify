# Simple script to check if imports work correctly

try:
    import mood_tracker.mood_tracker.settings
    print("Successfully imported settings")
    
    import mood_tracker.tracker
    print("Successfully imported tracker app")
    
    print("All imports successful! Your module structure seems correct.")
except ImportError as e:
    print(f"Import error: {e}")
    print("\nTroubleshooting suggestions:")
    print("1. Ensure all directories have __init__.py files")
    print("2. Check that your virtualenv is activated")
    print("3. Verify PYTHONPATH includes the project root directory")
