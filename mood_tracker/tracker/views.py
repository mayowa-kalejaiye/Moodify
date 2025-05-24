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

from .models import Mood, Comment
from .serializers import (
    MoodSerializer, 
    # MoodCommentSerializer, # Commented out as it's legacy
    UserSerializer, 
    UserRegisterSerializer,
    PasswordChangeSerializer,
    CommentSerializer
)

class CustomTokenObtainPairView(TokenObtainPairView):
    """
    Enhanced JWT token endpoint that returns user information along with tokens
    """
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
    
    def get(self, request):
        """API root endpoint with comprehensive documentation"""
        api_info = {
            'name': 'Mood Tracker API',
            'version': '1.0.0',
            'description': 'Track your moods and analyze sentiment patterns over time.',
            'endpoints': {
                'authentication': {
                    'login': {'url': '/api/login/', 'method': 'POST', 'description': 'Login to get authentication token'},
                    'logout': {'url': '/api/logout/', 'method': 'POST', 'description': 'Invalidate current token'},
                    'register': {'url': '/api/register/', 'method': 'POST', 'description': 'Create a new user account'},
                    'password_change': {'url': '/api/password-change/', 'method': 'POST', 'description': 'Change user password'}
                },
                'users': {
                    'profile': {'url': '/api/profile/', 'method': 'GET/PUT', 'description': 'View or update user profile'}
                },
                'moods': {
                    'create': {'url': '/api/moods/', 'method': 'POST', 'description': 'Log a new mood entry'},
                    'options': {'url': '/api/moods/', 'method': 'GET', 'description': 'Get available mood options'},
                    'history': {'url': '/api/moods/history/', 'method': 'GET', 'description': 'Get user\'s mood history'},
                    'summary': {'url': '/api/moods/summary/', 'method': 'GET', 'description': 'Get summary statistics of user\'s moods'},
                    'detail': {'url': '/api/moods/{mood_id}/', 'method': 'GET/PUT/DELETE', 'description': 'Get, update or delete a specific mood entry'},
                    'trends': {'url': '/api/moods/trends/', 'method': 'GET', 'description': 'Get mood trends over time'}
                },
                'comments': {
                    'list_create': {'url': '/api/moods/{mood_id}/comments/', 'method': 'GET/POST', 'description': 'List or create comments for a mood entry'},
                    'detail': {'url': '/api/moods/{mood_id}/comments/{comment_id}/', 'method': 'GET/PUT/DELETE', 'description': 'Retrieve, update, or delete a specific comment'}
                },
                'ai_suggestions': {
                    'motivation': {'url': '/api/suggestions/motivation/', 'method': 'GET', 'description': 'Get personalized motivational messages based on recent mood trends.'},
                    'habits': {'url': '/api/suggestions/habits/', 'method': 'GET', 'description': 'Get habit improvement suggestions based on mood-activity correlations.'},
                    'patterns': {'url': '/api/moods/analysis/patterns/', 'method': 'GET', 'description': 'Analyze mood patterns by time of day and day of week.'}
                },
                'exports': {
                    'json': {'url': '/api/moods/export/json/', 'method': 'GET', 'description': 'Export moods in JSON format'},
                    'csv': {'url': '/api/moods/export/csv/', 'method': 'GET', 'description': 'Export moods in CSV format'}
                },
                'admin': {
                    'sentiment_analysis': {'url': '/api/sentiment-analysis/', 'method': 'GET', 'description': 'Analyze sentiment across all users (admin only)'}
                },
                'documentation': {
                    'swagger': {'url': '/swagger/', 'method': 'GET', 'description': 'API documentation with Swagger UI'},
                    'redoc': {'url': '/redoc/', 'method': 'GET', 'description': 'API documentation with ReDoc UI'}
                }
            },
            'status': 'online'
        }
        return Response(api_info, status=status.HTTP_200_OK)

class UserRegisterAPIView(APIView):
    permission_classes = [AllowAny]
    
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
    
    def get(self, request):
        """Get user profile"""
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request):
        """Update user profile"""
        serializer = UserSerializer(request.user, data=request.data, partial=True)
        if serializer.is_valid():
            # Don't allow username changes through this endpoint
            if 'username' in serializer.validated_data:
                return Response(
                    {'error': 'Username cannot be changed through this endpoint'}, 
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PasswordChangeAPIView(APIView):
    """Change user password"""
    permission_classes = [IsAuthenticated]
    
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

    def get(self, request):
        """Get user's mood options (for potential UI elements)"""
        # You could return preset mood options or common moods
        return Response({
            'mood_options': ['Happy', 'Sad', 'Anxious', 'Excited', 'Tired', 'Content', 'Angry']
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
    
    def get(self, request):
        """Export user's moods as JSON"""
        moods = Mood.objects.filter(user=request.user)
        serializer = MoodSerializer(moods, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class ExportMoodCsvAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
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
    
    def get(self, request, mood_id):
        """Get a specific mood entry"""
        mood = self.get_mood(mood_id, request.user)
        if not mood:
            return Response({'error': 'Mood not found or you do not have permission'}, 
                            status=status.HTTP_404_NOT_FOUND)
        
        serializer = MoodSerializer(mood)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
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
                mood_entry.sentiment = sentiment.polarity
                mood_entry.save()
            
            return Response(MoodSerializer(mood_entry).data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
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
    """API view to get AI-generated motivational content"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        recent_moods = Mood.objects.filter(
            user=request.user
        ).order_by('-created_at')[:5]
        
        if not recent_moods:
            return Response(
                {"message": "You need to log some moods first"},
                status=status.HTTP_200_OK
            )
        
        # Aggregate recent mood data for context
        avg_rating = recent_moods.aggregate(avg=Avg('rating'))['avg'] or 3
        mood_trend = "positive" if avg_rating > 3.5 else "negative" if avg_rating < 2.5 else "neutral"
        
        try:
            # Free AI-like suggestion system using pattern matching and templates
            
            # Gather context from user's data for personalization
            user_name = request.user.first_name or request.user.username
            time_of_day = "morning" if 5 <= datetime.now().hour < 12 else "afternoon" if 12 <= datetime.now().hour < 18 else "evening"
            
            # Get recent mood text for pattern matching
            recent_mood_texts = [mood.mood.lower() for mood in recent_moods if mood.mood]
            recent_notes = [mood.notes for mood in recent_moods if mood.notes]
            
            # Check for specific patterns in mood data
            has_anxiety = any('anxious' in text or 'anxiety' in text for text in recent_mood_texts)
            has_stress = any('stress' in note.lower() if note else False for note in recent_notes)
            has_positive = any(text in ['happy', 'excited', 'content'] for text in recent_mood_texts)
            
            # Create personalized templates based on context
            motivation_templates = {
                "positive": [
                    f"Good {time_of_day}, {user_name}! Keep up the great mindset! Your positive outlook is shaping your reality.",
                    f"You're doing fantastic, {user_name}! Remember to celebrate these good moments.",
                    "Your positive energy is contagious. Continue spreading joy!",
                    "Wonderful progress! Keep nurturing the habits that bring you joy.",
                ],
                "neutral": [
                    f"{user_name}, balance is key. Take time today to do something that brings you joy.",
                    "Steady as you go. Small positive actions can shift your momentum.",
                    f"You're in a stable place, {user_name} - a good time to set new goals!",
                    "Remember that consistency matters more than intensity. Keep going!"
                ],
                "negative": [
                    f"{user_name}, difficult days are just that - days. Not your whole life. Tomorrow is a fresh start.",
                    "Take a moment for self-care today. Even small acts of kindness to yourself matter.",
                    "Remember that it's okay not to be okay sometimes. Reach out if you need support.",
                    "One step at a time. Focus on just the next small positive action."
                ]
            }
            
            # Add specialized messages based on specific patterns
            if has_anxiety:
                motivation_templates["negative"].append("Try this quick exercise: breathe in for 4 counts, hold for 4, out for 6. Repeat 5 times to calm anxiety.")
                motivation_templates["neutral"].append("When anxious thoughts arise, notice them without judgment. Name them, then let them float by.")
            
            if has_stress:
                motivation_templates["negative"].append("For stress relief: identify one thing you can control and take action on it, let go of what you can't control.")
                motivation_templates["neutral"].append("Consider a 10-minute break to reset: step outside, stretch, or enjoy a cup of tea mindfully.")
            
            # Additional specialized patterns
            has_sadness = any(text in ['sad', 'depressed', 'down', 'unhappy'] for text in recent_mood_texts)
            has_anger = any(text in ['angry', 'frustrated', 'annoyed', 'mad'] for text in recent_mood_texts)
            has_fatigue = any(text in ['tired', 'exhausted', 'fatigued'] for text in recent_mood_texts)
            
            if has_sadness:
                motivation_templates["negative"].append(f"{user_name}, sadness is often telling us something important. What might your sadness be asking for? Perhaps connection or self-compassion.")
                motivation_templates["neutral"].append("Try the 'opposite action' technique: when feeling down, do something that normally brings you joy, even if you don't feel like it.")
            
            if has_anger:
                motivation_templates["negative"].append("When anger arises, try the 5-5-5 method: name 5 things you see, 5 things you hear, and 5 body sensations. This can help diffuse intense emotions.")
                motivation_templates["neutral"].append("Anger often masks other emotions like hurt or fear. Can you ask yourself what might be beneath the anger?")
            
            if has_fatigue:
                motivation_templates["negative"].append("Energy management beats time management. Try working in focused 25-minute blocks followed by 5-minute breaks.")
                motivation_templates["neutral"].append("Consider if you need more rest rather than more motivation. Sometimes the most productive thing is to recharge.")
            
            if has_positive and mood_trend == "negative":
                motivation_templates["negative"].append("You've felt happy recently - remember what brought you joy then and see if you can incorporate it today.")
            
            # Select a message based on current ratings and with some randomness
            import random
            
            # Occasionally add variety by selecting from a different category
            variety_dice = random.random()
            if variety_dice > 0.85:  # 15% chance to pick from neutral instead of actual mood
                motivation = random.choice(motivation_templates["neutral"])
            else:
                motivation = random.choice(motivation_templates[mood_trend])
            
            # Add a personalized closing line
            closing_lines = [
                f"Wishing you a wonderful {time_of_day}, {user_name}!",
                "You've got this!",
                "One day at a time.",
                "Small steps lead to big changes.",
                "You're stronger than you know."
            ]
            
            full_message = f"{motivation} {random.choice(closing_lines)}"
            
            return Response({
                "motivation": full_message,
                "mood_trend": mood_trend,
                "personalized": True
            })
            
        except Exception as e:
            return Response(
                {"error": "Could not generate motivation", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

class HabitImprovementAPIView(APIView):
    """API view to get AI-generated habit improvement suggestions"""
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        # Get moods from the last two weeks
        two_weeks_ago = timezone.now() - timedelta(days=14)
        recent_moods = Mood.objects.filter(
            user=request.user,
            created_at__gte=two_weeks_ago
        ).order_by('-created_at')
        
        if recent_moods.count() < 3:
            return Response(
                {"message": "Need more mood data to provide meaningful habit suggestions"},
                status=status.HTTP_200_OK
            )
            
        # Extract patterns based on notes and activities
        low_mood_activities = recent_moods.filter(rating__lt=3).values('activities').annotate(
            count=Count('id')).order_by('-count')[:3]
            
        high_mood_activities = recent_moods.filter(rating__gt=3).values('activities').annotate(
            count=Count('id')).order_by('-count')[:3]
        
        # Generate simple suggestions
        suggestions = []
        
        if low_mood_activities:
            for activity in low_mood_activities:
                if activity['activities']:
                    suggestions.append(f"Consider reducing '{activity['activities']}' which appears linked to lower moods")
        
        if high_mood_activities:
            for activity in high_mood_activities:
                if activity['activities']:
                    suggestions.append(f"Try to increase '{activity['activities']}' which appears linked to better moods")
        
        if not suggestions:
            suggestions = [
                "Try to maintain a consistent sleep schedule",
                "Consider adding short walks to your daily routine",
                "Practice mindfulness for 5 minutes each day",
                "Limit screen time before bed for better sleep quality"
            ]
        
        return Response({
            "habit_suggestions": suggestions,
            "message": "Small consistent changes can significantly impact your mood over time."
        })

class MoodPatternAnalysisAPIView(APIView):
    """API view to analyze mood patterns and provide insights"""
    permission_classes = [IsAuthenticated]
    
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
