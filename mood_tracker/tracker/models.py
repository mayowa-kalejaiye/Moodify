from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from datetime import date, timedelta

class Mood(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='moods')
    mood = models.CharField(max_length=100)
    notes = models.TextField(blank=True, null=True)
    sentiment = models.FloatField(null=True, blank=True)
    activities = models.CharField(max_length=255, blank=True, null=True)
    rating = models.IntegerField(default=3, choices=[
        (1, 'Very Bad'),
        (2, 'Bad'),
        (3, 'Neutral'),
        (4, 'Good'),
        (5, 'Very Good')
    ])
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username}: {self.mood} ({self.created_at.strftime('%Y-%m-%d')})"
    
    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Mood'
        verbose_name_plural = 'Moods'

# class MoodComment(models.Model):
#     """
#     LEGACY MODEL: This model is considered legacy.
#     Please use the Comment model for new development.
#     This model, its serializers, and views will be removed in a future version.
#     If you have data in this table, plan a migration to the Comment model.
#     """
#     mood_entry = models.ForeignKey(Mood, on_delete=models.CASCADE, related_name='legacy_comments')
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     content = models.TextField()
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def __str__(self):
#         return f"Comment on {self.mood_entry} - {self.created_at.strftime('%Y-%m-%d')}"
    
#     class Meta:
#         verbose_name = 'Legacy Mood Comment'
#         verbose_name_plural = 'Legacy Mood Comments'

class Comment(models.Model):
    """Model for user comments on mood entries"""
    mood = models.ForeignKey(Mood, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"Comment by {self.user.username} on mood {self.mood.id}"

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    age = models.PositiveIntegerField(null=True, blank=True)
    
    # Behavior Engine Fields
    coin_balance = models.IntegerField(default=0)
    clarity_score = models.PositiveSmallIntegerField(default=100)
    streak_count = models.PositiveSmallIntegerField(default=0)
    last_mood_log = models.DateField(null=True, blank=True)
    streak_last_updated = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} Profile"
    
    def update_streak(self):
        """Update streak count based on mood logging activity"""
        today = date.today()
        
        # Check if user has logged a mood today
        has_mood_today = Mood.objects.filter(
            user=self.user,
            created_at__date=today
        ).exists()
        
        if has_mood_today:
            # Update last mood log
            self.last_mood_log = today
            
            # If streak was updated yesterday or today, increment
            if (self.streak_last_updated == today - timedelta(days=1) or 
                self.streak_last_updated == today):
                if self.streak_last_updated != today:  # Only increment once per day
                    self.streak_count += 1
                    self.streak_last_updated = today
            else:
                # Reset streak if gap > 1 day
                self.streak_count = 1
                self.streak_last_updated = today
        else:
            # Check if streak should be broken (3+ days without logging)
            if (self.last_mood_log and 
                (today - self.last_mood_log).days >= 3):
                self.streak_count = 0
                self.clarity_score = max(0, self.clarity_score - 10)
        
        self.save()
    
    def can_stake_coins(self):
        """Check if user can participate in staking (age >= 18)"""
        return self.age is not None and self.age >= 18

class Challenge(models.Model):
    CHALLENGE_TYPES = [
        ('daily_reflection', 'Daily Reflection'),
        ('mood_awareness', 'Mood Awareness'),
        ('activity_tracking', 'Activity Tracking'),
    ]
    
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='challenges')
    challenge_type = models.CharField(max_length=20, choices=CHALLENGE_TYPES, default='daily_reflection')
    stake = models.PositiveIntegerField()
    start_date = models.DateField()
    end_date = models.DateField()
    completed = models.BooleanField(default=False)
    settled = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.profile.user.username} - {self.challenge_type} Challenge ({self.stake} coins)"
    
    @property
    def is_active(self):
        """Check if challenge is currently active"""
        today = date.today()
        return self.start_date <= today <= self.end_date and not self.settled
    
    @property
    def days_remaining(self):
        """Get days remaining in challenge"""
        if not self.is_active:
            return 0
        return (self.end_date - date.today()).days + 1
    
    def check_completion(self):
        """Check if challenge requirements are met"""
        if self.challenge_type == 'daily_reflection':
            # Check if user has logged moods for all days in challenge period
            total_days = (self.end_date - self.start_date).days + 1
            logged_days = Mood.objects.filter(
                user=self.profile.user,
                created_at__date__range=[self.start_date, self.end_date]
            ).dates('created_at', 'day').count()
            
            self.completed = logged_days >= total_days
        
        # Add other challenge type logic as needed
        return self.completed
    
    def get_completion_message(self):
        """Get AI-generated completion message for the challenge"""
        try:
            import requests
            from django.conf import settings
            
            # Prepare context for AI
            context = {
                'challenge_type': self.challenge_type,
                'stake': self.stake,
                'duration_days': (self.end_date - self.start_date).days + 1,
                'user_age': self.profile.age,
                'completed': self.completed,
                'tone': 'gen_z' if self.profile.age and self.profile.age < 30 else 'professional'
            }
            
            # Call AI service
            ai_service_url = getattr(settings, 'AI_SERVICE_URL', 'http://localhost:5000')
            
            payload = {
                'prompt_type': 'challenge_completion',
                'context': context,
                'max_length': 200
            }
            
            response = requests.post(
                f"{ai_service_url}/generate-challenge-message",
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json().get('message', 'Challenge completed!')
            else:
                return self._get_fallback_completion_message()
                
        except Exception as e:
            return self._get_fallback_completion_message()
    
    def _get_fallback_completion_message(self):
        """Fallback completion message when AI service is unavailable"""
        if self.completed:
            return f"Congratulations! You've successfully completed your {self.challenge_type} challenge and earned {self.stake} coins!"
        else:
            return f"Challenge period ended. Better luck next time with your {self.challenge_type} challenge."

class CoinTransaction(models.Model):
    TRANSACTION_TYPES = [
        ('earn_mood', 'Mood Log (+1)'),
        ('earn_reflection', 'Reflection (+2)'),
        ('earn_feedback', 'AI Feedback (+1)'),
        ('lose_inactive', 'Inactivity Penalty (-1)'),
        ('stake_challenge', 'Challenge Stake'),
        ('win_challenge', 'Challenge Win'),
        ('lose_challenge', 'Challenge Loss'),
        ('spend_insight', 'Deep Insight Purchase'),
    ]
    
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='coin_transactions')
    transaction_type = models.CharField(max_length=20, choices=TRANSACTION_TYPES)
    amount = models.IntegerField()  # Can be negative for losses
    balance_after = models.IntegerField()
    description = models.CharField(max_length=255, blank=True, null=True)
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.profile.user.username}: {self.transaction_type} ({self.amount:+d})"
    
    class Meta:
        ordering = ['-created_at']

class Nudge(models.Model):
    NUDGE_TYPES = [
        ('mood_trend', 'Mood Trend Alert'),
        ('time_reminder', 'Time-based Reminder'),
        ('skip_pattern', 'Skip Pattern Alert'),
        ('streak_motivation', 'Streak Motivation'),
    ]
    
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='nudges')
    nudge_type = models.CharField(max_length=20, choices=NUDGE_TYPES)
    message = models.TextField()
    tone = models.CharField(max_length=12, choices=[('gen_z', 'Gen Z'), ('professional', 'Professional')])
    viewed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.profile.user.username} - {self.nudge_type}"
    
    class Meta:
        ordering = ['-created_at']

class AISuggestionFeedback(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    suggestion_type = models.CharField(max_length=32)  # e.g., 'motivation', 'habits'
    suggestion_text = models.TextField()
    rating = models.IntegerField()  # 1=bad, 2=neutral, 3=good
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.suggestion_type} feedback"

def get_or_create_profile(user):
    """Ensure a Profile exists for the given user."""
    profile, created = Profile.objects.get_or_create(user=user)
    return profile

@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()

@receiver(post_save, sender=Mood)
def handle_mood_logged(sender, instance, created, **kwargs):
    """Handle coin rewards and streak updates when mood is logged"""
    if created:
        profile = get_or_create_profile(instance.user)
        
        # Award coin for mood log
        profile.coin_balance += 1
        profile.save()
        
        # Create transaction record
        CoinTransaction.objects.create(
            profile=profile,
            transaction_type='earn_mood',
            amount=1,
            balance_after=profile.coin_balance,
            description=f"Earned 1 coin for logging mood: {instance.mood}"
        )
        
        # Update streak
        profile.update_streak()

@receiver(post_save, sender=Comment)
def handle_comment_created(sender, instance, created, **kwargs):
    """Award coins for reflective comments"""
    if created:
        profile = get_or_create_profile(instance.user)
        
        # Award coins for reflection
        profile.coin_balance += 2
        profile.save()
        
        # Create transaction record
        CoinTransaction.objects.create(
            profile=profile,
            transaction_type='earn_reflection',
            amount=2,
            balance_after=profile.coin_balance,
            description=f"Earned 2 coins for thoughtful reflection comment"
        )

@receiver(post_save, sender=AISuggestionFeedback)
def handle_ai_feedback(sender, instance, created, **kwargs):
    """Award coins for AI feedback"""
    if created:
        profile = get_or_create_profile(instance.user)
        
        # Award coin for AI feedback
        profile.coin_balance += 1
        profile.save()
        
        # Create transaction record
        CoinTransaction.objects.create(
            profile=profile,
            transaction_type='earn_feedback',
            amount=1,
            balance_after=profile.coin_balance,
            description=f"Earned 1 coin for providing AI feedback on {instance.suggestion_type}"
        )
