from django.contrib import admin
from .models import Mood, Comment, Profile, AISuggestionFeedback 

@admin.register(Mood)
class MoodAdmin(admin.ModelAdmin):
    list_display = ('user', 'mood', 'rating', 'sentiment', 'created_at')
    list_filter = ('created_at', 'mood', 'rating', 'user')
    search_fields = ('mood', 'notes', 'user__username')
    readonly_fields = ('sentiment',)
    date_hierarchy = 'created_at'

# @admin.register(MoodComment)
# class MoodCommentAdmin(admin.ModelAdmin):
#     """
#     LEGACY ADMIN: Admin interface for the MoodComment model, which is considered legacy.
#     This will be removed in a future version.
#     """
#     list_display = ('mood_entry', 'user', 'created_at')
#     list_filter = ('created_at', 'user')
#     search_fields = ('content', 'user__username')

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'mood', 'created_at')
    list_filter = ('created_at', 'user')
    search_fields = ('content', 'user__username')
    date_hierarchy = 'created_at'

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'age')
    search_fields = ('user__username',)

@admin.register(AISuggestionFeedback)
class AISuggestionFeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'suggestion_type', 'rating', 'created_at')
    list_filter = ('suggestion_type', 'rating', 'created_at')
    search_fields = ('user__username', 'suggestion_text')
    date_hierarchy = 'created_at'
