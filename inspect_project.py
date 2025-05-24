import os
import sys
import importlib

def print_directory_structure(startpath):
    """Print the directory structure recursively"""
    for root, dirs, files in os.walk(startpath):
        level = root.replace(startpath, '').count(os.sep)
        indent = ' ' * 4 * level
        print(f"{indent}{os.path.basename(root)}/")
        sub_indent = ' ' * 4 * (level + 1)
        for f in files:
            if f.endswith('.py'):  # Only show Python files
                print(f"{sub_indent}{f}")

def try_imports():
    """Try different import styles to see what works"""
    print("\nTrying different import styles:")
    
    import_paths = [
        'tracker',
        'mood_tracker.tracker',
        'mood_tracker.mood_tracker.tracker'
    ]
    
    for path in import_paths:
        try:
            module = importlib.import_module(path)
            print(f"✓ Successfully imported: {path}")
            print(f"  Module location: {module.__file__}")
        except ImportError as e:
            print(f"✗ Failed to import: {path}")
            print(f"  Error: {e}")

if __name__ == "__main__":
    print("Python version:", sys.version)
    print("\nPython path:")
    for p in sys.path:
        print(f"- {p}")
        
    base_dir = os.path.dirname(os.path.abspath(__file__))
    print(f"\nProject structure starting from: {base_dir}")
    print_directory_structure(base_dir)
    
    # Try to import Django settings
    print("\nTrying to import Django settings:")
    os.environ['DJANGO_SETTINGS_MODULE'] = 'mood_tracker.mood_tracker.settings'
    
    try:
        import django
        django.setup()
        print("✓ Django setup successful")
        
        from django.conf import settings
        print(f"INSTALLED_APPS: {settings.INSTALLED_APPS}")
    except Exception as e:
        print(f"✗ Django setup failed: {e}")
    
    try_imports()
