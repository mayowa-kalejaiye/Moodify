#!/usr/bin/env python3
"""
Live API Test for Time-of-Day Consciousness
==========================================

This script tests the actual API endpoints to verify time-awareness.
"""

import requests
import json
from datetime import datetime

def test_time_aware_api():
    """Test the time-aware API endpoints"""
    base_url = "http://localhost:8000"
    
    print("🚀 TESTING LIVE TIME-AWARE API ENDPOINTS")
    print("=" * 60)
    
    # Test time-aware mood suggestions
    print("\n1. 📊 TESTING MOOD SUGGESTIONS (Time-Aware)")
    print("-" * 40)
    
    try:
        response = requests.get(f"{base_url}/api/moods/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {response.status_code}")
            print(f"🎯 Time Period: {data.get('time_context', {}).get('period', 'N/A')}")
            print(f"👋 Greeting: {data.get('time_context', {}).get('greeting', 'N/A')}")
            print(f"🎭 Suggested Moods: {data.get('suggested_moods', [])}")
            print(f"🏃 Suggested Activities: {data.get('suggested_activities', [])}")
            print(f"⚡ Energy Level: {data.get('time_context', {}).get('energy_level', 'N/A')}")
        else:
            print(f"❌ Failed with status: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Error testing mood suggestions: {e}")
    
    # Test time-aware motivation
    print("\n2. 💪 TESTING MOTIVATION SUGGESTIONS (Time-Aware)")
    print("-" * 40)
    
    try:
        test_data = {
            "mood_trend": "positive",
            "recent_moods": ["happy", "motivated"]
        }
        
        response = requests.post(f"{base_url}/api/suggestions/motivation/", 
                               json=test_data,
                               headers={'Content-Type': 'application/json'})
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {response.status_code}")
            print(f"💬 Message: {data.get('message', 'N/A')}")
            print(f"🎯 Type: {data.get('type', 'N/A')}")
            print(f"⏰ Time Context: {data.get('time_context', {})}")
        else:
            print(f"❌ Failed with status: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Error testing motivation: {e}")
    
    # Test time-aware nudges
    print("\n3. 🔔 TESTING NUDGE GENERATION (Time-Aware)")
    print("-" * 40)
    
    try:
        response = requests.get(f"{base_url}/api/nudges/next/")
        if response.status_code == 200:
            data = response.json()
            print(f"✅ Status: {response.status_code}")
            print(f"💬 Message: {data.get('message', 'N/A')}")
            print(f"🎭 Tone: {data.get('tone', 'N/A')}")
            print(f"🎯 Type: {data.get('nudge_type', 'N/A')}")
        else:
            print(f"❌ Failed with status: {response.status_code}")
            print(f"Response: {response.text}")
    except Exception as e:
        print(f"❌ Error testing nudges: {e}")
    
    print("\n" + "=" * 60)
    print("🎯 TIME-AWARE API TESTING COMPLETE")
    print(f"⏰ Current Time: {datetime.now().strftime('%I:%M %p')}")
    print("💡 All endpoints should reflect current time-of-day context!")

if __name__ == "__main__":
    test_time_aware_api()
