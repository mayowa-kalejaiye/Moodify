"""
Helper script for running tests with different options.
"""
import os
import sys
import django
from django.conf import settings
from django.test.utils import get_runner

if __name__ == "__main__":
    # Add the project root to the Python path
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, base_dir)
    
    # Set up Django
    os.environ['DJANGO_SETTINGS_MODULE'] = 'mood_tracker.mood_tracker.settings'
    
    # Print some debug info
    print(f"Python path: {sys.path}")
    print(f"DJANGO_SETTINGS_MODULE: {os.environ.get('DJANGO_SETTINGS_MODULE')}")
    
    # Try to import the settings module directly
    try:
        from mood_tracker.mood_tracker import settings
        print(f"Successfully imported settings. INSTALLED_APPS: {settings.INSTALLED_APPS}")
    except ImportError as e:
        print(f"Error importing settings: {e}")
        sys.exit(1)
    
    django.setup()
    
    # List all available apps after Django is set up
    print("\nAvailable apps in Django registry:")
    from django.apps import apps
    for app_config in apps.get_app_configs():
        print(f"- {app_config.name} ({app_config.path})")
    
    # Get the test runner
    TestRunner = get_runner(settings)
    test_runner = TestRunner(verbosity=2, interactive=True)
    
    # Define which tests to run - adjust according to your structure
    test_labels = ['mood_tracker.tracker.tests']
    
    # Get any command line args
    if len(sys.argv) > 1:
        test_labels = sys.argv[1:]
    
    # Run the tests
    print(f"\nRunning tests: {test_labels}")
    failures = test_runner.run_tests(test_labels)
    sys.exit(bool(failures))
