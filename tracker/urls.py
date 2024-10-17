from django.urls import path
from .views import log_mood, mood_history, user_login, export_json, sentiment_analysis, home_view, register, NotStaffView
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', home_view, name='home'),  # Root URL for homepage
    path('home/', home_view, name='home'),
    path('log/', log_mood, name='log_mood'),
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('history/', mood_history, name='mood_history'),
    path('export_json/', export_json, name='export_json'),
    path('staff/', sentiment_analysis, name='staff'),
path('notstaff/', NotStaffView, name='notstaff'),
]
