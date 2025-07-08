#!/usr/bin/env python3
"""
Test static file serving for Swagger UI
"""

import requests
from urllib.parse import urljoin

def test_static_files():
    """Test if static files are being served properly"""
    
    print("🔍 Testing Static File Serving")
    print("=" * 40)
    
    base_url = 'https://moodify-wmcd.onrender.com'
    
    # List of critical static files for Swagger UI
    static_files = [
        '/static/drf-yasg/swagger-ui-dist/swagger-ui.css',
        '/static/drf-yasg/swagger-ui-dist/swagger-ui-bundle.js',
        '/static/drf-yasg/swagger-ui-dist/swagger-ui-standalone-preset.js',
        '/static/drf-yasg/style.css',
    ]
    
    print(f"Base URL: {base_url}")
    print()
    
    working_files = 0
    total_files = len(static_files)
    
    for static_file in static_files:
        full_url = urljoin(base_url, static_file)
        
        try:
            response = requests.get(full_url, timeout=15)
            
            if response.status_code == 200:
                print(f"✅ {static_file} - OK")
                working_files += 1
            else:
                print(f"❌ {static_file} - Status: {response.status_code}")
                
        except requests.exceptions.RequestException as e:
            print(f"❌ {static_file} - Error: {e}")
    
    print()
    print(f"📊 Results: {working_files}/{total_files} static files working")
    
    if working_files == total_files:
        print("🎉 All static files are working! Swagger UI should display properly.")
    elif working_files > 0:
        print("⚠️  Some static files are working. Swagger UI might work partially.")
    else:
        print("❌ No static files are working. Swagger UI will be blank.")
        print("💡 This means we need to debug the static file serving configuration.")
    
    return working_files == total_files

if __name__ == '__main__':
    test_static_files()
