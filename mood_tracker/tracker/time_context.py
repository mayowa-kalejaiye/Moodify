#!/usr/bin/env python3
"""
Time-of-Day Consciousness Module for MoodSync
===========================================

This module provides time-aware functionality that makes the system conscious
of the current time of day and adjusts its behavior accordingly.
"""
from datetime import datetime, time
from typing import Dict, Tuple, List

class TimeOfDayContext:
    """
    Time-of-day consciousness helper that provides contextual information
    based on the current time.
    """
    
    # Time periods definition
    TIME_PERIODS = {
        'early_morning': (time(5, 0), time(8, 59)),    # 5:00-8:59 AM
        'morning': (time(9, 0), time(11, 59)),          # 9:00-11:59 AM
        'midday': (time(12, 0), time(13, 59)),          # 12:00-1:59 PM
        'afternoon': (time(14, 0), time(17, 59)),       # 2:00-5:59 PM
        'evening': (time(18, 0), time(21, 59)),         # 6:00-9:59 PM
        'night': (time(22, 0), time(23, 59)),           # 10:00-11:59 PM
        'late_night': (time(0, 0), time(4, 59)),        # 12:00-4:59 AM
    }
    
    # Contextual messages and suggestions based on time
    TIME_CONTEXT = {
        'early_morning': {
            'greeting': 'Good early morning',
            'mood_suggestions': ['refreshed', 'groggy', 'peaceful', 'energetic'],
            'activities': ['meditation', 'stretching', 'coffee', 'planning day'],
            'tone': 'gentle',
            'energy_level': 'building',
            'focus': 'preparation'
        },
        'morning': {
            'greeting': 'Good morning',
            'mood_suggestions': ['motivated', 'focused', 'productive', 'optimistic'],
            'activities': ['work', 'exercise', 'meetings', 'creative tasks'],
            'tone': 'energetic',
            'energy_level': 'high',
            'focus': 'achievement'
        },
        'midday': {
            'greeting': 'Good afternoon',
            'mood_suggestions': ['satisfied', 'accomplished', 'hungry', 'steady'],
            'activities': ['lunch', 'break', 'collaboration', 'reflection'],
            'tone': 'balanced',
            'energy_level': 'stable',
            'focus': 'sustenance'
        },
        'afternoon': {
            'greeting': 'Good afternoon',
            'mood_suggestions': ['determined', 'tired', 'persevering', 'social'],
            'activities': ['meetings', 'social tasks', 'problem solving', 'snack'],
            'tone': 'supportive',
            'energy_level': 'declining',
            'focus': 'persistence'
        },
        'evening': {
            'greeting': 'Good evening',
            'mood_suggestions': ['relaxed', 'social', 'tired', 'reflective'],
            'activities': ['dinner', 'family time', 'hobbies', 'unwinding'],
            'tone': 'warm',
            'energy_level': 'winding_down',
            'focus': 'connection'
        },
        'night': {
            'greeting': 'Good night',
            'mood_suggestions': ['peaceful', 'tired', 'content', 'sleepy'],
            'activities': ['reading', 'relaxation', 'preparation for bed', 'reflection'],
            'tone': 'calm',
            'energy_level': 'low',
            'focus': 'rest'
        },
        'late_night': {
            'greeting': 'Late night check-in',
            'mood_suggestions': ['restless', 'contemplative', 'worried', 'creative'],
            'activities': ['journal writing', 'quiet activities', 'breathing exercises'],
            'tone': 'gentle',
            'energy_level': 'very_low',
            'focus': 'peace'
        }
    }
    
    @classmethod
    def get_current_period(cls, current_time: datetime = None) -> str:
        """Get the current time period"""
        if current_time is None:
            current_time = datetime.now()
        
        current_time_only = current_time.time()
        
        for period, (start, end) in cls.TIME_PERIODS.items():
            if period == 'late_night':
                # Handle late night crossing midnight
                if current_time_only >= start or current_time_only <= end:
                    return period
            else:
                if start <= current_time_only <= end:
                    return period
        
        return 'morning'  # default fallback
    
    @classmethod
    def get_context(cls, current_time: datetime = None) -> Dict:
        """Get contextual information for the current time"""
        period = cls.get_current_period(current_time)
        context = cls.TIME_CONTEXT[period].copy()
        context['period'] = period
        context['timestamp'] = current_time or datetime.now()
        return context
    
    @classmethod
    def get_time_aware_greeting(cls, user_name: str = None, current_time: datetime = None) -> str:
        """Get a time-appropriate greeting"""
        context = cls.get_context(current_time)
        greeting = context['greeting']
        
        if user_name:
            return f"{greeting}, {user_name}!"
        return f"{greeting}!"
    
    @classmethod
    def get_contextual_motivation(cls, mood_trend: str, current_time: datetime = None) -> str:
        """Get time-aware motivational message"""
        context = cls.get_context(current_time)
        period = context['period']
        tone = context['tone']
        focus = context['focus']
        
        # Time-specific motivational templates
        motivation_templates = {
            'early_morning': {
                'positive': "You're starting your day beautifully! This peaceful morning energy is perfect for setting positive intentions.",
                'neutral': "Take this quiet morning moment to breathe deeply and set a gentle pace for your day ahead.",
                'negative': "Morning can be tough, but this fresh start gives you a chance to shift your energy. Take it slow and be kind to yourself."
            },
            'morning': {
                'positive': "Your morning energy is fantastic! Channel this motivation into something meaningful today.",
                'neutral': "You're in a good rhythm this morning. Build on this steady energy throughout your day.",
                'negative': "Mornings can feel overwhelming, but remember - you don't have to be perfect. Focus on just one small step forward."
            },
            'midday': {
                'positive': "You're crushing the middle of your day! Keep this momentum going while staying balanced.",
                'neutral': "Midday is perfect for checking in with yourself. You're doing well - take a moment to appreciate your progress.",
                'negative': "The afternoon slump is real, but temporary. A quick break or healthy snack might be just what you need."
            },
            'afternoon': {
                'positive': "Your afternoon perseverance is admirable! You're showing real strength in pushing through.",
                'neutral': "Afternoon energy can be tricky to maintain. You're doing great at staying steady through the day.",
                'negative': "Afternoon fatigue is completely normal. Be compassionate with yourself and consider what small comfort might help."
            },
            'evening': {
                'positive': "What a beautiful way to end your day! This positive evening energy is perfect for reflection and gratitude.",
                'neutral': "Evening is a natural time for winding down. You've made it through another day - that's something to acknowledge.",
                'negative': "Evening emotions can feel heavy. Remember that nighttime often amplifies worries - be extra gentle with yourself."
            },
            'night': {
                'positive': "Ending your day on such a positive note is wonderful! Rest well knowing you've done good today.",
                'neutral': "This calm night energy is perfect for peaceful rest. You've navigated another day successfully.",
                'negative': "Night can make everything feel more intense. Focus on small comforts and remember tomorrow is a fresh start."
            },
            'late_night': {
                'positive': "Your late-night positive energy is special! Channel this into something creative or meaningful before rest.",
                'neutral': "Late night check-ins show great self-awareness. Honor whatever feelings are present without judgment.",
                'negative': "Late-night struggles are common - you're not alone. Try some gentle breathing or write down your thoughts to ease your mind."
            }
        }
        
        return motivation_templates.get(period, {}).get(mood_trend, "Take care of yourself - you matter.")
    
    @classmethod
    def get_contextual_nudge(cls, user_name: str = None, streak_count: int = 0, current_time: datetime = None) -> str:
        """Get time-aware nudge message"""
        context = cls.get_context(current_time)
        period = context['period']
        greeting = cls.get_time_aware_greeting(user_name, current_time)
        
        nudge_templates = {
            'early_morning': [
                f"{greeting} This peaceful morning is perfect for a mindful mood check-in. How are you feeling as you start your day?",
                f"{greeting} Early birds like you deserve recognition! Quick mood log to capture this morning energy?",
                f"{greeting} What a beautiful time to reflect. Take a moment to notice how you're feeling right now."
            ],
            'morning': [
                f"{greeting} Your morning momentum is building - how's your energy feeling right now?",
                f"{greeting} Perfect time for a productive mood check! What's driving your morning motivation?",
                f"{greeting} Morning clarity is powerful - capture how you're feeling to track your patterns."
            ],
            'midday': [
                f"{greeting} Midday check-in time! How are you feeling halfway through your day?",
                f"{greeting} Lunch break = perfect mood break. Quick check-in on your afternoon vibes?",
                f"{greeting} How's your energy holding up? A quick mood log can help you stay aware."
            ],
            'afternoon': [
                f"{greeting} Afternoon persistence check! How are you powering through?",
                f"{greeting} This time of day can be tricky - how's your mood holding up?",
                f"{greeting} You're doing great getting through the day. Quick mood check to stay connected with yourself?"
            ],
            'evening': [
                f"{greeting} Perfect time for reflection - how did today treat you?",
                f"{greeting} Evening wind-down begins! How are you feeling as you transition to rest?",
                f"{greeting} End-of-day mood check can help you process today and prepare for tomorrow."
            ],
            'night': [
                f"{greeting} Nighttime self-care includes checking in with your emotions. How are you feeling?",
                f"{greeting} Before you rest, take a moment to acknowledge your feelings from today.",
                f"{greeting} Night reflection can be powerful. Quick mood log to honor your day?"
            ],
            'late_night': [
                f"{greeting} Late night thoughts can be intense. Logging your mood might help process them.",
                f"{greeting} You're up late - that's okay. How are you feeling in this quiet moment?",
                f"{greeting} Sometimes late nights bring clarity. Capture how you're feeling right now."
            ]
        }
        
        import random
        messages = nudge_templates.get(period, nudge_templates['morning'])
        return random.choice(messages)
    
    @classmethod
    def get_time_appropriate_activities(cls, current_time: datetime = None) -> List[str]:
        """Get activities appropriate for the current time"""
        context = cls.get_context(current_time)
        return context['activities']
    
    @classmethod
    def enhance_ai_payload_with_time_context(cls, payload: Dict, current_time: datetime = None) -> Dict:
        """Enhance AI service payload with time-of-day context"""
        context = cls.get_context(current_time)
        
        payload.update({
            'time_of_day': context['period'],
            'time_context': {
                'greeting': context['greeting'],
                'tone': context['tone'],
                'energy_level': context['energy_level'],
                'focus': context['focus'],
                'suggested_activities': context['activities'],
                'suggested_moods': context['mood_suggestions']
            },
            'timestamp': context['timestamp'].isoformat()
        })
        
        return payload
