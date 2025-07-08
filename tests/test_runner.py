import os
import sys
import django
import unittest
from django.test.utils import setup_test_environment, teardown_test_environment

if __name__ == "__main__":
    # Add the project root to the Python path
    base_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, base_dir)
    
    # Set the correct Django settings module
    os.environ['DJANGO_SETTINGS_MODULE'] = 'mood_tracker.mood_tracker.settings'
    
    try:
        # Initialize Django
        django.setup()
        
        # Create a fresh test database if specified
        if '--reset-db' in sys.argv:
            print("Setting up fresh test database...")
            from django.core.management import call_command
            call_command('makemigrations')
            call_command('migrate')
            sys.argv.remove('--reset-db')
        
        # Set up test environment
        setup_test_environment()
        
        # Handle specific test case
        if '--comments-list-test' in sys.argv:
            print("Running only the list_comments test...")
            from mood_tracker.tracker.tests.test_comments_ai import CommentAPITests
            suite = unittest.TestSuite()
            suite.addTest(CommentAPITests('test_list_comments'))
            runner = unittest.TextTestRunner(verbosity=2)
            result = runner.run(suite)
            teardown_test_environment()
            sys.exit(bool(result.failures or result.errors))
        
        # Normal test execution
        from mood_tracker.tracker.tests.test_comments_ai import CommentAPITests, AISuggestionAPITests
        
        # Create a test loader
        loader = unittest.TestLoader()
        
        # Create a test suite
        suite = unittest.TestSuite()
        
        # Add test classes
        if '--comments' in sys.argv:
            suite.addTest(loader.loadTestsFromTestCase(CommentAPITests))
            sys.argv.remove('--comments')
        elif '--ai' in sys.argv:
            suite.addTest(loader.loadTestsFromTestCase(AISuggestionAPITests))
            sys.argv.remove('--ai')
        else:
            suite.addTest(loader.loadTestsFromTestCase(CommentAPITests))
            suite.addTest(loader.loadTestsFromTestCase(AISuggestionAPITests))
        
        # Run the tests
        print("\nRunning Comment and AI Suggestion tests...\n")
        runner = unittest.TextTestRunner(verbosity=2)
        result = runner.run(suite)
        
        # Clean up
        teardown_test_environment()
        
        # Exit with appropriate status code
        sys.exit(bool(result.failures or result.errors))
        
    except ImportError as e:
        print(f"ImportError: {e}")
        print("Make sure all required modules are installed and the project structure is correct.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
