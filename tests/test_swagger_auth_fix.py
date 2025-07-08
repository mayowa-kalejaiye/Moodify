#!/usr/bin/env python3
"""
Test Swagger Authentication Fix

This script tests if the Swagger authentication issue is resolved
by checking the actual response from the production endpoint.

Usage:
    python tests/test_swagger_auth_fix.py
"""
import requests
from bs4 import BeautifulSoup

def test_swagger_authentication():
    """Test if Swagger UI loads without authentication redirect"""
    print("🔍 Testing Swagger Authentication Fix...")
    print("🌐 URL: https://moodify-wmcd.onrender.com/swagger/")
    
    try:
        # Test the swagger endpoint
        response = requests.get("https://moodify-wmcd.onrender.com/swagger/", timeout=15)
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📍 Final URL: {response.url}")
        
        if response.status_code == 200:
            # Check if we're actually on the swagger page
            content = response.text.lower()
            
            if 'swagger' in content and 'api' in content:
                print("✅ SUCCESS: Swagger UI loaded correctly!")
                print("✅ No authentication redirect detected")
                return True
            elif 'login' in content or 'django administration' in content:
                print("❌ FAILED: Still redirecting to login page")
                print("🔧 The page contains login elements")
                return False
            else:
                print("⚠️  UNCLEAR: Page loaded but content unclear")
                print("📝 First 200 characters of response:")
                print(response.text[:200])
                return False
                
        elif response.status_code == 302 or response.status_code == 301:
            print("❌ FAILED: Redirect detected")
            print(f"🔗 Redirecting to: {response.headers.get('Location', 'Unknown')}")
            return False
        else:
            print(f"❌ FAILED: HTTP {response.status_code}")
            print(f"📝 Response: {response.text[:200]}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ NETWORK ERROR: {e}")
        return False

def test_redoc_authentication():
    """Test if ReDoc loads without authentication redirect"""
    print("\n🔍 Testing ReDoc Authentication...")
    print("🌐 URL: https://moodify-wmcd.onrender.com/redoc/")
    
    try:
        response = requests.get("https://moodify-wmcd.onrender.com/redoc/", timeout=15)
        
        print(f"📊 Status Code: {response.status_code}")
        print(f"📍 Final URL: {response.url}")
        
        if response.status_code == 200:
            content = response.text.lower()
            if 'redoc' in content and 'api' in content:
                print("✅ SUCCESS: ReDoc loaded correctly!")
                return True
            elif 'login' in content:
                print("❌ FAILED: Still redirecting to login page")
                return False
            else:
                print("⚠️  UNCLEAR: Page loaded but content unclear")
                return False
        else:
            print(f"❌ FAILED: HTTP {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ NETWORK ERROR: {e}")
        return False

def main():
    """Main test function"""
    print("🧪 SWAGGER AUTHENTICATION FIX TEST")
    print("=" * 50)
    print("🎯 Testing if Swagger UI is accessible without login")
    print("📝 Note: Changes need to be deployed to take effect")
    print()
    
    # Test Swagger UI
    swagger_success = test_swagger_authentication()
    
    # Test ReDoc
    redoc_success = test_redoc_authentication()
    
    # Summary
    print("\n" + "=" * 50)
    print("📊 FINAL RESULTS:")
    print(f"  Swagger UI: {'✅ Working' if swagger_success else '❌ Still broken'}")
    print(f"  ReDoc:      {'✅ Working' if redoc_success else '❌ Still broken'}")
    
    if swagger_success and redoc_success:
        print("\n🎉 SUCCESS! Both documentation interfaces are working!")
        print("🌐 Swagger UI: https://moodify-wmcd.onrender.com/swagger/")
        print("📚 ReDoc:      https://moodify-wmcd.onrender.com/redoc/")
    elif not swagger_success and not redoc_success:
        print("\n❌ BOTH interfaces still have authentication issues")
        print("🔧 Next steps:")
        print("  1. Deploy the updated code with authentication_classes=[]")
        print("  2. Check if the deployment picked up the changes")
        print("  3. Verify the schema_view configuration")
    else:
        print("\n⚠️  Mixed results - some interfaces working, others not")
    
    print("\n💡 If still not working after deployment:")
    print("  - Check production logs")
    print("  - Verify no middleware is intercepting requests")
    print("  - Consider adding LOGIN_URL setting to avoid /accounts/login/ redirect")

if __name__ == "__main__":
    main()
