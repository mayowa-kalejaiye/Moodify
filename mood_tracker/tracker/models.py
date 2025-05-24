from django.db import models
from django.contrib.auth.models import User
from django.conf import settings

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
