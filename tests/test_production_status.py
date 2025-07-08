#!/usr/bin/env python3
"""
Quick Production Status Check

This script quickly checks if the production deployment is working
after the recent fixes.

Usage:
    python tests/test_production_status.py
"""
import requests
import time

def check_production_status():
    """Check production deployment status"""
    base_url = "https://moodify-wmcd.onrender.com"
    
    print("🌐 PRODUCTION STATUS CHECK")
    print("=" * 40)
    print(f"🔗 Testing: {base_url}")
    
    # Test basic connectivity
    try:
        print("\n🏠 Testing root endpoint...")
        response = requests.get(base_url, timeout=10)
        print(f"Root: {response.status_code} - {'✅ OK' if response.status_code == 200 else '❌ Error'}")
    except Exception as e:
        print(f"Root: ❌ Error - {e}")
    
    # Test Swagger
    try:
        print("\n📚 Testing Swagger UI...")
        response = requests.get(f"{base_url}/swagger/", timeout=10)
        print(f"Swagger: {response.status_code}")
        
        if response.status_code == 200:
            content = response.text.lower()
            if 'swagger' in content and 'api' in content:
                print("✅ Swagger UI is working correctly!")
            elif 'login' in content:
                print("❌ Still showing login page")
            else:
                print("⚠️ Page loaded but content unclear")
        elif response.status_code == 500:
            print("❌ Server error - deployment might still be in progress")
        else:
            print(f"❌ Unexpected status: {response.status_code}")
            
    except Exception as e:
        print(f"Swagger: ❌ Error - {e}")
    
    # Test ReDoc
    try:
        print("\n📖 Testing ReDoc...")
        response = requests.get(f"{base_url}/redoc/", timeout=10)
        print(f"ReDoc: {response.status_code} - {'✅ OK' if response.status_code == 200 else '❌ Error'}")
    except Exception as e:
        print(f"ReDoc: ❌ Error - {e}")
    
    print("\n🎯 SUMMARY:")
    print("If you see 500 errors, wait 2-3 minutes for deployment to complete")
    print("If authentication issues persist, check production logs")

if __name__ == "__main__":
    check_production_status()
