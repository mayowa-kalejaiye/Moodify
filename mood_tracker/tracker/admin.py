from django.contrib import admin
from .models import Mood, Comment 

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
