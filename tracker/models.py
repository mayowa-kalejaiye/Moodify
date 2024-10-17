from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator

class Mood(models.Model):
    SENTIMENT_CHOICES = [
        ('happy', 'Happy'),
        ('neutral', 'Neutral'),
        ('sad', 'Sad'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    mood = models.CharField(max_length=100)
    notes = models.TextField(validators=[MaxLengthValidator(500)], blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    sentiment = models.CharField(max_length=10, choices=SENTIMENT_CHOICES)


    def __str__(self):
        return f"{self.mood} - {self.created_at.strftime('%Y-%m-%d %H:%M:%S')}"
