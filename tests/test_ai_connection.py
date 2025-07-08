#!/usr/bin/env python3
"""
AI Service Connection Test

This script validates connectivity and functionality of the AI service endpoints
used by the MoodSync application. It tests all major endpoints including:
- /motivation - Motivation suggestions
- /habits - Habit improvement recommendations  
- /generate-nudge - Personalized nudges
- /generate-insights - Mood insights generation

Usage:
    python tests/test_ai_connection.py

Environment:
    Requires AI_SERVICE_URL to be set in .env file
"""
import os
import requests
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

def test_ai_service():
    ai_service_url = os.environ.get('AI_SERVICE_URL', 'http://127.0.0.1:5001')
    print(f"Testing AI service at: {ai_service_url}")
    
    # Test motivation endpoint (this is what your app actually uses)
    try:
        print("Testing motivation endpoint...")
        payload = {
            "mood_score": 5,
            "energy_level": 3,
            "stress_level": 7,
            "activities": ["work", "exercise"],
            "goals": ["improve mood", "reduce stress"]
        }
        response = requests.post(f"{ai_service_url}/motivation", json=payload, timeout=15)
        print(f"Motivation endpoint status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print("✅ Motivation endpoint working!")
            print(f"Sample response: {result.get('suggestion', 'No suggestion')[:100]}...")
        else:
            print(f"❌ Motivation endpoint failed: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Error testing motivation endpoint: {e}")

    # Test habits endpoint
    try:
        print("\nTesting habits endpoint...")
        payload = {
            "current_habits": ["morning walk", "meditation"],
            "goals": ["better sleep", "more energy"],
            "mood_trends": ["stress", "tired"]
        }
        response = requests.post(f"{ai_service_url}/habits", json=payload, timeout=15)
        print(f"Habits endpoint status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print("✅ Habits endpoint working!")
            print(f"Sample response: {result.get('suggestions', 'No suggestions')[:100]}...")
        else:
            print(f"❌ Habits endpoint failed: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Error testing habits endpoint: {e}")

    # Test generate-nudge endpoint
    try:
        print("\nTesting generate-nudge endpoint...")
        payload = {
            "user_profile": {"name": "Test User", "preferences": ["short messages"]},
            "context": {"current_mood": "neutral", "time_of_day": "afternoon"}
        }
        response = requests.post(f"{ai_service_url}/generate-nudge", json=payload, timeout=15)
        print(f"Generate-nudge endpoint status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print("✅ Generate-nudge endpoint working!")
            print(f"Sample response: {result.get('nudge', 'No nudge')[:100]}...")
        else:
            print(f"❌ Generate-nudge endpoint failed: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Error testing generate-nudge endpoint: {e}")

    # Test generate-insights endpoint
    try:
        print("\nTesting generate-insights endpoint...")
        payload = {
            "mood_data": [{"date": "2025-01-01", "mood": 7, "energy": 5}],
            "timeframe": "week"
        }
        response = requests.post(f"{ai_service_url}/generate-insights", json=payload, timeout=15)
        print(f"Generate-insights endpoint status: {response.status_code}")
        if response.status_code == 200:
            result = response.json()
            print("✅ Generate-insights endpoint working!")
            print(f"Sample response: {result.get('insights', 'No insights')[:100]}...")
        else:
            print(f"❌ Generate-insights endpoint failed: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Error testing generate-insights endpoint: {e}")

    # Test root endpoint to see what's available
    try:
        print("\nTesting root endpoint...")
        response = requests.get(ai_service_url, timeout=10)
        print(f"Root endpoint status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Root endpoint accessible!")
            print(f"Response: {response.text[:200]}...")
        else:
            print(f"Root endpoint status: {response.status_code}")
            print(f"Response: {response.text[:200]}...")
    except Exception as e:
        print(f"❌ Error testing root endpoint: {e}")

if __name__ == "__main__":
    test_ai_service()
