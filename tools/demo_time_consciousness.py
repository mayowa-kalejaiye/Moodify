#!/usr/bin/env python3
"""
Time-of-Day Consciousness Demonstration
=====================================

This demonstrates how MoodSync adapts its behavior based on the current time.
"""

import sys
import os
from datetime import datetime
import json

# Add the project to Python path
sys.path.insert(0, os.path.abspath('.'))

from mood_tracker.tracker.time_context import TimeOfDayContext

def demonstrate_current_time_consciousness():
    """Demonstrate time consciousness for the current time"""
    
    current_time = datetime.now()
    
    print("🕐 MOODSYNC TIME-OF-DAY CONSCIOUSNESS DEMO")
    print("=" * 60)
    print(f"⏰ Current Time: {current_time.strftime('%A, %B %d, %Y at %I:%M %p')}")
    
    # Get current time context
    context = TimeOfDayContext.get_context(current_time)
    period = context['period']
    
    print(f"\n📅 Current Time Period: {period.replace('_', ' ').title()}")
    print("-" * 40)
    
    # Show contextual information
    print(f"👋 Greeting: {context['greeting']}")
    print(f"🎭 Tone: {context['tone']}")
    print(f"⚡ Energy Level: {context['energy_level']}")
    print(f"🎯 Focus: {context['focus']}")
    
    print(f"\n🎭 Time-Appropriate Mood Suggestions:")
    for mood in context['mood_suggestions']:
        print(f"   • {mood}")
    
    print(f"\n🏃 Time-Appropriate Activities:")
    for activity in context['activities']:
        print(f"   • {activity}")
    
    # Show personalized greeting
    print(f"\n👋 Personalized Greeting:")
    greeting = TimeOfDayContext.get_time_aware_greeting("User", current_time)
    print(f"   {greeting}")
    
    # Show motivational messages for different moods
    print(f"\n💪 Time-Aware Motivational Messages:")
    
    for mood_trend in ['positive', 'neutral', 'negative']:
        motivation = TimeOfDayContext.get_contextual_motivation(mood_trend, current_time)
        print(f"   📈 {mood_trend.title()}: {motivation}")
        print()
    
    # Show nudge example
    print(f"🔔 Time-Aware Nudge Example:")
    nudge = TimeOfDayContext.get_contextual_nudge("User", current_time=current_time)
    print(f"   {nudge}")
    
    # Show AI payload enhancement
    print(f"\n🤖 AI Service Payload Enhancement:")
    sample_payload = {
        "user_name": "User",
        "mood_trend": "positive",
        "user_age": 25
    }
    
    enhanced_payload = TimeOfDayContext.enhance_ai_payload_with_time_context(
        sample_payload.copy(), current_time
    )
    
    print(f"   📤 Enhanced with time context:")
    print(f"   {json.dumps(enhanced_payload, indent=2, default=str)}")
    
    print("\n" + "=" * 60)
    print("✨ This is how MoodSync adapts to YOUR current time!")
    print("🎯 Every API response includes this contextual awareness.")
    print("💡 Your experience changes throughout the day automatically.")

if __name__ == "__main__":
    demonstrate_current_time_consciousness()
