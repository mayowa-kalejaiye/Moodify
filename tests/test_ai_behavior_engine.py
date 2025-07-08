#!/usr/bin/env python3
"""
AI-Powered Behavior Engine Test Script
Tests the dynamic message generation and AI integration
"""

import os
import sys
import django
from datetime import date, timedelta
import requests
import json

# Add the project directory to the Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'mood_tracker'))

# Set up Django settings
os.environ.setdefault('DJANGO_SECRET_KEY', 'test-key-12345')
os.environ.setdefault('DEBUG', 'True')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mood_tracker.mood_tracker.settings')

try:
    django.setup()
except Exception as e:
    print(f"❌ Django setup failed: {e}")
    sys.exit(1)

# Import Django models and utilities
from django.contrib.auth.models import User
from django.test import Client
from django.urls import reverse
from mood_tracker.tracker.models import Profile, Mood, Challenge, CoinTransaction, Nudge
from mood_tracker.tracker.views import NudgeView

def test_ai_service_connection():
    """Test connection to AI service"""
    print("\n🤖 Testing AI Service Connection...")
    
    try:
        # Test AI service health
        response = requests.get('http://localhost:5001/list-models', timeout=5)
        if response.status_code == 200:
            print("✅ AI service is running and accessible")
            models = response.json()
            print(f"   Available models: {len(models.get('available_models_for_generateContent', []))}")
            return True
        else:
            print(f"⚠️  AI service returned status {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ AI service connection failed: {e}")
        print("   Make sure the AI service is running on localhost:5001")
        return False

def test_ai_nudge_generation():
    """Test AI-powered nudge generation"""
    print("\n💬 Testing AI Nudge Generation...")
    
    try:
        # Create test context
        context = {
            'user_age': 25,
            'streak_count': 5,
            'coin_balance': 25,
            'tone': 'gen_z',
            'recent_moods': [
                {'mood': 'happy', 'rating': 4, 'notes': 'Great day at work', 'date': '2025-01-07'},
                {'mood': 'tired', 'rating': 3, 'notes': 'Long day', 'date': '2025-01-06'},
                {'mood': 'excited', 'rating': 5, 'notes': 'Got promoted!', 'date': '2025-01-05'}
            ]
        }
        
        payload = {
            'prompt_type': 'nudge_message',
            'context': context,
            'max_length': 150
        }
        
        response = requests.post(
            'http://localhost:5001/generate-nudge',
            json=payload,
            timeout=15
        )
        
        if response.status_code == 200:
            result = response.json()
            message = result.get('message', 'No message generated')
            tone = result.get('tone', 'unknown')
            
            print(f"✅ AI nudge generated successfully")
            print(f"   Tone: {tone}")
            print(f"   Message: {message}")
            print(f"   Length: {len(message)} characters")
            return True
        else:
            print(f"❌ AI nudge generation failed with status {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ AI nudge generation request failed: {e}")
        return False

def test_ai_challenge_message():
    """Test AI-powered challenge completion messages"""
    print("\n🏆 Testing AI Challenge Messages...")
    
    try:
        # Test completion message
        context = {
            'challenge_type': 'daily_log',
            'stake': 20,
            'duration_days': 7,
            'user_age': 28,
            'completed': True,
            'tone': 'gen_z'
        }
        
        payload = {
            'prompt_type': 'challenge_completion',
            'context': context,
            'max_length': 200
        }
        
        response = requests.post(
            'http://localhost:5001/generate-challenge-message',
            json=payload,
            timeout=15
        )
        
        if response.status_code == 200:
            result = response.json()
            message = result.get('message', 'No message generated')
            completed = result.get('completed', False)
            
            print(f"✅ AI challenge message generated successfully")
            print(f"   Completed: {completed}")
            print(f"   Message: {message}")
            return True
        else:
            print(f"❌ AI challenge message generation failed with status {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ AI challenge message generation request failed: {e}")
        return False

def test_ai_mood_insights():
    """Test AI-powered mood insights"""
    print("\n🧠 Testing AI Mood Insights...")
    
    try:
        # Create comprehensive mood data
        mood_data = [
            {'date': '2025-01-07', 'mood': 'happy', 'rating': 4, 'notes': 'Great presentation at work', 'activities': 'work,exercise'},
            {'date': '2025-01-06', 'mood': 'tired', 'rating': 3, 'notes': 'Long day', 'activities': 'work,commute'},
            {'date': '2025-01-05', 'mood': 'excited', 'rating': 5, 'notes': 'Got promoted!', 'activities': 'work,celebration'},
            {'date': '2025-01-04', 'mood': 'anxious', 'rating': 2, 'notes': 'Worried about meeting', 'activities': 'work,meditation'},
            {'date': '2025-01-03', 'mood': 'calm', 'rating': 4, 'notes': 'Relaxing weekend', 'activities': 'reading,nature'},
        ]
        
        context = {
            'user_age': 30,
            'analysis_period': 30,
            'mood_data': mood_data,
            'avg_rating': 3.6,
            'total_entries': 5,
            'streak_count': 10,
            'tone': 'professional'
        }
        
        payload = {
            'prompt_type': 'mood_insights',
            'context': context
        }
        
        response = requests.post(
            'http://localhost:5001/generate-insights',
            json=payload,
            timeout=20
        )
        
        if response.status_code == 200:
            result = response.json()
            insights = result.get('insights', [])
            recommendations = result.get('recommendations', [])
            mood_trends = result.get('mood_trends', 'No trends available')
            
            print(f"✅ AI mood insights generated successfully")
            print(f"   Insights: {len(insights)}")
            for i, insight in enumerate(insights, 1):
                print(f"     {i}. {insight}")
            print(f"   Recommendations: {len(recommendations)}")
            for i, rec in enumerate(recommendations, 1):
                print(f"     {i}. {rec}")
            print(f"   Trends: {mood_trends}")
            return True
        else:
            print(f"❌ AI mood insights generation failed with status {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"❌ AI mood insights generation request failed: {e}")
        return False

def test_behavior_engine_integration():
    """Test integration between behavior engine and AI system"""
    print("\n🔗 Testing Behavior Engine + AI Integration...")
    
    try:
        # Create a test user
        user, created = User.objects.get_or_create(
            username='ai_test_user',
            defaults={'email': 'ai_test@example.com'}
        )
        
        # Get or create profile
        profile, created = Profile.objects.get_or_create(
            user=user,
            defaults={
                'age': 26,
                'coin_balance': 30,
                'streak_count': 3,
                'clarity_score': 85
            }
        )
        
        # Create some test moods
        test_moods = [
            {'mood': 'happy', 'rating': 4, 'notes': 'Good day with friends'},
            {'mood': 'stressed', 'rating': 2, 'notes': 'Work deadline approaching'},
            {'mood': 'calm', 'rating': 4, 'notes': 'Meditation helped'},
        ]
        
        for mood_data in test_moods:
            Mood.objects.create(
                user=user,
                **mood_data
            )
        
        # Test dynamic nudge generation
        nudge_view = NudgeView()
        nudge = nudge_view._generate_contextual_nudge(profile)
        
        if nudge:
            print(f"✅ Dynamic nudge generated")
            print(f"   Type: {nudge.nudge_type}")
            print(f"   Tone: {nudge.tone}")
            print(f"   Message: {nudge.message}")
            
            # Test challenge completion message
            challenge = Challenge.objects.create(
                profile=profile,
                challenge_type='daily_log',
                stake=15,
                start_date=date.today() - timedelta(days=7),
                end_date=date.today(),
                completed=True
            )
            
            completion_message = challenge.get_completion_message()
            print(f"✅ Challenge completion message: {completion_message}")
            
            return True
        else:
            print("❌ No nudge generated")
            return False
            
    except Exception as e:
        print(f"❌ Behavior engine integration test failed: {e}")
        return False

def run_all_tests():
    """Run all AI-powered behavior engine tests"""
    print("🎯 AI-Powered MoodSync Behavior Engine Test Suite")
    print("="*60)
    
    results = []
    
    # Test individual components
    results.append(test_ai_service_connection())
    results.append(test_ai_nudge_generation())
    results.append(test_ai_challenge_message())
    results.append(test_ai_mood_insights())
    results.append(test_behavior_engine_integration())
    
    # Summary
    print("\n📊 Test Results Summary")
    print("="*30)
    passed = sum(results)
    total = len(results)
    
    print(f"✅ Passed: {passed}/{total}")
    print(f"❌ Failed: {total - passed}/{total}")
    
    if passed == total:
        print("\n🎉 All tests passed! AI-powered behavior engine is working correctly.")
        print("\n🚀 Ready for production deployment:")
        print("   - Dynamic AI-generated nudges")
        print("   - Personalized challenge messages")
        print("   - AI-powered mood insights")
        print("   - Contextual user engagement")
    else:
        print("\n⚠️  Some tests failed. Please check the AI service and configuration.")
        print("\n🔧 Next steps:")
        print("   1. Ensure AI service is running on localhost:5001")
        print("   2. Check GEMINI_API_KEY environment variable")
        print("   3. Verify database migrations are applied")
        print("   4. Test individual endpoints manually")

if __name__ == "__main__":
    run_all_tests()
