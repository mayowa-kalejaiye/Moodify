"""
Test to verify Swagger UI is publicly accessible
"""
import requests
import pytest
from django.test import TestCase, Client
from django.urls import reverse


class SwaggerAccessTest(TestCase):
    """Test that Swagger UI is publicly accessible without authentication"""
    
    def setUp(self):
        self.client = Client()
    
    def test_swagger_ui_accessible(self):
        """Test that Swagger UI can be accessed without authentication"""
        response = self.client.get('/swagger/')
        
        # Should NOT redirect to login page
        self.assertNotEqual(response.status_code, 302)
        
        # Should be successful or redirect to Swagger UI
        self.assertIn(response.status_code, [200, 301])
        
        # Should not contain login redirect
        if response.status_code == 302:
            redirect_location = response.get('Location', '')
            self.assertNotIn('/accounts/login/', redirect_location)
            self.assertNotIn('login', redirect_location.lower())
    
    def test_swagger_json_accessible(self):
        """Test that Swagger JSON schema is accessible"""
        response = self.client.get('/swagger.json')
        
        # Should be successful
        self.assertIn(response.status_code, [200, 301])
        
        # Should not redirect to login
        if response.status_code == 302:
            redirect_location = response.get('Location', '')
            self.assertNotIn('/accounts/login/', redirect_location)
    
    def test_redoc_accessible(self):
        """Test that ReDoc is accessible without authentication"""
        response = self.client.get('/redoc/')
        
        # Should NOT redirect to login page
        self.assertNotEqual(response.status_code, 302)
        
        # Should be successful
        self.assertIn(response.status_code, [200, 301])
        
        # Should not contain login redirect
        if response.status_code == 302:
            redirect_location = response.get('Location', '')
            self.assertNotIn('/accounts/login/', redirect_location)
            self.assertNotIn('login', redirect_location.lower())


def test_production_swagger_access():
    """Test production Swagger access"""
    try:
        url = 'https://moodify-wmcd.onrender.com/swagger/'
        
        # Make request without authentication
        response = requests.get(url, allow_redirects=False, timeout=30)
        
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {dict(response.headers)}")
        
        if response.status_code == 302:
            location = response.headers.get('Location', '')
            print(f"Redirect Location: {location}")
            
            # Check if it's redirecting to login
            if '/accounts/login/' in location or '/login' in location:
                print("❌ STILL REDIRECTING TO LOGIN!")
                return False
            else:
                print("✅ Redirecting but not to login page")
        elif response.status_code == 200:
            print("✅ SUCCESS: Swagger UI accessible directly")
            return True
        else:
            print(f"❌ Unexpected status code: {response.status_code}")
            return False
            
    except Exception as e:
        print(f"❌ Error accessing Swagger: {e}")
        return False


if __name__ == '__main__':
    test_production_swagger_access()
