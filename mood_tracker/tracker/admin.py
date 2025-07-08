from django.contrib import admin
from .models import Mood, Comment, Profile, AISuggestionFeedback, Challenge, CoinTransaction, Nudge 

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
    list_display = ('user', 'age', 'coin_balance', 'clarity_score', 'streak_count', 'last_mood_log')
    search_fields = ('user__username',)
    list_filter = ('age', 'coin_balance', 'clarity_score', 'streak_count')
    readonly_fields = ('coin_balance', 'clarity_score', 'streak_count', 'last_mood_log', 'streak_last_updated')
    
    fieldsets = (
        ('User Info', {
            'fields': ('user', 'age')
        }),
        ('Behavior Engine', {
            'fields': ('coin_balance', 'clarity_score', 'streak_count', 'last_mood_log', 'streak_last_updated'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Challenge)
class ChallengeAdmin(admin.ModelAdmin):
    list_display = ('profile', 'challenge_type', 'stake', 'start_date', 'end_date', 'completed', 'settled')
    list_filter = ('challenge_type', 'completed', 'settled', 'start_date', 'end_date')
    search_fields = ('profile__user__username',)
    readonly_fields = ('completed', 'settled', 'created_at')
    date_hierarchy = 'created_at'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('profile__user')

@admin.register(CoinTransaction)
class CoinTransactionAdmin(admin.ModelAdmin):
    list_display = ('profile', 'transaction_type', 'amount', 'balance_after', 'created_at')
    list_filter = ('transaction_type', 'created_at')
    search_fields = ('profile__user__username',)
    readonly_fields = ('profile', 'transaction_type', 'amount', 'balance_after', 'challenge', 'created_at')
    date_hierarchy = 'created_at'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('profile__user')
    
    def has_add_permission(self, request):
        return False  # Transactions should only be created programmatically
    
    def has_change_permission(self, request, obj=None):
        return False  # Transactions should not be edited

@admin.register(Nudge)
class NudgeAdmin(admin.ModelAdmin):
    list_display = ('profile', 'nudge_type', 'tone', 'viewed', 'created_at')
    list_filter = ('nudge_type', 'tone', 'viewed', 'created_at')
    search_fields = ('profile__user__username', 'message')
    readonly_fields = ('profile', 'nudge_type', 'tone', 'created_at')
    date_hierarchy = 'created_at'
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('profile__user')
    
    fieldsets = (
        ('Nudge Info', {
            'fields': ('profile', 'nudge_type', 'tone', 'viewed')
        }),
        ('Content', {
            'fields': ('message',)
        }),
        ('Timestamps', {
            'fields': ('created_at',),
            'classes': ('collapse',)
        }),
    )

@admin.register(AISuggestionFeedback)
class AISuggestionFeedbackAdmin(admin.ModelAdmin):
    list_display = ('user', 'suggestion_type', 'rating', 'created_at')
    list_filter = ('suggestion_type', 'rating', 'created_at')
    search_fields = ('user__username', 'suggestion_text')
    date_hierarchy = 'created_at'
