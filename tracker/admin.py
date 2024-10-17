from django.contrib import admin
from .models import Mood

@admin.register(Mood)
class MoodAdmin(admin.ModelAdmin):
    list_display = ('user', 'mood', 'created_at')  # Fields to display in the admin list
    search_fields = ('user__username', 'mood')  # Allow searching by username and mood
