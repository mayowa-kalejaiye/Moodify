# A simple test script to verify basic functionality without Django's test runner

import requests
import json
import subprocess
import time
import os
import sys

def run_server():
    """Start Django development server in a subprocess"""
    server = subprocess.Popen([
        "python", "manage.py", "runserver", "8000"
    ])
    time.sleep(5)  # Give the server time to start
    return server

def stop_server(server):
    """Stop the Django server"""
    server.terminate()
    server.wait()

def test_api_endpoints():
    """Test basic API functionality"""
    print("Testing API endpoints...")
    
    # Test the API root endpoint
    response = requests.get("http://localhost:8000/api/")
    if response.status_code == 200:
        print("✓ API root endpoint works")
    else:
        print(f"✗ API root endpoint failed: {response.status_code}")
    
    # Test health check endpoint
    response = requests.get("http://localhost:8000/api/health/")
    if response.status_code == 200:
        print("✓ Health check endpoint works")
    else:
        print(f"✗ Health check endpoint failed: {response.status_code}")
    
    # You can add more basic tests here

if __name__ == "__main__":
    print("Starting test server...")
    server = run_server()
    
    try:
        test_api_endpoints()
    finally:
        print("\nStopping test server...")
        stop_server(server)
