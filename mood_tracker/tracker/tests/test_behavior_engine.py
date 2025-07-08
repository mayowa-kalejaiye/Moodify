"""
Test cases for MoodSync Behavior Engine
"""
from django.test import TestCase, Client
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from datetime import date, timedelta
import json

from mood_tracker.tracker.models import (
    Mood, Profile, Challenge, CoinTransaction, Nudge, Comment, AISuggestionFeedback
)


class BehaviorEngineModelTests(TestCase):
    """Test behavior engine models"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.profile = Profile.objects.get(user=self.user)
        self.profile.age = 25
        self.profile.save()
    
    def test_profile_creation(self):
        """Test profile is created with correct defaults"""
        self.assertEqual(self.profile.coin_balance, 0)
        self.assertEqual(self.profile.clarity_score, 100)
        self.assertEqual(self.profile.streak_count, 0)
        self.assertIsNone(self.profile.last_mood_log)
    
    def test_coin_reward_on_mood_log(self):
        """Test that logging mood awards coins"""
        initial_balance = self.profile.coin_balance
        
        # Create a mood entry
        mood = Mood.objects.create(
            user=self.user,
            mood='happy',
            rating=4,
            notes='Feeling great today!'
        )
        
        # Refresh profile
        self.profile.refresh_from_db()
        
        # Check coin balance increased
        self.assertEqual(self.profile.coin_balance, initial_balance + 1)
        
        # Check transaction record
        transaction = CoinTransaction.objects.filter(
            profile=self.profile,
            transaction_type='earn_mood'
        ).first()
        self.assertIsNotNone(transaction)
        self.assertEqual(transaction.amount, 1)
    
    def test_coin_reward_on_comment(self):
        """Test that adding comments awards coins"""
        # Create a mood entry
        mood = Mood.objects.create(
            user=self.user,
            mood='happy',
            rating=4
        )
        
        initial_balance = self.profile.coin_balance
        
        # Add a comment
        comment = Comment.objects.create(
            user=self.user,
            mood=mood,
            content='This is a reflection on my mood.'
        )
        
        # Refresh profile
        self.profile.refresh_from_db()
        
        # Check coin balance increased by 3 (2 for mood + 1 for comment)
        self.assertEqual(self.profile.coin_balance, initial_balance + 3)
    
    def test_streak_update(self):
        """Test streak counting logic"""
        today = date.today()
        
        # Create mood for today
        Mood.objects.create(
            user=self.user,
            mood='happy',
            rating=4,
            created_at=timezone.now()
        )
        
        # Update streak
        self.profile.update_streak()
        
        # Check streak count
        self.assertEqual(self.profile.streak_count, 1)
        self.assertEqual(self.profile.last_mood_log, today)
    
    def test_challenge_creation(self):
        """Test challenge creation and validation"""
        # Set sufficient coin balance
        self.profile.coin_balance = 30
        self.profile.save()
        
        challenge = Challenge.objects.create(
            profile=self.profile,
            challenge_type='daily_reflection',
            stake=20,
            start_date=date.today(),
            end_date=date.today() + timedelta(days=7)
        )
        
        self.assertEqual(challenge.stake, 20)
        self.assertTrue(challenge.is_active)
        self.assertEqual(challenge.days_remaining, 8)  # Including today
    
    def test_can_stake_coins_age_restriction(self):
        """Test age restriction for staking"""
        # Test user under 18
        self.profile.age = 17
        self.profile.save()
        self.assertFalse(self.profile.can_stake_coins())
        
        # Test user over 18
        self.profile.age = 18
        self.profile.save()
        self.assertTrue(self.profile.can_stake_coins())
    
    def test_nudge_creation(self):
        """Test nudge creation and tone adaptation"""
        # Create nudge for Gen Z user
        nudge = Nudge.objects.create(
            profile=self.profile,
            nudge_type='time_reminder',
            message='Quick vibe check? 😊',
            tone='gen_z'
        )
        
        self.assertEqual(nudge.tone, 'gen_z')
        self.assertFalse(nudge.viewed)


class BehaviorEngineAPITests(TestCase):
    """Test behavior engine API endpoints"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.profile = Profile.objects.get(user=self.user)
        self.profile.age = 25
        self.profile.coin_balance = 50
        self.profile.save()
        
        # Login user
        self.client.login(username='testuser', password='testpass123')
    
    def test_coin_balance_endpoint(self):
        """Test coin balance API endpoint"""
        url = reverse('api_coin_balance')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['balance'], 50)
        self.assertEqual(data['clarity_score'], 100)
    
    def test_streak_endpoint(self):
        """Test streak API endpoint"""
        url = reverse('api_streak')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['streak_count'], 0)
        self.assertEqual(data['clarity_score'], 100)
    
    def test_challenge_creation_endpoint(self):
        """Test challenge creation API"""
        url = reverse('api_challenge')
        challenge_data = {
            'challenge_type': 'daily_reflection',
            'stake': 20,
            'start_date': date.today().isoformat(),
            'end_date': (date.today() + timedelta(days=7)).isoformat()
        }
        
        response = self.client.post(
            url,
            data=json.dumps(challenge_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 201)
        
        # Check challenge was created
        challenge = Challenge.objects.filter(profile=self.profile).first()
        self.assertIsNotNone(challenge)
        self.assertEqual(challenge.stake, 20)
        
        # Check coins were deducted
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.coin_balance, 30)  # 50 - 20
    
    def test_challenge_insufficient_coins(self):
        """Test challenge creation with insufficient coins"""
        self.profile.coin_balance = 5
        self.profile.save()
        
        url = reverse('api_challenge')
        challenge_data = {
            'challenge_type': 'daily_reflection',
            'stake': 20,
            'start_date': date.today().isoformat(),
            'end_date': (date.today() + timedelta(days=7)).isoformat()
        }
        
        response = self.client.post(
            url,
            data=json.dumps(challenge_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
    
    def test_underage_staking_restriction(self):
        """Test that users under 18 cannot stake coins"""
        self.profile.age = 17
        self.profile.save()
        
        url = reverse('api_challenge')
        challenge_data = {
            'challenge_type': 'daily_reflection',
            'stake': 20,
            'start_date': date.today().isoformat(),
            'end_date': (date.today() + timedelta(days=7)).isoformat()
        }
        
        response = self.client.post(
            url,
            data=json.dumps(challenge_data),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 400)
    
    def test_nudge_endpoint(self):
        """Test nudge API endpoint"""
        # Create a nudge
        nudge = Nudge.objects.create(
            profile=self.profile,
            nudge_type='time_reminder',
            message='Test nudge message',
            tone='gen_z'
        )
        
        url = reverse('api_nudge')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertEqual(data['message'], 'Test nudge message')
        self.assertEqual(data['tone'], 'gen_z')
    
    def test_behavior_stats_endpoint(self):
        """Test behavior engine statistics endpoint"""
        url = reverse('api_behavior_stats')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        
        # Check structure
        self.assertIn('coins', data)
        self.assertIn('streaks', data)
        self.assertIn('challenges', data)
        self.assertIn('nudges', data)
        
        # Check coin data
        self.assertEqual(data['coins']['balance'], 50)
        self.assertEqual(data['coins']['clarity_score'], 100)


class BehaviorEngineTaskTests(TestCase):
    """Test Celery tasks for behavior engine"""
    
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.profile = Profile.objects.get(user=self.user)
        self.profile.age = 25
        self.profile.coin_balance = 10
        self.profile.save()


class BehaviorEngineIntegrationTests(TestCase):
    """Integration tests for behavior engine workflow"""
    
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='test@example.com'
        )
        self.profile = Profile.objects.get(user=self.user)
        self.profile.age = 25
        self.profile.save()
        
        self.client.login(username='testuser', password='testpass123')
    
    def test_complete_behavior_workflow(self):
        """Test complete behavior engine workflow"""
        # 1. User logs mood (earns coins)
        mood_url = reverse('api_mood_create')
        mood_data = {
            'mood': 'happy',
            'rating': 4,
            'notes': 'Great day!',
            'activities': 'exercise'
        }
        
        response = self.client.post(
            mood_url,
            data=json.dumps(mood_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        
        # Check coins earned
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.coin_balance, 1)
        
        # 2. User adds reflection (earns more coins)
        mood = Mood.objects.get(user=self.user)
        comment_url = reverse('api_comment_list_create', kwargs={'mood_id': mood.id})
        comment_data = {
            'content': 'This was a great day because I exercised and felt accomplished.'
        }
        
        response = self.client.post(
            comment_url,
            data=json.dumps(comment_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        
        # Check coins earned for reflection
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.coin_balance, 3)  # 1 + 2 for reflection
        
        # 3. User provides AI feedback (earns coins)
        feedback_url = reverse('api_ai_feedback')
        feedback_data = {
            'suggestion_type': 'motivation',
            'suggestion_text': 'Keep up the great work!',
            'rating': 3
        }
        
        response = self.client.post(
            feedback_url,
            data=json.dumps(feedback_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        
        # Check coins earned for feedback
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.coin_balance, 4)  # 3 + 1 for feedback
        
        # 4. Check streak was updated
        self.assertEqual(self.profile.streak_count, 1)
        self.assertEqual(self.profile.last_mood_log, date.today())
        
        # 5. User stakes coins on challenge
        challenge_url = reverse('api_challenge')
        challenge_data = {
            'challenge_type': 'daily_reflection',
            'stake': 15,  # Changed to valid stake amount (min 10)
            'start_date': date.today().isoformat(),
            'end_date': (date.today() + timedelta(days=7)).isoformat()
        }
        
        # Need to add more coins first for valid stake
        self.profile.coin_balance = 20
        self.profile.save()
        
        response = self.client.post(
            challenge_url,
            data=json.dumps(challenge_data),
            content_type='application/json'
        )
        self.assertEqual(response.status_code, 201)
        
        # Check coins deducted
        self.profile.refresh_from_db()
        self.assertEqual(self.profile.coin_balance, 5)  # 20 - 15
        
        # 6. Check behavior stats
        stats_url = reverse('api_behavior_stats')
        response = self.client.get(stats_url)
        self.assertEqual(response.status_code, 200)
        
        data = json.loads(response.content)
        self.assertEqual(data['coins']['balance'], 5)  # Updated balance
        self.assertEqual(data['streaks']['current_streak'], 1)
        self.assertEqual(data['challenges']['total'], 1)
        self.assertEqual(data['challenges']['completed'], 0)  # Not completed yet


if __name__ == '__main__':
    # Run with: python manage.py test mood_tracker.tracker.tests.test_behavior_engine
    pass
