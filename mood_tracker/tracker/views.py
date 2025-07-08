from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Avg, Count, Q
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.core.cache import cache
from django.conf import settings
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page

import csv
import random
from datetime import datetime, timedelta
from textblob import TextBlob

from rest_framework import status, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework.authtoken.models import Token
from rest_framework.decorators import api_view, permission_classes
from rest_framework.exceptions import PermissionDenied
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

# Add Swagger imports
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

# Swagger API Tags for categorization
SWAGGER_TAGS = {
    'AUTHENTICATION': 'Authentication & Security',
    'MOOD_TRACKING': 'Mood & Behavior Tracking',
    'COIN_SYSTEM': 'Coin & Challenge System',
    'NUDGE_SYSTEM': 'Nudge & Engagement System',
    'PROFILE_MANAGEMENT': 'Profile & User Management',
    'ADMIN_MONITORING': 'Admin & System Monitoring',
    'AI_INSIGHTS': 'AI-Powered Insights',
    'DATA_EXPORT': 'Data Export & Analytics'
}

from .models import Mood, Comment, Profile, AISuggestionFeedback, Challenge, CoinTransaction, Nudge, get_or_create_profile
from .serializers import (
    MoodSerializer, 
    UserSerializer, 
    UserRegisterSerializer,
    PasswordChangeSerializer,
    CommentSerializer,
    ProfileSerializer,
    AISuggestionFeedbackSerializer,
    ChallengeSerializer,
    CoinTransactionSerializer,
    NudgeSerializer,
)
from .time_context import TimeOfDayContext

import requests
import os
import logging
from urllib.parse import urlparse

logger = logging.getLogger(__name__)

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Enhanced JWT token endpoint that returns user information along with tokens
    """
    @swagger_auto_schema(
        tags=[SWAGGER_TAGS['AUTHENTICATION']],
        operation_summary="🔐 Login with JWT Authentication",
        operation_description="Authenticate user and receive JWT access/refresh tokens along with user profile data",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description="Username or email"),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description="User password")
            }
        ),
        responses={
            200: openapi.Response(
                description="Authentication successful",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'access': openapi.Schema(type=openapi.TYPE_STRING, description="JWT access token"),
                        'refresh': openapi.Schema(type=openapi.TYPE_STRING, description="JWT refresh token"),
                        'user': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'username': openapi.Schema(type=openapi.TYPE_STRING),
                                'email': openapi.Schema(type=openapi.TYPE_STRING),
                                'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                                'last_name': openapi.Schema(type=openapi.TYPE_STRING),
                            }
                        )
                    }
                )
            ),
            401: openapi.Response(description="Invalid credentials")
        }
    )
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        
        # If successful, add user data to response
        if response.status_code == status.HTTP_200_OK:
            # Get username from request
            username = request.data.get('username')
            
            # Get user info
            try:
                user = User.objects.get(username=username)
                user_data = UserSerializer(user).data
                
                # Add user data to response
                response.data['user'] = user_data
            except User.DoesNotExist:
                pass
        
        return response

class HomeAPIView(APIView):
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(
        tags=[SWAGGER_TAGS['ADMIN_MONITORING']],
        operation_summary="🏠 API Documentation Hub",
        operation_description="Comprehensive API documentation with all available endpoints, methods, and descriptions",
        responses={
            200: openapi.Response(
                description="API documentation and endpoint information",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'name': openapi.Schema(type=openapi.TYPE_STRING),
                        'version': openapi.Schema(type=openapi.TYPE_STRING),
                        'description': openapi.Schema(type=openapi.TYPE_STRING),
                        'endpoints': openapi.Schema(type=openapi.TYPE_OBJECT),
                        'status': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            )
        }
    )
    def get(self, request):
        """API root endpoint with comprehensive documentation"""
        api_info = {
            'name': 'MoodSync API - Behavior Engine v1',
            'version': '2.0.0',
            'description': 'Advanced mood tracking with AI insights, behavior analytics, and gamification features.',
            'endpoints': {
                'authentication': {
                    'login': {'url': '/api/login/', 'method': 'POST', 'description': 'Login with username/password - returns both legacy token and JWT tokens'},
                    'logout': {'url': '/api/logout/', 'method': 'POST', 'description': 'Logout and invalidate authentication token'},
                    'register': {'url': '/api/register/', 'method': 'POST', 'description': 'Create a new user account with automatic profile setup'},
                    'password_change': {'url': '/api/password-change/', 'method': 'POST', 'description': 'Change user password with old password verification'},
                    'jwt_token': {'url': '/api/token/', 'method': 'POST', 'description': 'Get JWT access and refresh tokens'},
                    'jwt_refresh': {'url': '/api/token/refresh/', 'method': 'POST', 'description': 'Refresh JWT access token'},
                },
                'profile_management': {
                    'profile': {'url': '/api/profile/', 'method': 'GET/PUT/PATCH', 'description': 'View or update user profile including age and personal info'},
                    'coin_balance': {'url': '/api/coins/balance/', 'method': 'GET', 'description': 'Get current coin balance and transaction history'},
                    'streak': {'url': '/api/streak/', 'method': 'GET', 'description': 'Get current mood logging streak and statistics'},
                    'behavior_stats': {'url': '/api/behavior/stats/', 'method': 'GET', 'description': 'Comprehensive behavior engine statistics and achievements'},
                },
                'mood_tracking': {
                    'create': {'url': '/api/moods/', 'method': 'POST', 'description': 'Log a new mood entry with automatic sentiment analysis and coin rewards'},
                    'options': {'url': '/api/moods/', 'method': 'GET', 'description': 'Get time-aware mood options and suggested activities'},
                    'history': {'url': '/api/moods/history/', 'method': 'GET', 'description': 'Get mood history with filtering, caching, and pagination'},
                    'summary': {'url': '/api/moods/summary/', 'method': 'GET', 'description': 'Get comprehensive mood statistics and distribution analysis'},
                    'trends': {'url': '/api/moods/trends/', 'method': 'GET', 'description': 'Analyze mood trends over time with daily aggregations'},
                    'detail': {'url': '/api/moods/{mood_id}/', 'method': 'GET/PUT/DELETE', 'description': 'Get, update, or delete a specific mood entry'},
                    'insights': {'url': '/api/insights/', 'method': 'GET', 'description': 'Get AI-powered mood insights and personalized recommendations'},
                },
                'comments_reflection': {
                    'list_create': {'url': '/api/moods/{mood_id}/comments/', 'method': 'GET/POST', 'description': 'List or create reflective comments for mood entries (+2 coins per reflection)'},
                    'detail': {'url': '/api/moods/{mood_id}/comments/{comment_id}/', 'method': 'GET/PUT/DELETE', 'description': 'Retrieve, update, or delete specific reflection comments'},
                },
                'ai_insights': {
                    'motivation': {'url': '/api/suggestions/motivation/', 'method': 'GET', 'description': 'Get personalized motivational messages based on recent mood patterns'},
                    'habits': {'url': '/api/suggestions/habits/', 'method': 'GET', 'description': 'Get AI-powered habit improvement suggestions from mood-activity correlations'},
                    'patterns': {'url': '/api/moods/analysis/patterns/', 'method': 'GET', 'description': 'Advanced mood pattern analysis by time, day, and behavioral factors'},
                    'feedback': {'url': '/api/ai-feedback/', 'method': 'POST', 'description': 'Submit feedback on AI suggestions to improve recommendations'},
                },
                'behavior_engine': {
                    'challenges': {'url': '/api/coins/stake/', 'method': 'GET/POST', 'description': 'View active challenges or create new mood-based challenges with coin stakes'},
                    'nudges': {'url': '/api/nudges/next/', 'method': 'GET', 'description': 'Get next personalized nudge based on behavior patterns and time context'},
                    'coin_transactions': {'url': '/api/coins/balance/', 'method': 'GET', 'description': 'View detailed coin transaction history and earning patterns'},
                },
                'data_export': {
                    'json': {'url': '/api/moods/export/json/', 'method': 'GET', 'description': 'Export all mood data in JSON format for backup or analysis'},
                    'csv': {'url': '/api/moods/export/csv/', 'method': 'GET', 'description': 'Export mood data in CSV format for spreadsheet analysis'},
                },
                'system_monitoring': {
                    'health': {'url': '/api/health/', 'method': 'GET', 'description': 'System health check endpoint for monitoring and uptime verification'},
                    'sentiment_analysis': {'url': '/api/sentiment-analysis/', 'method': 'GET', 'description': 'Admin-only endpoint for cross-user sentiment analysis and trends'},
                },
                'documentation': {
                    'swagger': {'url': '/swagger/', 'method': 'GET', 'description': 'Interactive API documentation with Swagger UI and live testing'},
                    'redoc': {'url': '/redoc/', 'method': 'GET', 'description': 'Clean API documentation with ReDoc interface'},
                    'api_root': {'url': '/api/', 'method': 'GET', 'description': 'This comprehensive API documentation endpoint'},
                }
            },
            'features': {
                'behavior_engine': 'Gamification with coins, challenges, and streaks',
                'ai_insights': 'Machine learning-powered mood analysis and suggestions',
                'sentiment_analysis': 'Automatic sentiment scoring of mood notes',
                'time_awareness': 'Context-aware mood suggestions based on time of day',
                'pattern_recognition': 'Advanced mood pattern analysis and trend detection',
                'personalized_nudges': 'Smart engagement prompts based on user behavior',
                'data_export': 'Complete data portability in JSON and CSV formats',
                'caching': 'Optimized performance with intelligent caching',
                'authentication': 'Multiple auth methods including JWT and legacy tokens',
            },
            'coin_system': {
                'mood_log': '+1 coin per mood entry',
                'reflection': '+2 coins per mood comment/reflection',
                'ai_feedback': '+1 coin per AI suggestion feedback',
                'challenge_win': '2x stake amount for completed challenges',
                'streak_bonus': 'Bonus coins for maintaining mood logging streaks',
            },
            'status': 'online',
            'build': 'MoodSync-Behavior-Engine-v1',
            'last_updated': '2025-07-08'
        }
        return Response(api_info, status=status.HTTP_200_OK)

class UserRegisterAPIView(APIView):
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(
        tags=[SWAGGER_TAGS['AUTHENTICATION']],
        operation_summary="👤 User Registration",
        operation_description="Create a new user account with automatic profile creation and token generation",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'email', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description="Unique username"),
                'email': openapi.Schema(type=openapi.TYPE_STRING, format='email', description="Valid email address"),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description="Strong password (min 8 chars)"),
                'first_name': openapi.Schema(type=openapi.TYPE_STRING, description="Optional first name"),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING, description="Optional last name")
            }
        ),
        responses={
            201: openapi.Response(
                description="Registration successful",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'user': openapi.Schema(type=openapi.TYPE_OBJECT),
                        'token': openapi.Schema(type=openapi.TYPE_STRING, description="Authentication token"),
                        'message': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            ),
            400: openapi.Response(description="Validation errors")
        }
    )
    def post(self, request):
        """Register a new user"""
        serializer = UserRegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Generate token for the new user
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'user': UserSerializer(user).data,
                'token': token.key,
                'message': 'Registration successful!'
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginAPIView(APIView):
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(
        tags=[SWAGGER_TAGS['AUTHENTICATION']],
        operation_summary="🔑 User Login (Legacy + JWT)",
        operation_description="Login with username/password and receive both legacy token and JWT tokens for maximum compatibility",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['username', 'password'],
            properties={
                'username': openapi.Schema(type=openapi.TYPE_STRING, description="Username or email"),
                'password': openapi.Schema(type=openapi.TYPE_STRING, description="User password")
            }
        ),
        responses={
            200: openapi.Response(
                description="Login successful",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'user': openapi.Schema(type=openapi.TYPE_OBJECT),
                        'token': openapi.Schema(type=openapi.TYPE_STRING, description="Legacy token"),
                        'refresh': openapi.Schema(type=openapi.TYPE_STRING, description="JWT refresh token"),
                        'access': openapi.Schema(type=openapi.TYPE_STRING, description="JWT access token"),
                        'message': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            ),
            401: openapi.Response(description="Invalid credentials"),
            400: openapi.Response(description="Missing username or password")
        }
    )
    def post(self, request):
        """Login a user and return both standard token and JWT tokens"""
        username = request.data.get('username')
        password = request.data.get('password')
        
        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                login(request, user)
                
                # Create token auth
                token, created = Token.objects.get_or_create(user=user)
                
                # Create JWT tokens
                refresh = RefreshToken.for_user(user)
                
                return Response({
                    'user': UserSerializer(user).data,
                    'token': token.key,  # Legacy token
                    'refresh': str(refresh),  # JWT refresh token
                    'access': str(refresh.access_token),  # JWT access token
                    'message': 'Login successful!'
                }, status=status.HTTP_200_OK)
            return Response({'error': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({'error': 'Please provide both username and password'}, 
                       status=status.HTTP_400_BAD_REQUEST)

class UserLogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        tags=[SWAGGER_TAGS['AUTHENTICATION']],
        operation_summary="🚪 User Logout",
        operation_description="Logout user and invalidate authentication token. Requires valid authentication.",
        responses={
            200: openapi.Response(
                description="Logout successful",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            ),
            401: openapi.Response(description="Authentication required"),
            500: openapi.Response(description="Server error")
        }
    )
    def post(self, request):
        """Logout user and invalidate token"""
        try:
            # Remove token to force re-login
            request.user.auth_token.delete()
            logout(request)
            return Response({'message': 'Logout successful!'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class UserProfileAPIView(APIView):
    """View and update user profile information"""
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        tags=[SWAGGER_TAGS['PROFILE_MANAGEMENT']],
        operation_summary="👤 Get User Profile",
        operation_description="Retrieve current user's profile information including personal details and stats",
        responses={
            200: openapi.Response(
                description="User profile data",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'username': openapi.Schema(type=openapi.TYPE_STRING),
                        'email': openapi.Schema(type=openapi.TYPE_STRING),
                        'first_name': openapi.Schema(type=openapi.TYPE_STRING),
                        'last_name': openapi.Schema(type=openapi.TYPE_STRING),
                        'profile': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'age': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'coin_balance': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'clarity_score': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'streak_count': openapi.Schema(type=openapi.TYPE_INTEGER)
                            }
                        )
                    }
                )
            ),
            401: openapi.Response(description="Authentication required")
        }
    )
    def get(self, request):
        """Get user profile"""
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        tags=[SWAGGER_TAGS['PROFILE_MANAGEMENT']],
        operation_summary="✏️ Update User Profile (Complete)",
        operation_description="Update user profile with all fields (complete replacement). Age can be provided at top level or nested under profile.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'first_name': openapi.Schema(type=openapi.TYPE_STRING, description="First name"),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING, description="Last name"),
                'email': openapi.Schema(type=openapi.TYPE_STRING, format='email', description="Email address"),
                'age': openapi.Schema(type=openapi.TYPE_INTEGER, minimum=13, maximum=120, description="User's age (top-level)"),
                'profile': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'age': openapi.Schema(type=openapi.TYPE_INTEGER, minimum=13, maximum=120, description="User's age (nested)")
                    },
                    description="Profile data (alternative to top-level age)"
                )
            }
        ),
        responses={
            200: openapi.Response(description="Profile updated successfully"),
            400: openapi.Response(description="Validation errors"),
            401: openapi.Response(description="Authentication required")
        }
    )
    def put(self, request):
        """Update user profile (including age)"""
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        tags=[SWAGGER_TAGS['PROFILE_MANAGEMENT']],
        operation_summary="📝 Update User Profile (Partial)",
        operation_description="Partially update user profile (only provided fields will be updated). Age can be provided at top level or nested under profile.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'first_name': openapi.Schema(type=openapi.TYPE_STRING, description="First name (optional)"),
                'last_name': openapi.Schema(type=openapi.TYPE_STRING, description="Last name (optional)"),
                'email': openapi.Schema(type=openapi.TYPE_STRING, format='email', description="Email address (optional)"),
                'age': openapi.Schema(type=openapi.TYPE_INTEGER, minimum=13, maximum=120, description="User's age (top-level, optional)"),
                'profile': openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'age': openapi.Schema(type=openapi.TYPE_INTEGER, minimum=13, maximum=120, description="User's age (nested, optional)")
                    },
                    description="Profile data (alternative to top-level age)"
                )
            }
        ),
        responses={
            200: openapi.Response(description="Profile updated successfully"),
            400: openapi.Response(description="Validation errors"),
            401: openapi.Response(description="Authentication required")
        }
    )
    def patch(self, request):
        # Allow PATCH for partial updates (e.g., just age)
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordChangeAPIView(APIView):
    """Change user password"""
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        tags=[SWAGGER_TAGS['AUTHENTICATION']],
        operation_summary="🔐 Change Password",
        operation_description="Change user password with old password verification. Generates new authentication token.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['old_password', 'new_password'],
            properties={
                'old_password': openapi.Schema(type=openapi.TYPE_STRING, description="Current password for verification"),
                'new_password': openapi.Schema(type=openapi.TYPE_STRING, description="New password (min 8 characters)")
            }
        ),
        responses={
            200: openapi.Response(
                description="Password changed successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING),
                        'new_token': openapi.Schema(type=openapi.TYPE_STRING, description="New authentication token")
                    }
                )
            ),
            400: openapi.Response(description="Validation errors or incorrect old password"),
            401: openapi.Response(description="Authentication required")
        }
    )
    def post(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        if serializer.is_valid():
            # Check old password is correct
            user = request.user
            if not user.check_password(serializer.validated_data['old_password']):
                return Response(
                    {'old_password': 'Incorrect password'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Set new password
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            
            # Update token to force re-login on other devices
            Token.objects.filter(user=user).delete()
            new_token = Token.objects.create(user=user)
            
            return Response({
                'message': 'Password changed successfully',
                'new_token': new_token.key
            }, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MoodCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        tags=[SWAGGER_TAGS['MOOD_TRACKING']],
        operation_summary="📝 Log New Mood Entry",
        operation_description="Create a new mood entry with automatic sentiment analysis and streak tracking",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['mood', 'rating'],
            properties={
                'mood': openapi.Schema(type=openapi.TYPE_STRING, description="Mood description (e.g., 'Happy', 'Anxious')"),
                'rating': openapi.Schema(type=openapi.TYPE_INTEGER, minimum=1, maximum=10, description="Mood rating from 1-10"),
                'notes': openapi.Schema(type=openapi.TYPE_STRING, description="Optional detailed notes about your mood"),
                'activities': openapi.Schema(type=openapi.TYPE_STRING, description="Activities associated with this mood")
            }
        ),
        responses={
            201: openapi.Response(
                description="Mood entry created successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'mood': openapi.Schema(type=openapi.TYPE_STRING),
                        'rating': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'notes': openapi.Schema(type=openapi.TYPE_STRING),
                        'sentiment': openapi.Schema(type=openapi.TYPE_NUMBER, description="Auto-calculated sentiment score"),
                        'created_at': openapi.Schema(type=openapi.TYPE_STRING, format='datetime')
                    }
                )
            ),
            400: openapi.Response(description="Validation errors")
        }
    )
    def post(self, request):
        """Create a new mood entry"""
        serializer = MoodSerializer(data=request.data)
        if serializer.is_valid():
            # Create but don't save the mood instance yet
            mood_entry = serializer.save(user=request.user)
            
            # Process mood text
            mood_entry.mood = mood_entry.mood.capitalize()
            
            # Perform sentiment analysis if notes provided
            if mood_entry.notes:
                sentiment = TextBlob(mood_entry.notes).sentiment
                mood_entry.sentiment = sentiment.polarity if sentiment.polarity is not None else 0.0
            
            # Now save the instance with additional data
            mood_entry.save()
            
            return Response(MoodSerializer(mood_entry).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        tags=[SWAGGER_TAGS['MOOD_TRACKING']],
        operation_summary="🎭 Get Time-Aware Mood Options",
        operation_description="Retrieve mood options appropriate for the current time of day, along with suggested activities",
        responses={
            200: openapi.Response(
                description="Time-aware mood options and context",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'mood_options': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING),
                            description="List of mood options appropriate for current time"
                        ),
                        'time_context': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'period': openapi.Schema(type=openapi.TYPE_STRING),
                                'greeting': openapi.Schema(type=openapi.TYPE_STRING),
                                'suggested_activities': openapi.Schema(
                                    type=openapi.TYPE_ARRAY,
                                    items=openapi.Schema(type=openapi.TYPE_STRING)
                                )
                            }
                        )
                    }
                )
            )
        }
    )
    def get(self, request):
        """Get time-aware mood options and context"""
        current_time = timezone.now()
        time_context = TimeOfDayContext.get_context(current_time)
        
        # Base mood options
        base_moods = ['Happy', 'Sad', 'Anxious', 'Excited', 'Tired', 'Content', 'Angry', 'Calm', 'Stressed', 'Relaxed']
        
        # Get time-appropriate mood suggestions
        time_appropriate_moods = time_context['mood_suggestions']
        
        # Combine and prioritize time-appropriate moods
        all_moods = list(dict.fromkeys(time_appropriate_moods + base_moods))  # Remove duplicates, preserve order
        
        return Response({
            'mood_options': [mood.capitalize() for mood in all_moods],
            'time_context': {
                'period': time_context['period'],
                'greeting': time_context['greeting'],
                'suggested_activities': time_context['activities'],
                'energy_level': time_context['energy_level'],
                'focus': time_context['focus']
            }
        }, status=status.HTTP_200_OK)
    
# class MoodCommentViewSet(APIView): # Should be MoodCommentAPIView if not a ViewSet
#     """
#     LEGACY VIEW: This view is for the MoodComment model, which is considered legacy.
#     Please use CommentListCreateAPIView and CommentDetailAPIView for new development.
#     This will be removed in a future version.
#     """
#     serializer_class = MoodCommentSerializer # This serializer is also marked legacy
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         """Get queryset for mood comments"""
#         queryset = MoodComment.objects.filter(user=request.user)
#         serializer = self.serializer_class(queryset, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)
    
#     def post(self, request):
#         """Create a new comment for a mood entry"""
#         serializer = self.serializer_class(data=request.data)
#         if serializer.is_valid():
#             # Ensure the mood entry exists and belongs to the user
#             mood_entry_id = request.data.get('mood_entry')
#             try:
#                 mood_entry = Mood.objects.get(id=mood_entry_id, user=request.user)
#                 serializer.save(mood_entry=mood_entry)
#                 return Response(serializer.data, status=status.HTTP_201_CREATED)
#             except Mood.DoesNotExist:
#                 return Response({'error': 'Mood entry not found or you do not have permission'}, 
#                                 status=status.HTTP_404_NOT_FOUND)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class MoodHistoryAPIView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [JSONParser, FormParser, MultiPartParser]  # Support different request formats
    
    @swagger_auto_schema(
        tags=[SWAGGER_TAGS['MOOD_TRACKING']],
        operation_summary="📊 Get Mood History",
        operation_description="Retrieve user's mood history with optional filtering and caching. Supports pagination and date range filtering.",
        manual_parameters=[
            openapi.Parameter(
                'limit',
                openapi.IN_QUERY,
                description="Maximum number of entries to return",
                type=openapi.TYPE_INTEGER
            ),
            openapi.Parameter(
                'start_date',
                openapi.IN_QUERY,
                description="Start date for filtering (YYYY-MM-DD format)",
                type=openapi.TYPE_STRING,
                format='date'
            ),
            openapi.Parameter(
                'end_date',
                openapi.IN_QUERY,
                description="End date for filtering (YYYY-MM-DD format)",
                type=openapi.TYPE_STRING,
                format='date'
            ),
            openapi.Parameter(
                'mood',
                openapi.IN_QUERY,
                description="Filter by specific mood (case-insensitive)",
                type=openapi.TYPE_STRING
            ),
            openapi.Parameter(
                'no_cache',
                openapi.IN_QUERY,
                description="Skip cache and fetch fresh data",
                type=openapi.TYPE_BOOLEAN
            )
        ],
        responses={
            200: openapi.Response(
                description="Mood history data",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'mood': openapi.Schema(type=openapi.TYPE_STRING),
                            'rating': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'notes': openapi.Schema(type=openapi.TYPE_STRING),
                            'activities': openapi.Schema(type=openapi.TYPE_STRING),
                            'sentiment': openapi.Schema(type=openapi.TYPE_NUMBER),
                            'created_at': openapi.Schema(type=openapi.TYPE_STRING, format='datetime')
                        }
                    )
                )
            ),
            400: openapi.Response(description="Invalid date format"),
            401: openapi.Response(description="Authentication required")
        }
    )
    def get(self, request):
        """Get mood history for the authenticated user with caching"""
        # Cache key based on user ID and query params
        cache_key = f"mood_history_{request.user.id}_{hash(frozenset(request.query_params.items()))}"
        
        # Try to get from cache first
        cached_response = cache.get(cache_key)
        if cached_response and not request.query_params.get('no_cache'):
            return Response(cached_response, status=status.HTTP_200_OK)
        
        # Optional query parameters
        limit = request.query_params.get('limit', None)
        start_date = request.query_params.get('start_date', None)
        end_date = request.query_params.get('end_date', None)
        mood_filter = request.query_params.get('mood', None)
        
        # Build query
        moods_query = Mood.objects.filter(user=request.user)
        
        if start_date:
            try:
                start_date = datetime.strptime(start_date, '%Y-%m-%d').date()
                moods_query = moods_query.filter(created_at__date__gte=start_date)
            except ValueError:
                return Response({'error': 'Invalid start_date format. Use YYYY-MM-DD'},
                               status=status.HTTP_400_BAD_REQUEST)
        
        if end_date:
            try:
                end_date = datetime.strptime(end_date, '%Y-%m-%d').date()
                moods_query = moods_query.filter(created_at__date__lte=end_date)
            except ValueError:
                return Response({'error': 'Invalid end_date format. Use YYYY-MM-DD'},
                               status=status.HTTP_400_BAD_REQUEST)
        
        if mood_filter:
            moods_query = moods_query.filter(mood__iexact=mood_filter)
        
        # Order by most recent first
        moods_query = moods_query.order_by('-created_at')
        
        # Apply limit if specified
        if limit and limit.isdigit():
            moods_query = moods_query[:int(limit)]
        
        serializer = MoodSerializer(moods_query, many=True)
        
        # Cache for 5 minutes
        cache.set(cache_key, serializer.data, 60 * 5)
        
        return Response(serializer.data, status=status.HTTP_200_OK)

class MoodSummaryAPIView(APIView):
    """Get summary statistics of user's moods"""
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        tags=[SWAGGER_TAGS['MOOD_TRACKING']],
        operation_summary="📈 Get Mood Summary Statistics",
        operation_description="Retrieve comprehensive mood statistics including counts, averages, and sentiment distribution",
        responses={
            200: openapi.Response(
                description="Mood summary statistics",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'total_entries': openapi.Schema(type=openapi.TYPE_INTEGER, description="Total number of mood entries"),
                        'mood_counts': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            description="Count of each mood type"
                        ),
                        'average_sentiment': openapi.Schema(type=openapi.TYPE_NUMBER, description="Average sentiment score"),
                        'mood_distribution': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'positive': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'neutral': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'negative': openapi.Schema(type=openapi.TYPE_INTEGER)
                            }
                        )
                    }
                )
            ),
            401: openapi.Response(description="Authentication required")
        }
    )
    def get(self, request):
        # All moods for the user
        moods = Mood.objects.filter(user=request.user)
        
        # Count of each mood type
        mood_counts = {}
        for mood in moods:
            mood_name = mood.mood.lower()
            if mood_name in mood_counts:
                mood_counts[mood_name] += 1
            else:
                mood_counts[mood_name] = 1
        
        # Get average sentiment if available
        avg_sentiment = 0
        sentiment_moods = moods.filter(sentiment__isnull=False)
        if sentiment_moods.exists():
            avg_sentiment = sentiment_moods.aggregate(Avg('sentiment'))['sentiment__avg']
        
        return Response({
            'total_entries': moods.count(),
            'mood_counts': mood_counts,
            'average_sentiment': avg_sentiment,
            'mood_distribution': {
                'positive': moods.filter(sentiment__gt=0).count(),
                'neutral': moods.filter(sentiment=0).count(),
                'negative': moods.filter(sentiment__lt=0).count(),
            }
        }, status=status.HTTP_200_OK)

class MoodTrendsAPIView(APIView):
    """Get mood trends over time"""
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        tags=[SWAGGER_TAGS['MOOD_TRACKING']],
        operation_summary="📉 Get Mood Trends Over Time",
        operation_description="Analyze mood trends over a specified time period with daily aggregations and sentiment tracking",
        manual_parameters=[
            openapi.Parameter(
                'days',
                openapi.IN_QUERY,
                description="Number of days to analyze (default: 30, min: 1, max: 365)",
                type=openapi.TYPE_INTEGER
            )
        ],
        responses={
            200: openapi.Response(
                description="Mood trends data",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'days_analyzed': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'total_entries': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'trends': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'date': openapi.Schema(type=openapi.TYPE_STRING, format='date'),
                                    'moods': openapi.Schema(type=openapi.TYPE_OBJECT, description="Mood counts for the day"),
                                    'avg_sentiment': openapi.Schema(type=openapi.TYPE_NUMBER),
                                    'count': openapi.Schema(type=openapi.TYPE_INTEGER)
                                }
                            )
                        )
                    }
                )
            ),
            401: openapi.Response(description="Authentication required")
        }
    )
    def get(self, request):
        # Get time range from query params (defaults to last 30 days)
        days = int(request.query_params.get('days', 30))
        
        # Limit to reasonable values
        if days < 1:
            days = 1
        elif days > 365:
            days = 365
            
        start_date = datetime.now() - timedelta(days=days)
        
        # Get moods within time range
        moods = Mood.objects.filter(
            user=request.user,
            created_at__gte=start_date
        ).order_by('created_at')
        
        # Group by date and mood
        date_moods = {}
        for mood in moods:
            date_str = mood.created_at.strftime('%Y-%m-%d')
            if date_str not in date_moods:
                date_moods[date_str] = {'date': date_str, 'moods': {}, 'avg_sentiment': 0, 'count': 0}
            
            # Increment mood count
            mood_name = mood.mood.lower()
            if mood_name in date_moods[date_str]['moods']:
                date_moods[date_str]['moods'][mood_name] += 1
            else:
                date_moods[date_str]['moods'][mood_name] = 1
            
            # Update average sentiment
            if mood.sentiment is not None:
                current_count = date_moods[date_str]['count']
                current_avg = date_moods[date_str]['avg_sentiment']
                new_count = current_count + 1
                new_avg = ((current_avg * current_count) + mood.sentiment) / new_count
                date_moods[date_str]['avg_sentiment'] = new_avg
                date_moods[date_str]['count'] = new_count
        
        # Convert to list and sort by date
        trends = list(date_moods.values())
        trends.sort(key=lambda x: x['date'])
        
        return Response({
            'days_analyzed': days,
            'total_entries': moods.count(),
            'trends': trends
        }, status=status.HTTP_200_OK)

class ExportMoodJsonAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        tags=[SWAGGER_TAGS['DATA_EXPORT']],
        operation_summary="📊 Export Moods as JSON",
        operation_description="Export all user's mood entries in JSON format for backup or external analysis",
        responses={
            200: openapi.Response(
                description="JSON export of all mood entries",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'mood': openapi.Schema(type=openapi.TYPE_STRING),
                            'rating': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'notes': openapi.Schema(type=openapi.TYPE_STRING),
                            'activities': openapi.Schema(type=openapi.TYPE_STRING),
                            'sentiment': openapi.Schema(type=openapi.TYPE_NUMBER),
                            'created_at': openapi.Schema(type=openapi.TYPE_STRING, format='datetime')
                        }
                    )
                )
            )
        }
    )
    def get(self, request):
        """Export user's moods as JSON"""
        moods = Mood.objects.filter(user=request.user)
        serializer = MoodSerializer(moods, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ExportMoodCsvAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        tags=[SWAGGER_TAGS['DATA_EXPORT']],
        operation_summary="📈 Export Moods as CSV",
        operation_description="Export all user's mood entries in CSV format suitable for spreadsheet analysis",
        responses={
            200: openapi.Response(
                description="CSV file download",
                schema=openapi.Schema(
                    type=openapi.TYPE_STRING,
                    format='binary',
                    description="CSV file containing mood data"
                ),
                headers={
                    'Content-Disposition': openapi.Schema(type=openapi.TYPE_STRING, description='attachment; filename="moods.csv"')
                }
            )
        }
    )
    def get(self, request):
        """Export user's moods as CSV"""
        moods = Mood.objects.filter(user=request.user)
        
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="moods.csv"'
        
        writer = csv.writer(response)
        writer.writerow(['Mood', 'Notes', 'Sentiment', 'Date'])
        
        for mood in moods:
            writer.writerow([
                mood.mood, 
                mood.notes, 
                mood.sentiment if mood.sentiment is not None else 'N/A', 
                mood.created_at.strftime('%Y-%m-%d %H:%M:%S')
            ])
            
        return response

class SentimentAnalysisAPIView(APIView):
    """For admin users to analyze sentiment across users"""
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        # Aggregate sentiments by user
        user_average_sentiments = (
            Mood.objects.filter(sentiment__isnull=False)
            .values('user__username')
            .annotate(average_sentiment=Avg('sentiment'))
            .order_by('user__username')
        )
        
        return Response(list(user_average_sentiments), status=status.HTTP_200_OK)

# Individual Mood CRUD Operations
class MoodDetailAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get_mood(self, mood_id, user):
        """Helper method to get a mood entry and verify ownership"""
        try:
            return Mood.objects.get(id=mood_id, user=user)
        except Mood.DoesNotExist:
            return None
    
    @swagger_auto_schema(
        tags=[SWAGGER_TAGS['MOOD_TRACKING']],
        operation_summary="🔍 Get Specific Mood Entry",
        operation_description="Retrieve a specific mood entry by ID. User can only access their own mood entries.",
        manual_parameters=[
            openapi.Parameter(
                'mood_id',
                openapi.IN_PATH,
                description="ID of the mood entry to retrieve",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="Mood entry details",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'mood': openapi.Schema(type=openapi.TYPE_STRING),
                        'rating': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'notes': openapi.Schema(type=openapi.TYPE_STRING),
                        'activities': openapi.Schema(type=openapi.TYPE_STRING),
                        'sentiment': openapi.Schema(type=openapi.TYPE_NUMBER),
                        'created_at': openapi.Schema(type=openapi.TYPE_STRING, format='datetime')
                    }
                )
            ),
            404: openapi.Response(description="Mood entry not found or no permission"),
            401: openapi.Response(description="Authentication required")
        }
    )
    def get(self, request, mood_id):
        """Get a specific mood entry"""
        mood = self.get_mood(mood_id, request.user)
        if not mood:
            return Response({'error': 'Mood not found or you do not have permission'}, 
                            status=status.HTTP_404_NOT_FOUND)
        
        serializer = MoodSerializer(mood)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    @swagger_auto_schema(
        tags=[SWAGGER_TAGS['MOOD_TRACKING']],
        operation_summary="✏️ Update Specific Mood Entry",
        operation_description="Update a specific mood entry. Automatically re-analyzes sentiment if notes are updated.",
        manual_parameters=[
            openapi.Parameter(
                'mood_id',
                openapi.IN_PATH,
                description="ID of the mood entry to update",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'mood': openapi.Schema(type=openapi.TYPE_STRING, description="Updated mood description"),
                'rating': openapi.Schema(type=openapi.TYPE_INTEGER, minimum=1, maximum=10, description="Updated mood rating"),
                'notes': openapi.Schema(type=openapi.TYPE_STRING, description="Updated notes (triggers sentiment re-analysis)"),
                'activities': openapi.Schema(type=openapi.TYPE_STRING, description="Updated activities")
            }
        ),
        responses={
            200: openapi.Response(description="Mood entry updated successfully"),
            400: openapi.Response(description="Validation errors"),
            404: openapi.Response(description="Mood entry not found or no permission"),
            401: openapi.Response(description="Authentication required")
        }
    )
    def put(self, request, mood_id):
        """Update a specific mood entry"""
        mood = self.get_mood(mood_id, request.user)
        if not mood:
            return Response({'error': 'Mood not found or you do not have permission'}, 
                            status=status.HTTP_404_NOT_FOUND)
        
        serializer = MoodSerializer(mood, data=request.data, partial=True)
        if serializer.is_valid():
            mood_entry = serializer.save()
            
            # Re-analyze sentiment if notes were updated
            if 'notes' in request.data and mood_entry.notes:
                sentiment = TextBlob(mood_entry.notes).sentiment
                mood_entry.sentiment = sentiment.polarity if sentiment.polarity is not None else 0.0
                mood_entry.save()
            
            return Response(MoodSerializer(mood_entry).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @swagger_auto_schema(
        tags=[SWAGGER_TAGS['MOOD_TRACKING']],
        operation_summary="🗑️ Delete Specific Mood Entry",
        operation_description="Permanently delete a specific mood entry. This action cannot be undone.",
        manual_parameters=[
            openapi.Parameter(
                'mood_id',
                openapi.IN_PATH,
                description="ID of the mood entry to delete",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            204: openapi.Response(
                description="Mood entry deleted successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            ),
            404: openapi.Response(description="Mood entry not found or no permission"),
            401: openapi.Response(description="Authentication required")
        }
    )
    def delete(self, request, mood_id):
        """Delete a specific mood entry"""
        mood = self.get_mood(mood_id, request.user)
        if not mood:
            return Response({'error': 'Mood not found or you do not have permission'}, 
                            status=status.HTTP_404_NOT_FOUND)
        
        mood.delete()
        return Response({'message': 'Mood deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

# Implement health check endpoint
class HealthCheckAPIView(APIView):
    permission_classes = [AllowAny]
    
    @swagger_auto_schema(
        tags=[SWAGGER_TAGS['ADMIN_MONITORING']],
        operation_summary="❤️ System Health Check",
        operation_description="Check if the API system is running and responsive. No authentication required.",
        responses={
            200: openapi.Response(
                description="System is healthy and operational",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'status': openapi.Schema(type=openapi.TYPE_STRING, description="System status"),
                        'timestamp': openapi.Schema(type=openapi.TYPE_STRING, format='datetime', description="Current server time"),
                        'version': openapi.Schema(type=openapi.TYPE_STRING, description="API version")
                    }
                )
            )
        }
    )
    def get(self, request):
        """Health check endpoint to verify API is running"""
        return Response({
            'status': 'healthy',
            'timestamp': datetime.now().isoformat(),
            'version': '1.0.0',
        }, status=status.HTTP_200_OK)

# Comment views
class CommentListCreateAPIView(generics.ListCreateAPIView):
    """API view to list and create comments for a specific mood"""
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        tags=[SWAGGER_TAGS['MOOD_TRACKING']],
        operation_summary="💬 List Comments for Mood Entry",
        operation_description="Retrieve all comments for a specific mood entry. Only mood owner can view comments.",
        manual_parameters=[
            openapi.Parameter(
                'mood_id',
                openapi.IN_PATH,
                description="ID of the mood entry to get comments for",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="List of comments for the mood entry",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'content': openapi.Schema(type=openapi.TYPE_STRING),
                            'created_at': openapi.Schema(type=openapi.TYPE_STRING, format='datetime'),
                            'updated_at': openapi.Schema(type=openapi.TYPE_STRING, format='datetime')
                        }
                    )
                )
            ),
            403: openapi.Response(description="Permission denied - not your mood entry"),
            404: openapi.Response(description="Mood entry not found")
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @swagger_auto_schema(
        tags=[SWAGGER_TAGS['MOOD_TRACKING']],
        operation_summary="💬 Add Comment to Mood Entry",
        operation_description="Add a new comment to a mood entry. Earns +2 coins for reflection. Only mood owner can add comments.",
        manual_parameters=[
            openapi.Parameter(
                'mood_id',
                openapi.IN_PATH,
                description="ID of the mood entry to comment on",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['content'],
            properties={
                'content': openapi.Schema(type=openapi.TYPE_STRING, description="Comment content")
            }
        ),
        responses={
            201: openapi.Response(
                description="Comment created successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'content': openapi.Schema(type=openapi.TYPE_STRING),
                        'created_at': openapi.Schema(type=openapi.TYPE_STRING, format='datetime'),
                        'updated_at': openapi.Schema(type=openapi.TYPE_STRING, format='datetime')
                    }
                )
            ),
            400: openapi.Response(description="Validation errors"),
            403: openapi.Response(description="Permission denied - not your mood entry"),
            404: openapi.Response(description="Mood entry not found")
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    
    def get_queryset(self):
        mood_id = self.kwargs.get('mood_id')
        mood = get_object_or_404(Mood, id=mood_id)
        
        # Security check - users can only see comments on their own moods
        if mood.user != self.request.user:
            raise PermissionDenied("You do not have permission to view these comments")
        
        return Comment.objects.filter(mood=mood)
    
    def get_serializer_context(self):
        context = super().get_serializer_context()
        context['mood_id'] = self.kwargs.get('mood_id')
        return context

class CommentDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    """API view to retrieve, update, and delete a comment"""
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = 'comment_id'
    
    @swagger_auto_schema(
        tags=[SWAGGER_TAGS['MOOD_TRACKING']],
        operation_summary="💬 Get Specific Comment",
        operation_description="Retrieve details of a specific comment. Only comment owner can view.",
        manual_parameters=[
            openapi.Parameter(
                'mood_id',
                openapi.IN_PATH,
                description="ID of the mood entry containing the comment",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
            openapi.Parameter(
                'comment_id',
                openapi.IN_PATH,
                description="ID of the comment to retrieve",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            200: openapi.Response(
                description="Comment details",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'content': openapi.Schema(type=openapi.TYPE_STRING),
                        'created_at': openapi.Schema(type=openapi.TYPE_STRING, format='datetime'),
                        'updated_at': openapi.Schema(type=openapi.TYPE_STRING, format='datetime')
                    }
                )
            ),
            403: openapi.Response(description="Permission denied - not your comment"),
            404: openapi.Response(description="Comment not found")
        }
    )
    def get(self, request, *args, **kwargs):
        return super().get(request, *args, **kwargs)
    
    @swagger_auto_schema(
        tags=[SWAGGER_TAGS['MOOD_TRACKING']],
        operation_summary="💬 Update Comment",
        operation_description="Update content of a specific comment. Only comment owner can update.",
        manual_parameters=[
            openapi.Parameter(
                'mood_id',
                openapi.IN_PATH,
                description="ID of the mood entry containing the comment",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
            openapi.Parameter(
                'comment_id',
                openapi.IN_PATH,
                description="ID of the comment to update",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'content': openapi.Schema(type=openapi.TYPE_STRING, description="Updated comment content")
            }
        ),
        responses={
            200: openapi.Response(
                description="Comment updated successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'content': openapi.Schema(type=openapi.TYPE_STRING),
                        'created_at': openapi.Schema(type=openapi.TYPE_STRING, format='datetime'),
                        'updated_at': openapi.Schema(type=openapi.TYPE_STRING, format='datetime')
                    }
                )
            ),
            400: openapi.Response(description="Validation errors"),
            403: openapi.Response(description="Permission denied - not your comment"),
            404: openapi.Response(description="Comment not found")
        }
    )
    def put(self, request, *args, **kwargs):
        return super().put(request, *args, **kwargs)
    
    @swagger_auto_schema(
        tags=[SWAGGER_TAGS['MOOD_TRACKING']],
        operation_summary="💬 Partially Update Comment",
        operation_description="Partially update content of a specific comment. Only comment owner can update.",
        manual_parameters=[
            openapi.Parameter(
                'mood_id',
                openapi.IN_PATH,
                description="ID of the mood entry containing the comment",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
            openapi.Parameter(
                'comment_id',
                openapi.IN_PATH,
                description="ID of the comment to update",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            properties={
                'content': openapi.Schema(type=openapi.TYPE_STRING, description="Updated comment content")
            }
        ),
        responses={
            200: openapi.Response(
                description="Comment updated successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'content': openapi.Schema(type=openapi.TYPE_STRING),
                        'created_at': openapi.Schema(type=openapi.TYPE_STRING, format='datetime'),
                        'updated_at': openapi.Schema(type=openapi.TYPE_STRING, format='datetime')
                    }
                )
            ),
            400: openapi.Response(description="Validation errors"),
            403: openapi.Response(description="Permission denied - not your comment"),
            404: openapi.Response(description="Comment not found")
        }
    )
    def patch(self, request, *args, **kwargs):
        return super().patch(request, *args, **kwargs)
    
    @swagger_auto_schema(
        tags=[SWAGGER_TAGS['MOOD_TRACKING']],
        operation_summary="💬 Delete Comment",
        operation_description="Permanently delete a specific comment. Only comment owner can delete.",
        manual_parameters=[
            openapi.Parameter(
                'mood_id',
                openapi.IN_PATH,
                description="ID of the mood entry containing the comment",
                type=openapi.TYPE_INTEGER,
                required=True
            ),
            openapi.Parameter(
                'comment_id',
                openapi.IN_PATH,
                description="ID of the comment to delete",
                type=openapi.TYPE_INTEGER,
                required=True
            )
        ],
        responses={
            204: openapi.Response(description="Comment deleted successfully"),
            403: openapi.Response(description="Permission denied - not your comment"),
            404: openapi.Response(description="Comment not found")
        }
    )
    def delete(self, request, *args, **kwargs):
        return super().delete(request, *args, **kwargs)
    
    def get_queryset(self):
        mood_id = self.kwargs.get('mood_id')
        comment_id = self.kwargs.get('comment_id')
        
        # Get the comment
        comment = get_object_or_404(Comment, id=comment_id, mood_id=mood_id)
        
        # Security check - users can only manage their own comments
        if comment.user != self.request.user:
            raise PermissionDenied("You do not have permission to modify this comment")
        
        return Comment.objects.filter(id=comment_id)

# AI Suggestion views
class MotivationSuggestionAPIView(APIView):
    """API view to get AI-generated motivational content by calling the AI microservice"""
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=[SWAGGER_TAGS['AI_INSIGHTS']],
        operation_summary="💪 Get AI Motivational Messages",
        operation_description="Receive personalized motivational content based on recent mood trends and user profile",
        responses={
            200: openapi.Response(
                description="Personalized motivational content",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'motivation': openapi.Schema(type=openapi.TYPE_STRING, description="AI-generated motivational message"),
                        'mood_trend': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            enum=['positive', 'neutral', 'negative'],
                            description="Detected mood trend"
                        ),
                        'personalized_with_ai': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Whether AI service was used"),
                        'source': openapi.Schema(type=openapi.TYPE_STRING, description="Source of the motivation message")
                    }
                )
            ),
            503: openapi.Response(description="AI service unavailable - fallback message provided")
        }
    )
    def get(self, request):
        ai_service_url = os.environ.get("AI_SERVICE_URL", "http://127.0.0.1:5001")
        logger.info(f"MotivationSuggestionAPIView: Using AI_SERVICE_URL={ai_service_url}")

        recent_moods = Mood.objects.filter(user=request.user).order_by('-created_at')[:5]
        if not recent_moods:
            return Response(
                {"message": "You need to log some moods first to get personalized motivation."},
                status=status.HTTP_200_OK
            )

        avg_rating = recent_moods.aggregate(avg=Avg('rating'))['avg'] or 3
        mood_trend_label = "positive" if avg_rating > 3.5 else "negative" if avg_rating < 2.5 else "neutral"
        user_name = request.user.first_name or request.user.username
        recent_mood_texts = [mood.mood for mood in recent_moods if mood.mood]
        recent_notes_texts = [mood.notes for mood in recent_moods if mood.notes]

        # Get age from profile if available, always ensure profile exists
        user_age = None
        try:
            profile = get_or_create_profile(request.user)
            user_age = profile.age
        except Exception:
            user_age = None

        # Add time-of-day consciousness
        current_time = timezone.now()
        time_context = TimeOfDayContext.get_context(current_time)

        payload = {
            "user_name": user_name,
            "mood_trend_label": mood_trend_label,
            "recent_mood_texts": recent_mood_texts,
            "recent_notes_texts": recent_notes_texts,
            "user_age": user_age,  
        }
        
        # Enhance payload with time context
        payload = TimeOfDayContext.enhance_ai_payload_with_time_context(payload, current_time)
        
        logger.debug(f"MotivationSuggestionAPIView: Time-aware payload for AI service: {payload}")

        try:
            response = requests.post(f"{ai_service_url}/motivation", json=payload, timeout=15)
            logger.info(f"MotivationSuggestionAPIView: AI service response status: {response.status_code}")
            response.raise_for_status()
            ai_response_data = response.json()
            motivation_text = ai_response_data.get("text")
            if motivation_text:
                return Response({
                    "motivation": motivation_text,
                    "mood_trend": mood_trend_label,
                    "personalized_with_ai": True,
                    "source": "AI Service",
                    "time_context": {
                        "period": time_context['period'],
                        "greeting": time_context['greeting'],
                        "suggested_activities": time_context['activities']
                    }
                })
        except requests.exceptions.RequestException as e:
            logger.error(f"MotivationSuggestionAPIView: AI service error: {str(e)}")
        except Exception as e:
            logger.error(f"MotivationSuggestionAPIView: Unexpected error: {str(e)}")

        # Fallback with time-aware message
        fallback_motivation = TimeOfDayContext.get_contextual_motivation(mood_trend_label, current_time)
        time_greeting = TimeOfDayContext.get_time_aware_greeting(user_name, current_time)
        
        return Response({
            "motivation": f"{time_greeting} {fallback_motivation}",
            "mood_trend": mood_trend_label,
            "personalized_with_ai": False,
            "source": "Time-Aware Fallback",
            "time_context": {
                "period": time_context['period'],
                "greeting": time_context['greeting'],
                "suggested_activities": time_context['activities']
            }
        }, status=status.HTTP_503_SERVICE_UNAVAILABLE)

class HabitImprovementAPIView(APIView):
    """API view to get AI-generated habit improvement suggestions by calling the AI microservice"""
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(
        tags=[SWAGGER_TAGS['AI_INSIGHTS']],
        operation_summary="🌱 Get AI Habit Improvement Suggestions",
        operation_description="Receive personalized habit suggestions based on mood-activity correlations from the last 2 weeks",
        responses={
            200: openapi.Response(
                description="AI-generated habit improvement suggestions",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'habit_suggestions': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING),
                            description="List of personalized habit suggestions"
                        ),
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description="Explanatory message"),
                        'personalized_with_ai': openapi.Schema(type=openapi.TYPE_BOOLEAN, description="Whether AI service was used"),
                        'source': openapi.Schema(type=openapi.TYPE_STRING, description="Source of the suggestions")
                    }
                )
            ),
            503: openapi.Response(description="AI service unavailable - fallback suggestions provided")
        }
    )
    def get(self, request):
        ai_service_url = os.environ.get("AI_SERVICE_URL", "http://127.0.0.1:5001")
        logger.info(f"HabitImprovementAPIView: Using AI_SERVICE_URL={ai_service_url}")

        two_weeks_ago = timezone.now() - timedelta(days=14)
        recent_moods = Mood.objects.filter(
            user=request.user,
            created_at__gte=two_weeks_ago
        ).order_by('-created_at')

        if recent_moods.count() < 3:
            return Response(
                {"message": "Need more mood data (at least 3 entries in the last 2 weeks) to provide meaningful habit suggestions."},
                status=status.HTTP_200_OK
            )

        low_mood_activities = [m.activities for m in recent_moods.filter(rating__lt=3) if m.activities]
        high_mood_activities = [m.activities for m in recent_moods.filter(rating__gt=3) if m.activities]
        user_name = request.user.first_name or request.user.username

        payload = {
            "user_name": user_name,
            "low_mood_activities": low_mood_activities,
            "high_mood_activities": high_mood_activities,
        }
        logger.debug(f"HabitImprovementAPIView: Payload for AI service: {payload}")

        try:
            response = requests.post(f"{ai_service_url}/habits", json=payload, timeout=15)
            logger.info(f"HabitImprovementAPIView: AI service response status: {response.status_code}")
            response.raise_for_status()
            ai_response_data = response.json()
            suggestions_list = ai_response_data.get("suggestions")
            if suggestions_list and isinstance(suggestions_list, list):
                return Response({
                    "habit_suggestions": suggestions_list,
                    "message": "AI-powered habit suggestions to help you cultivate wellbeing.",
                    "personalized_with_ai": True,
                    "source": "AI Service"
                }, status=status.HTTP_200_OK)
            else:
                logger.error("HabitImprovementAPIView: AI service responded but no 'suggestions' list found.")
                return Response({
                    "error": "AI service responded but no habit suggestions were returned.",
                    "habit_suggestions": [],
                    "personalized_with_ai": False,
                    "source": "AI Service (Invalid Response)"
                }, status=status.HTTP_502_BAD_GATEWAY)
        except requests.exceptions.RequestException as e:
            logger.error(f"HabitImprovementAPIView: Error calling AI service: {e}", exc_info=True)
            return Response({
                "error": "Failed to connect to AI service.",
                "habit_suggestions": [],
                "personalized_with_ai": False,
                "source": "Django Fallback (AI Service Call Failed)",
                "details": str(e)
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)

class MoodPatternAnalysisAPIView(APIView):
    """API view to analyze mood patterns and provide insights"""
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        tags=[SWAGGER_TAGS['AI_INSIGHTS']],
        operation_summary="📊 Analyze Mood Patterns",
        operation_description="Analyze mood patterns by time-of-day and day-of-week to provide personalized insights. Requires at least 7 days of mood data.",
        responses={
            200: openapi.Response(
                description="Mood pattern analysis insights",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'pattern_insights': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING),
                            description="List of insight messages about mood patterns"
                        ),
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description="General guidance message")
                    }
                )
            ),
            401: openapi.Response(description="Authentication required")
        }
    )
    def get(self, request):
        # Get moods from the last month
        month_ago = timezone.now() - timedelta(days=30)
        moods = Mood.objects.filter(
            user=request.user,
            created_at__gte=month_ago
        ).order_by('created_at')
        
        if moods.count() < 7:
            return Response(
                {"message": "Need at least a week of mood data for pattern analysis"},
                status=status.HTTP_200_OK
            )
        
        # Time-of-day analysis
        morning_moods = moods.filter(created_at__hour__lt=12).aggregate(avg=Avg('rating'))['avg'] or 0
        afternoon_moods = moods.filter(created_at__hour__gte=12, created_at__hour__lt=18).aggregate(avg=Avg('rating'))['avg'] or 0
        evening_moods = moods.filter(created_at__hour__gte=18).aggregate(avg=Avg('rating'))['avg'] or 0
        
        time_insights = []
        if morning_moods > afternoon_moods and morning_moods > evening_moods:
            time_insights.append("Your mood tends to be best in the mornings")
        elif afternoon_moods > morning_moods and afternoon_moods > evening_moods:
            time_insights.append("Your mood tends to be best in the afternoons")
        elif evening_moods > morning_moods and evening_moods > afternoon_moods:
            time_insights.append("Your mood tends to be best in the evenings")
        
        # Day-of-week analysis
        weekday_avgs = {}
        for i in range(7):
            avg = moods.filter(created_at__week_day=i+1).aggregate(avg=Avg('rating'))['avg']
            if avg:
                weekday_avgs[i] = avg
        
        if weekday_avgs:
            best_day = max(weekday_avgs.items(), key=lambda x: x[1])
            worst_day = min(weekday_avgs.items(), key=lambda x: x[1])
            
            days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            time_insights.append(f"Your mood tends to be best on {days[best_day[0]]}s")
            time_insights.append(f"Your mood tends to be worst on {days[worst_day[0]]}s")
        
        return Response({
            "pattern_insights": time_insights,
            "message": "Understanding your mood patterns can help you plan your activities better."
        })

class AISuggestionFeedbackAPIView(APIView):
    """API view to submit feedback on AI suggestions"""
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        tags=[SWAGGER_TAGS['AI_INSIGHTS']],
        operation_summary="📝 Submit AI Suggestion Feedback",
        operation_description="Submit feedback on AI-generated suggestions to help improve the system. Earns +1 coin for providing feedback.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['suggestion_type', 'suggestion_text', 'rating'],
            properties={
                'suggestion_type': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=['motivation', 'habits', 'insights', 'nudge'],
                    description="Type of AI suggestion being rated"
                ),
                'suggestion_text': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    description="The actual suggestion text that was provided"
                ),
                'rating': openapi.Schema(
                    type=openapi.TYPE_INTEGER,
                    minimum=1,
                    maximum=3,
                    description="Feedback rating (1=bad, 2=neutral, 3=good)"
                )
            }
        ),
        responses={
            201: openapi.Response(
                description="Feedback submitted successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'suggestion_type': openapi.Schema(type=openapi.TYPE_STRING),
                        'suggestion_text': openapi.Schema(type=openapi.TYPE_STRING),
                        'rating': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'created_at': openapi.Schema(type=openapi.TYPE_STRING, format='datetime')
                    }
                )
            ),
            400: openapi.Response(description="Validation errors"),
            401: openapi.Response(description="Authentication required")
        }
    )
    def post(self, request):
        serializer = AISuggestionFeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# =====================================
# BEHAVIOR ENGINE VIEWS
# =====================================

class CoinBalanceView(APIView):
    """Get user's current coin balance and recent transactions"""
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        tags=[SWAGGER_TAGS['COIN_SYSTEM']],
        operation_summary="💰 Get Coin Balance & Transaction History",
        operation_description="Retrieve current coin balance, clarity score, and recent transaction history",
        responses={
            200: openapi.Response(
                description="Coin balance and transaction data",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'balance': openapi.Schema(type=openapi.TYPE_INTEGER, description="Current coin balance"),
                        'clarity_score': openapi.Schema(type=openapi.TYPE_NUMBER, description="User's clarity score (0-100)"),
                        'transactions': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'transaction_type': openapi.Schema(type=openapi.TYPE_STRING),
                                    'amount': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'balance_after': openapi.Schema(type=openapi.TYPE_INTEGER),
                                    'created_at': openapi.Schema(type=openapi.TYPE_STRING, format='datetime')
                                }
                            ),
                            description="Recent transaction history (last 20)"
                        )
                    }
                )
            ),
            401: openapi.Response(description="Authentication required")
        }
    )
    def get(self, request):
        profile = get_or_create_profile(request.user)
        
        # Get recent transactions
        transactions = CoinTransaction.objects.filter(
            profile=profile
        ).order_by('-created_at')[:20]
        
        transaction_serializer = CoinTransactionSerializer(transactions, many=True)
        
        return Response({
            'balance': profile.coin_balance,
            'clarity_score': profile.clarity_score,
            'transactions': transaction_serializer.data
        })

class ChallengeView(APIView):
    """Create and manage challenges"""
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        tags=[SWAGGER_TAGS['COIN_SYSTEM']],
        operation_summary="🎯 Get User's Challenges",
        operation_description="Retrieve all challenges for the authenticated user, ordered by creation date",
        responses={
            200: openapi.Response(
                description="List of user's challenges",
                schema=openapi.Schema(
                    type=openapi.TYPE_ARRAY,
                    items=openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'challenge_type': openapi.Schema(type=openapi.TYPE_STRING),
                            'stake': openapi.Schema(type=openapi.TYPE_INTEGER),
                            'start_date': openapi.Schema(type=openapi.TYPE_STRING, format='date'),
                            'end_date': openapi.Schema(type=openapi.TYPE_STRING, format='date'),
                            'completed': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                            'settled': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                            'created_at': openapi.Schema(type=openapi.TYPE_STRING, format='datetime')
                        }
                    )
                )
            )
        }
    )
    def get(self, request):
        profile = get_or_create_profile(request.user)
        challenges = Challenge.objects.filter(profile=profile).order_by('-created_at')
        serializer = ChallengeSerializer(challenges, many=True)
        return Response(serializer.data)
    
    @swagger_auto_schema(
        tags=[SWAGGER_TAGS['COIN_SYSTEM']],
        operation_summary="🎯 Create New Challenge",
        operation_description="Create a new challenge with coin stake. Automatically deducts stake from balance and prevents multiple active challenges.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['challenge_type', 'stake', 'start_date', 'end_date'],
            properties={
                'challenge_type': openapi.Schema(
                    type=openapi.TYPE_STRING,
                    enum=['daily_reflection', 'mood_awareness', 'activity_tracking'],
                    description="Type of challenge to create"
                ),
                'stake': openapi.Schema(type=openapi.TYPE_INTEGER, minimum=1, description="Coin amount to stake"),
                'start_date': openapi.Schema(type=openapi.TYPE_STRING, format='date', description="Challenge start date"),
                'end_date': openapi.Schema(type=openapi.TYPE_STRING, format='date', description="Challenge end date")
            }
        ),
        responses={
            201: openapi.Response(
                description="Challenge created successfully",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'challenge_type': openapi.Schema(type=openapi.TYPE_STRING),
                        'stake': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'start_date': openapi.Schema(type=openapi.TYPE_STRING, format='date'),
                        'end_date': openapi.Schema(type=openapi.TYPE_STRING, format='date'),
                        'completed': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        'settled': openapi.Schema(type=openapi.TYPE_BOOLEAN)
                    }
                )
            ),
            400: openapi.Response(description="Validation errors or active challenge exists"),
            402: openapi.Response(description="Insufficient coin balance")
        }
    )
    def post(self, request):
        profile = get_or_create_profile(request.user)
        
        # Check if user already has an active challenge
        active_challenge = Challenge.objects.filter(
            profile=profile,
            settled=False
        ).first()
        
        if active_challenge:
            return Response(
                {'error': 'You already have an active challenge'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        serializer = ChallengeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            challenge = serializer.save(profile=profile)
            
            # Deduct stake from balance
            profile.coin_balance -= challenge.stake
            profile.save()
            
            # Create transaction record
            CoinTransaction.objects.create(
                profile=profile,
                transaction_type='stake_challenge',
                amount=-challenge.stake,
                balance_after=profile.coin_balance,
                challenge=challenge
            )
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class StreakView(APIView):
    """Get user's current streak information"""
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        tags=[SWAGGER_TAGS['COIN_SYSTEM']],
        operation_summary="🔥 Get User Streak Information",
        operation_description="Retrieve current mood logging streak information and progress towards goals",
        responses={
            200: openapi.Response(
                description="Current streak information and progress",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'streak_count': openapi.Schema(type=openapi.TYPE_INTEGER, description="Current consecutive days streak"),
                        'last_mood_log': openapi.Schema(type=openapi.TYPE_STRING, format='date', description="Date of last mood log"),
                        'streak_progress': openapi.Schema(type=openapi.TYPE_INTEGER, description="Progress towards 30-day goal (0-30)"),
                        'clarity_score': openapi.Schema(type=openapi.TYPE_INTEGER, description="Current clarity score (0-100)")
                    }
                )
            ),
            401: openapi.Response(description="Authentication required")
        }
    )
    def get(self, request):
        profile = get_or_create_profile(request.user)
        
        # Update streak before returning
        profile.update_streak()
        
        return Response({
            'streak_count': profile.streak_count,
            'last_mood_log': profile.last_mood_log,
            'streak_progress': min(profile.streak_count, 30),  # Visual bar 0-30
            'clarity_score': profile.clarity_score
        })

class NudgeView(APIView):
    """Get personalized nudges for the user"""
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        tags=[SWAGGER_TAGS['NUDGE_SYSTEM']],
        operation_summary="🔔 Get Next Personalized Nudge",
        operation_description="Retrieve the next unviewed nudge or generate a new AI-powered contextual nudge based on user behavior",
        responses={
            200: openapi.Response(
                description="Personalized nudge message",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'id': openapi.Schema(type=openapi.TYPE_INTEGER),
                        'nudge_type': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            enum=['mood_trend', 'time_reminder', 'skip_pattern', 'celebration'],
                            description="Type of nudge"
                        ),
                        'message': openapi.Schema(type=openapi.TYPE_STRING, description="AI-generated personalized message"),
                        'tone': openapi.Schema(
                            type=openapi.TYPE_STRING,
                            enum=['gen_z', 'professional', 'friendly'],
                            description="Tone of the nudge message"
                        ),
                        'viewed': openapi.Schema(type=openapi.TYPE_BOOLEAN),
                        'created_at': openapi.Schema(type=openapi.TYPE_STRING, format='datetime')
                    }
                )
            ),
            404: openapi.Response(description="No nudges available")
        }
    )
    def get(self, request):
        profile = get_or_create_profile(request.user)
        
        # Get unviewed nudges first
        nudge = Nudge.objects.filter(
            profile=profile,
            viewed=False
        ).order_by('-created_at').first()
        
        if not nudge:
            # Generate new nudge based on user context
            nudge = self._generate_contextual_nudge(profile)
        
        if nudge:
            serializer = NudgeSerializer(nudge)
            return Response(serializer.data)
        
        return Response({'message': 'No nudges available'}, status=status.HTTP_404_NOT_FOUND)
    
    @swagger_auto_schema(
        tags=[SWAGGER_TAGS['NUDGE_SYSTEM']],
        operation_summary="👁️ Mark Nudge as Viewed",
        operation_description="Mark a specific nudge as viewed to track engagement and prevent re-delivery",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=['nudge_id'],
            properties={
                'nudge_id': openapi.Schema(type=openapi.TYPE_INTEGER, description="ID of the nudge to mark as viewed")
            }
        ),
        responses={
            200: openapi.Response(
                description="Nudge marked as viewed",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'message': openapi.Schema(type=openapi.TYPE_STRING)
                    }
                )
            ),
            400: openapi.Response(description="Missing nudge_id"),
            404: openapi.Response(description="Nudge not found")
        }
    )
    def post(self, request):
        nudge_id = request.data.get('nudge_id')
        if not nudge_id:
            return Response({'error': 'nudge_id required'}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            nudge = Nudge.objects.get(id=nudge_id, profile__user=request.user)
            nudge.viewed = True
            nudge.save()
            return Response({'message': 'Nudge marked as viewed'})
        except Nudge.DoesNotExist:
            return Response({'error': 'Nudge not found'}, status=status.HTTP_404_NOT_FOUND)
    
    def _generate_contextual_nudge(self, profile):
        """Generate time-aware contextual nudge based on user behavior"""
        from datetime import date, timedelta
        
        today = date.today()
        current_time = timezone.now()
        
        # Check if user hasn't logged today
        has_mood_today = Mood.objects.filter(
            user=profile.user,
            created_at__date=today
        ).exists()
        
        if not has_mood_today:
            # Check mood trend
            recent_moods = Mood.objects.filter(
                user=profile.user,
                created_at__date__gte=today - timedelta(days=7)
            ).order_by('-created_at')
            
            # Determine tone based on age
            tone = 'gen_z' if profile.age and profile.age < 30 else 'professional'
            
            # Get time context
            time_context = TimeOfDayContext.get_context(current_time)
            user_name = profile.user.first_name or profile.user.username
            
            # Try AI-based nudge message first
            message = self._generate_ai_nudge_message(profile, recent_moods, tone, time_context)
            
            # If AI fails, use time-aware fallback
            if not message:
                message = TimeOfDayContext.get_contextual_nudge(
                    user_name, 
                    profile.streak_count, 
                    current_time
                )
            
            if recent_moods.exists():
                avg_rating = sum(m.rating for m in recent_moods) / len(recent_moods)
                if avg_rating < 3:
                    nudge_type = 'mood_trend'
                else:
                    nudge_type = 'time_reminder'
            else:
                nudge_type = 'skip_pattern'
            
            # Create nudge
            nudge = Nudge.objects.create(
                profile=profile,
                nudge_type=nudge_type,
                message=message,
                tone=tone
            )
            
            return nudge
        
        return None
    
    def _generate_ai_nudge_message(self, profile, recent_moods, tone, time_context=None):
        """Generate AI-powered time-aware nudge message based on user context"""
        try:
            # Prepare context for AI
            context = {
                'user_age': profile.age,
                'streak_count': profile.streak_count,
                'coin_balance': profile.coin_balance,
                'tone': tone,
                'recent_moods': []
            }
            
            # Add time context if available
            if time_context:
                context['time_context'] = {
                    'period': time_context['period'],
                    'greeting': time_context['greeting'],
                    'tone': time_context['tone'],
                    'energy_level': time_context['energy_level'],
                    'focus': time_context['focus'],
                    'suggested_activities': time_context['activities']
                }
            
            # Add recent mood data
            for mood in recent_moods[:5]:  # Last 5 moods
                context['recent_moods'].append({
                    'mood': mood.mood,
                    'rating': mood.rating,
                    'notes': mood.notes[:100] if mood.notes else None,  # First 100 chars
                    'date': mood.created_at.strftime('%Y-%m-%d')
                })
            
            # Call AI service
            ai_response = self._call_ai_service_for_nudge(context)
            
            if ai_response and 'message' in ai_response:
                return ai_response['message']
            else:
                # Return None to trigger time-aware fallback
                return None
                
        except Exception as e:
            logger.error(f"Error generating AI nudge: {str(e)}")
            # Return None to trigger time-aware fallback
            return None
    
    def _call_ai_service_for_nudge(self, context):
        """Call the AI service to generate a nudge message"""
        try:
            import requests
            
            # AI service endpoint
            ai_service_url = getattr(settings, 'AI_SERVICE_URL', 'http://localhost:5000')
            
            payload = {
                'prompt_type': 'nudge_message',
                'context': context,
                'max_length': 150
            }
            
            response = requests.post(
                f"{ai_service_url}/generate-nudge",
                json=payload,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.warning(f"AI service returned status {response.status_code}")
                return None
                
        except requests.RequestException as e:
            logger.error(f"Error calling AI service: {str(e)}")
            return None
        except Exception as e:
            logger.error(f"Unexpected error in AI service call: {str(e)}")
            return None
    
    def _get_fallback_message(self, tone, streak_count):
        """Fallback message when AI service is unavailable"""
        if tone == 'gen_z':
            messages = [
                "Hey! Quick mood check? 🎯",
                "Your vibes matter - drop a mood log? ✨",
                "Mental health check-in time! 💭"
            ]
        else:
            messages = [
                "Time for your daily mood reflection.",
                "How are you feeling today? Consider logging your mood.",
                "Regular mood tracking supports your emotional wellbeing."
            ]
        
        import random
        return random.choice(messages)

class BehaviorEngineStatsView(APIView):
    """Get comprehensive behavior engine statistics"""
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        tags=[SWAGGER_TAGS['ADMIN_MONITORING']],
        operation_summary="📈 Get Behavior Engine Statistics",
        operation_description="Retrieve comprehensive statistics about coins, streaks, challenges, and nudges for the authenticated user",
        responses={
            200: openapi.Response(
                description="Behavior engine statistics",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'coins': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'balance': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'total_earned': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'total_spent': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'clarity_score': openapi.Schema(type=openapi.TYPE_NUMBER)
                            }
                        ),
                        'streaks': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'current_streak': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'last_mood_log': openapi.Schema(type=openapi.TYPE_STRING, format='date'),
                                'streak_progress': openapi.Schema(type=openapi.TYPE_INTEGER)
                            }
                        ),
                        'challenges': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'total_challenges': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'completed_challenges': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'success_rate': openapi.Schema(type=openapi.TYPE_NUMBER)
                            }
                        ),
                        'nudges': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            properties={
                                'total_nudges': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'viewed_nudges': openapi.Schema(type=openapi.TYPE_INTEGER),
                                'engagement_rate': openapi.Schema(type=openapi.TYPE_NUMBER)
                            }
                        )
                    }
                )
            ),
            401: openapi.Response(description="Authentication required")
        }
    )
    def get(self, request):
        from django.db.models import Sum
        profile = get_or_create_profile(request.user)
        
        # Coin statistics
        total_earned = CoinTransaction.objects.filter(
            profile=profile,
            amount__gt=0
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        total_spent = CoinTransaction.objects.filter(
            profile=profile,
            amount__lt=0
        ).aggregate(total=Sum('amount'))['total'] or 0
        
        # Challenge statistics
        total_challenges = Challenge.objects.filter(profile=profile).count()
        completed_challenges = Challenge.objects.filter(
            profile=profile,
            completed=True
        ).count()
        
        # Nudge statistics
        total_nudges = Nudge.objects.filter(profile=profile).count()
        viewed_nudges = Nudge.objects.filter(
            profile=profile,
            viewed=True
        ).count()
        
        return Response({
            'coins': {
                'balance': profile.coin_balance,
                'total_earned': total_earned,
                'total_spent': abs(total_spent),
                'clarity_score': profile.clarity_score
            },
            'streaks': {
                'current_streak': profile.streak_count,
                'last_mood_log': profile.last_mood_log,
                'streak_progress': min(profile.streak_count, 30)
            },
            'challenges': {
                'total': total_challenges,
                'completed': completed_challenges,
                'success_rate': (completed_challenges / total_challenges * 100) if total_challenges > 0 else 0
            },
            'nudges': {
                'total': total_nudges,
                'viewed': viewed_nudges,
                'engagement_rate': (viewed_nudges / total_nudges * 100) if total_nudges > 0 else 0
            }
        })

class MoodInsightsView(APIView):
    """Get AI-powered mood insights"""
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(
        tags=[SWAGGER_TAGS['AI_INSIGHTS']],
        operation_summary="🧠 Get AI-Powered Mood Insights",
        operation_description="Get personalized AI analysis of mood patterns, trends, and recommendations. Costs 5 coins per analysis.",
        manual_parameters=[
            openapi.Parameter(
                'days',
                openapi.IN_QUERY,
                description="Number of days to analyze (default: 30, max: 365)",
                type=openapi.TYPE_INTEGER
            )
        ],
        responses={
            200: openapi.Response(
                description="AI-generated mood insights and recommendations",
                schema=openapi.Schema(
                    type=openapi.TYPE_OBJECT,
                    properties={
                        'insights': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING),
                            description="AI-generated insights about mood patterns"
                        ),
                        'recommendations': openapi.Schema(
                            type=openapi.TYPE_ARRAY,
                            items=openapi.Schema(type=openapi.TYPE_STRING),
                            description="Personalized recommendations for improvement"
                        ),
                        'mood_trends': openapi.Schema(
                            type=openapi.TYPE_OBJECT,
                            description="Statistical analysis of mood trends"
                        ),
                        'cost_coins': openapi.Schema(type=openapi.TYPE_INTEGER, description="Coins spent for this analysis"),
                        'remaining_balance': openapi.Schema(type=openapi.TYPE_INTEGER, description="User's remaining coin balance")
                    }
                )
            ),
            402: openapi.Response(description="Insufficient coins"),
            404: openapi.Response(description="Not enough mood data"),
            503: openapi.Response(description="AI service unavailable")
        }
    )
    def get(self, request):
        days = int(request.query_params.get('days', 30))
        cost_coins = 5  # Cost for deep insights
        
        profile = get_or_create_profile(request.user)
        
        # Check if user has enough coins
        if profile.coin_balance < cost_coins:
            return Response({
                'error': 'Insufficient coins for deep insights',
                'required_coins': cost_coins,
                'current_balance': profile.coin_balance
            }, status=status.HTTP_402_PAYMENT_REQUIRED)
        
        # Get mood data
        from datetime import date, timedelta
        start_date = date.today() - timedelta(days=days)
        
        moods = Mood.objects.filter(
            user=request.user,
            created_at__date__gte=start_date
        ).order_by('-created_at')
        
        if not moods.exists():
            return Response({
                'error': 'Not enough mood data for insights',
                'message': 'Log more moods to get personalized insights'
            }, status=status.HTTP_404_NOT_FOUND)
        
        # Generate AI insights
        insights_data = self._generate_ai_insights(profile, moods, days)
        
        if insights_data:
            # Deduct coins for the service
            profile.coin_balance -= cost_coins
            profile.save()
            
            # Create transaction record
            CoinTransaction.objects.create(
                profile=profile,
                transaction_type='spend_insight',
                amount=-cost_coins,
                balance_after=profile.coin_balance
            )
            
            insights_data['cost_coins'] = cost_coins
            insights_data['remaining_balance'] = profile.coin_balance
            
            return Response(insights_data)
        else:
            return Response({
                'error': 'Failed to generate insights',
                'message': 'AI service temporarily unavailable'
            }, status=status.HTTP_503_SERVICE_UNAVAILABLE)
    
    def _generate_ai_insights(self, profile, moods, days):
        """Generate AI-powered mood insights"""
        try:
            import requests
            
            # Prepare mood data for AI
            mood_data = []
            for mood in moods:
                mood_data.append({
                    'date': mood.created_at.strftime('%Y-%m-%d'),
                    'mood': mood.mood,
                    'rating': mood.rating,
                    'notes': mood.notes[:200] if mood.notes else None,
                    'activities': mood.activities
                })
            
            # Calculate basic statistics
            ratings = [m.rating for m in moods]
            avg_rating = sum(ratings) / len(ratings)
            
            context = {
                'user_age': profile.age,
                'analysis_period': days,
                'mood_data': mood_data,
                'avg_rating': avg_rating,
                'total_entries': len(mood_data),
                'streak_count': profile.streak_count,
                'tone': 'gen_z' if profile.age and profile.age < 30 else 'professional'
            }
            
            # Call AI service
            ai_service_url = getattr(settings, 'AI_SERVICE_URL', 'http://localhost:5000')
            
            payload = {
                'prompt_type': 'mood_insights',
                'context': context
            }
            
            response = requests.post(
                f"{ai_service_url}/generate-insights",
                json=payload,
                timeout=15
            )
            
            if response.status_code == 200:
                return response.json()
            else:
                logger.warning(f"AI service returned status {response.status_code}")
                return None
                
        except Exception as e:
            logger.error(f"Error generating AI insights: {str(e)}")
            return None
