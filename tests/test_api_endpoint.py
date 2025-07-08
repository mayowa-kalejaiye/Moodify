import requests
import json

def test_api_endpoint():
    """Test if the behavior stats API endpoint works now"""
    try:
        # First check if the server is running
        response = requests.get('http://localhost:8000/api/behavior/stats/', timeout=5)
        print(f"Response status: {response.status_code}")
        
        if response.status_code == 200:
            data = response.json()
            print("Response data:", json.dumps(data, indent=2))
        else:
            print(f"Error response: {response.text}")
            
    except requests.exceptions.ConnectionError:
        print("Server is not running. Please start the Django server first.")
        print("Run: python manage.py runserver")
    except Exception as e:
        print(f"Error testing endpoint: {e}")

if __name__ == "__main__":
    test_api_endpoint()
