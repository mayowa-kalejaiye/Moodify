from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

# API URL patterns
urlpatterns = [
    # API root
    path('api/', views.HomeAPIView.as_view(), name='api_home'),
    
    # Authentication endpoints
    path('api/login/', views.UserLoginAPIView.as_view(), name='api_login'),
    path('api/logout/', views.UserLogoutAPIView.as_view(), name='api_logout'),
    path('api/register/', views.UserRegisterAPIView.as_view(), name='api_register'),
    path('api/password-change/', views.PasswordChangeAPIView.as_view(), name='api_password_change'),
    path('api/profile/', views.UserProfileAPIView.as_view(), name='api_user_profile'),
    
    # JWT token endpoints
    path('api/token/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    # Mood endpoints
    path('api/moods/', views.MoodCreateAPIView.as_view(), name='api_mood_create'),
    path('api/moods/history/', views.MoodHistoryAPIView.as_view(), name='api_mood_history'),
    path('api/moods/summary/', views.MoodSummaryAPIView.as_view(), name='api_mood_summary'),
    path('api/moods/trends/', views.MoodTrendsAPIView.as_view(), name='api_mood_trends'),
    path('api/moods/<int:mood_id>/', views.MoodDetailAPIView.as_view(), name='api_mood_detail'),
    
    # Export endpoints
    path('api/moods/export/json/', views.ExportMoodJsonAPIView.as_view(), name='api_export_json'),
    path('api/moods/export/csv/', views.ExportMoodCsvAPIView.as_view(), name='api_export_csv'),
    
    # Comment endpoints
    path('api/moods/<int:mood_id>/comments/', views.CommentListCreateAPIView.as_view(), name='api_comment_list_create'),
    path('api/moods/<int:mood_id>/comments/<int:comment_id>/', views.CommentDetailAPIView.as_view(), name='api_comment_detail'),
    
    # AI suggestions endpoints
    path('api/suggestions/motivation/', views.MotivationSuggestionAPIView.as_view(), name='api_motivation_suggestion'),
    path('api/suggestions/habits/', views.HabitImprovementAPIView.as_view(), name='api_habit_improvement'),
    path('api/moods/analysis/patterns/', views.MoodPatternAnalysisAPIView.as_view(), name='api_mood_pattern_analysis'),
    
    # Admin-only endpoints
    path('api/sentiment-analysis/', views.SentimentAnalysisAPIView.as_view(), name='api_sentiment_analysis'),
    
    # Health check endpoint
    path('api/health/', views.HealthCheckAPIView.as_view(), name='api_health_check'),
    
    # Redirect root to API homepage
    path('', views.HomeAPIView.as_view(), name='root_redirect'),
]
