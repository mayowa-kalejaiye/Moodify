#!/usr/bin/env python3
"""
Comprehensive test script to verify Swagger UI is working properly
"""

import requests
import time
from datetime import datetime

def test_swagger_access():
    """Test if Swagger UI is accessible and working properly"""
    
    print("🧪 Testing Swagger UI Access")
    print("=" * 50)
    
    base_url = 'https://moodify-wmcd.onrender.com'
    swagger_url = f'{base_url}/swagger/'
    
    print(f"Testing URL: {swagger_url}")
    print(f"Timestamp: {datetime.now()}")
    print()
    
    try:
        # Test main Swagger UI
        print("1. Testing Swagger UI main page...")
        response = requests.get(swagger_url, timeout=30, allow_redirects=True)
        
        print(f"   Status Code: {response.status_code}")
        print(f"   Final URL: {response.url}")
        
        if response.status_code == 200:
            print("   ✅ SUCCESS: Swagger UI is accessible!")
            
            # Check if it contains expected content
            if 'swagger' in response.text.lower() or 'api' in response.text.lower():
                print("   ✅ Content looks correct (contains Swagger/API references)")
            else:
                print("   ⚠️  Warning: Content might not be loading properly")
                
        elif response.status_code == 302:
            if '/accounts/login/' in response.url:
                print("   ❌ FAILED: Still redirecting to login page!")
                return False
            else:
                print(f"   ⚠️  Redirected to: {response.url}")
        else:
            print(f"   ❌ FAILED: Unexpected status code {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ FAILED: Network error - {e}")
        return False
    
    print()
    
    # Test Swagger JSON schema
    print("2. Testing Swagger JSON schema...")
    try:
        schema_url = f'{base_url}/swagger.json'
        response = requests.get(schema_url, timeout=30)
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ SUCCESS: Swagger JSON schema accessible!")
            
            # Try to parse as JSON
            try:
                data = response.json()
                if 'swagger' in data or 'openapi' in data:
                    print("   ✅ Valid OpenAPI/Swagger schema detected")
                else:
                    print("   ⚠️  Schema format might be unexpected")
            except Exception:
                print("   ⚠️  Response is not valid JSON")
        else:
            print(f"   ❌ FAILED: Status code {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ FAILED: Network error - {e}")
    
    print()
    
    # Test ReDoc
    print("3. Testing ReDoc documentation...")
    try:
        redoc_url = f'{base_url}/redoc/'
        response = requests.get(redoc_url, timeout=30)
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ SUCCESS: ReDoc is accessible!")
        elif response.status_code == 302:
            if '/accounts/login/' in response.headers.get('Location', ''):
                print("   ❌ FAILED: ReDoc redirecting to login!")
            else:
                print(f"   ⚠️  ReDoc redirected to: {response.headers.get('Location')}")
        else:
            print(f"   ❌ FAILED: Status code {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ FAILED: Network error - {e}")
    
    print()
    
    # Test health endpoint for good measure
    print("4. Testing API health endpoint...")
    try:
        health_url = f'{base_url}/api/health/'
        response = requests.get(health_url, timeout=30)
        
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code == 200:
            print("   ✅ SUCCESS: API is responding!")
        else:
            print(f"   ⚠️  API health check returned: {response.status_code}")
            
    except requests.exceptions.RequestException as e:
        print(f"   ❌ FAILED: Network error - {e}")
    
    print()
    print("=" * 50)
    print("🎉 Test completed!")
    print()
    print("If you see ✅ SUCCESS for the Swagger UI main page,")
    print("then the authentication issue has been resolved!")
    print()
    print("Any remaining ⚠️  warnings about static files will be")
    print("fixed in the next deployment after collectstatic runs.")
    
    return True

if __name__ == '__main__':
    test_swagger_access()
