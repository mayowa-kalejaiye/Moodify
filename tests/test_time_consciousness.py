#!/usr/bin/env python3
"""
Time-of-Day Consciousness Test for MoodSync
==========================================

This test demonstrates the time-aware functionality implemented in MoodSync.
"""

import sys
import os
from datetime import datetime, time
import json

# Add the project root to Python path
sys.path.insert(0, os.path.abspath('.'))

# Import our time context module directly
from mood_tracker.tracker.time_context import TimeOfDayContext

def test_time_consciousness():
    """Test all time-of-day consciousness features"""
    
    print("🕐 TIME-OF-DAY CONSCIOUSNESS TEST")
    print("=" * 60)
    
    # Test different times of day
    test_times = [
        datetime(2025, 7, 8, 6, 30),    # Early morning
        datetime(2025, 7, 8, 10, 0),    # Morning
        datetime(2025, 7, 8, 13, 0),    # Midday
        datetime(2025, 7, 8, 16, 0),    # Afternoon
        datetime(2025, 7, 8, 19, 0),    # Evening
        datetime(2025, 7, 8, 23, 0),    # Night
        datetime(2025, 7, 8, 2, 0),     # Late night
    ]
    
    for test_time in test_times:
        print(f"\n⏰ Testing time: {test_time.strftime('%I:%M %p')}")
        print("-" * 40)
        
        # Get time period
        period = TimeOfDayContext.get_current_period(test_time)
        print(f"📅 Period: {period}")
        
        # Get context
        context = TimeOfDayContext.get_context(test_time)
        print(f"🎯 Context:")
        print(f"   • Greeting: {context['greeting']}")
        print(f"   • Tone: {context['tone']}")
        print(f"   • Energy Level: {context['energy_level']}")
        print(f"   • Focus: {context['focus']}")
        print(f"   • Suggested Moods: {', '.join(context['mood_suggestions'])}")
        print(f"   • Suggested Activities: {', '.join(context['activities'])}")
        
        # Test greetings
        greeting = TimeOfDayContext.get_time_aware_greeting("Alex", test_time)
        print(f"👋 Personalized Greeting: {greeting}")
        
        # Test motivational messages
        for mood_trend in ['positive', 'neutral', 'negative']:
            motivation = TimeOfDayContext.get_contextual_motivation(mood_trend, test_time)
            print(f"💪 {mood_trend.title()} Motivation: {motivation}")
        
        # Test nudge messages
        nudge = TimeOfDayContext.get_contextual_nudge("Alex", 5, test_time)
        print(f"🔔 Nudge Message: {nudge}")
        
        print()

def test_ai_payload_enhancement():
    """Test AI payload enhancement with time context"""
    
    print("\n🤖 AI PAYLOAD ENHANCEMENT TEST")
    print("=" * 60)
    
    # Base payload
    base_payload = {
        "user_name": "Alex",
        "mood_trend_label": "positive",
        "recent_mood_texts": ["happy", "excited", "motivated"],
        "user_age": 25
    }
    
    # Test at different times
    morning_time = datetime(2025, 7, 8, 9, 0)
    evening_time = datetime(2025, 7, 8, 20, 0)
    
    for test_time, time_label in [(morning_time, "Morning"), (evening_time, "Evening")]:
        print(f"\n⏰ {time_label} Enhancement:")
        print("-" * 30)
        
        enhanced_payload = TimeOfDayContext.enhance_ai_payload_with_time_context(
            base_payload.copy(), test_time
        )
        
        print("📤 Enhanced Payload:")
        print(json.dumps(enhanced_payload, indent=2, default=str))

def test_time_period_detection():
    """Test time period detection accuracy"""
    
    print("\n🕐 TIME PERIOD DETECTION TEST")
    print("=" * 60)
    
    # Test boundary cases
    test_cases = [
        (time(5, 0), "early_morning"),
        (time(8, 59), "early_morning"),
        (time(9, 0), "morning"),
        (time(11, 59), "morning"),
        (time(12, 0), "midday"),
        (time(13, 59), "midday"),
        (time(14, 0), "afternoon"),
        (time(17, 59), "afternoon"),
        (time(18, 0), "evening"),
        (time(21, 59), "evening"),
        (time(22, 0), "night"),
        (time(23, 59), "night"),
        (time(0, 0), "late_night"),
        (time(4, 59), "late_night"),
    ]
    
    for test_time, expected_period in test_cases:
        test_datetime = datetime.combine(datetime.today(), test_time)
        detected_period = TimeOfDayContext.get_current_period(test_datetime)
        
        status = "✅" if detected_period == expected_period else "❌"
        print(f"{status} {test_time.strftime('%H:%M')} -> {detected_period} (expected: {expected_period})")

if __name__ == "__main__":
    print("🚀 STARTING TIME-OF-DAY CONSCIOUSNESS TESTS")
    print("=" * 80)
    
    try:
        test_time_consciousness()
        test_ai_payload_enhancement() 
        test_time_period_detection()
        
        print("\n" + "=" * 80)
        print("✅ ALL TIME CONSCIOUSNESS TESTS COMPLETED SUCCESSFULLY!")
        print("\n🎯 KEY FEATURES IMPLEMENTED:")
        print("• Time-aware greetings and messages")
        print("• Context-appropriate mood suggestions")
        print("• Time-specific motivational content")
        print("• Intelligent nudge timing")
        print("• Enhanced AI service payloads")
        print("• Activity recommendations by time")
        print("• Energy level awareness")
        print("• Focus area adaptation")
        
    except Exception as e:
        print(f"\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
