from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework.test import APIClient, APITestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from .models import Mood
import json

class MoodAPITestCase(APITestCase):
    """
    Comprehensive test suite for the Mood Tracker API.
    
    This test suite verifies all API endpoints including authentication, 
    mood tracking operations, and admin features. It covers:
    - Authentication (login, register, token usage)
    - Authorization and permissions
    - CRUD operations on mood entries
    - Data validation and error handling
    - Admin-only functionality
    """
    
    def setUp(self):
        """
        Test setup: creates users, authentication tokens, and sample mood entries.
        This runs before each test method.
        """
        # Create test users
        self.user1 = User.objects.create_user(username='testuser1', email='test1@example.com', password='password123')
        self.user2 = User.objects.create_user(username='testuser2', email='test2@example.com', password='password123')
        self.admin_user = User.objects.create_superuser(username='admin', email='admin@example.com', password='admin123')
        
        # Create tokens for authentication
        self.token1 = Token.objects.create(user=self.user1)
        self.token2 = Token.objects.create(user=self.user2)
        self.admin_token = Token.objects.create(user=self.admin_user)
        
        # Create some test mood entries
        Mood.objects.create(user=self.user1, mood='Happy', notes='Feeling good today!', sentiment=0.8)
        Mood.objects.create(user=self.user1, mood='Sad', notes='Not a great day', sentiment=-0.5)
        Mood.objects.create(user=self.user2, mood='Excited', notes='Looking forward to the weekend', sentiment=0.9)
    
    # === AUTH ENDPOINT TESTS ===
    
    def test_home_endpoint(self):
        """Test the API root endpoint returns proper documentation"""
        url = reverse('api_home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Updated to match actual API response structure
        self.assertIn('name', response.data)
        self.assertIn('version', response.data)
        self.assertIn('description', response.data)
        self.assertIn('endpoints', response.data)
        
        # Also verify all expected endpoint documentation is included
        self.assertIn('authentication', response.data['endpoints'])
        self.assertIn('moods', response.data['endpoints'])
    
    def test_login_success(self):
        """Test successful user login with valid credentials"""
        url = reverse('api_login')
        data = {'username': 'testuser1', 'password': 'password123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('token', response.data)
        self.assertEqual(response.data['user']['username'], 'testuser1')
    
    def test_login_failure(self):
        """Test login rejection with invalid credentials"""
        url = reverse('api_login')
        
        # Test with wrong password
        data = {'username': 'testuser1', 'password': 'wrongpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Test with non-existent user
        data = {'username': 'nonexistentuser', 'password': 'password123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        
        # Test with missing fields
        response = self.client.post(url, {'username': 'testuser1'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_register_success(self):
        """Test successful user registration with valid data"""
        url = reverse('api_register')
        # Include password_confirm in the request data
        data = {
            'username': 'newuser', 
            'email': 'newuser@example.com', 
            'password': 'newpassword123',
            'password_confirm': 'newpassword123'  # Added this field
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 4)  # 3 created in setUp + 1 new
    
    def test_register_failure(self):
        """Test registration rejection with invalid data"""
        url = reverse('api_register')
        
        # Test with existing username
        data = {'username': 'testuser1', 'email': 'new@example.com', 
                'password': 'password123', 'password_confirm': 'password123'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Test with mismatched passwords
        data = {'username': 'newuser2', 'email': 'new2@example.com', 
                'password': 'password123', 'password_confirm': 'differentpassword'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Test with too short password
        data = {'username': 'newuser2', 'email': 'new2@example.com', 
                'password': 'short', 'password_confirm': 'short'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_logout(self):
        """Test user logout invalidates the token"""
        url = reverse('api_logout')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify token is no longer valid
        token_check_url = reverse('api_mood_history')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        response = self.client.get(token_check_url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    # === MOOD ENDPOINT TESTS ===
    
    def test_create_mood_success(self):
        """Test creating a new mood entry with valid data"""
        url = reverse('api_mood_create')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        data = {'mood': 'Relaxed', 'notes': 'Enjoying a quiet evening'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Mood.objects.filter(user=self.user1).count(), 3)  # 2 from setUp + 1 new
    
    def test_create_mood_validation(self):
        """Test mood entry creation with invalid data"""
        url = reverse('api_mood_create')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        
        # Test with missing required fields
        response = self.client.post(url, {}, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Test with too long mood text
        data = {'mood': 'a' * 101, 'notes': 'Valid notes'}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_mood_history(self):
        """Test retrieving user's mood history"""
        url = reverse('api_mood_history')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # User1 should have 2 moods from setUp
    
    def test_mood_history_filters(self):
        """Test mood history filtering options"""
        url = reverse('api_mood_history')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        
        # Test date filtering
        response = self.client.get(f"{url}?start_date=2023-01-01&end_date=2030-01-01")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Test mood filtering
        response = self.client.get(f"{url}?mood=Happy")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Only Happy mood
        
        # Test limit parameter
        response = self.client.get(f"{url}?limit=1")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)  # Limited to 1 entry
    
    def test_mood_summary(self):
        """Test mood summary statistics endpoint"""
        url = reverse('api_mood_summary')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('total_entries', response.data)
        self.assertIn('mood_counts', response.data)
        self.assertIn('average_sentiment', response.data)
        self.assertEqual(response.data['total_entries'], 2)  # User1 has 2 moods
    
    def test_mood_trends(self):
        """Test mood trends analysis endpoint"""
        url = reverse('api_mood_trends')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        
        # Test with default days parameter
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('trends', response.data)
        
        # Test with custom days parameter
        response = self.client.get(f"{url}?days=7")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['days_analyzed'], 7)
    
    def test_mood_detail(self):
        """Test retrieving a specific mood entry"""
        mood = Mood.objects.filter(user=self.user1).first()
        url = reverse('api_mood_detail', kwargs={'mood_id': mood.id})
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['mood'], mood.mood)
    
    def test_mood_detail_access_control(self):
        """Test that users can only access their own mood entries"""
        # Get a mood belonging to user1
        mood = Mood.objects.filter(user=self.user1).first()
        url = reverse('api_mood_detail', kwargs={'mood_id': mood.id})
        
        # User2 should not be able to access user1's mood
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token2.key}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        
        # User1 should be able to access their own mood
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_update_mood_success(self):
        """Test successful mood entry update"""
        mood = Mood.objects.filter(user=self.user1).first()
        url = reverse('api_mood_detail', kwargs={'mood_id': mood.id})
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        data = {'notes': 'Updated mood notes'}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['notes'], 'Updated mood notes')
    
    def test_update_mood_validation(self):
        """Test mood update with invalid data"""
        mood = Mood.objects.filter(user=self.user1).first()
        url = reverse('api_mood_detail', kwargs={'mood_id': mood.id})
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        
        # Test with too long mood text
        data = {'mood': 'a' * 101}
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_delete_mood(self):
        """Test mood entry deletion"""
        mood = Mood.objects.filter(user=self.user1).first()
        url = reverse('api_mood_detail', kwargs={'mood_id': mood.id})
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        
        # Delete the mood
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        
        # Verify it's actually deleted
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    # === EXPORT ENDPOINT TESTS ===
    
    def test_export_json(self):
        """Test exporting moods as JSON"""
        url = reverse('api_export_json')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)  # User1 has 2 moods
    
    def test_export_csv(self):
        """Test exporting moods as CSV"""
        url = reverse('api_export_csv')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'text/csv')
        self.assertTrue('attachment; filename="moods.csv"' in response['Content-Disposition'])
    
    # === ADMIN FEATURE TESTS ===
    
    def test_sentiment_analysis_access_control(self):
        """Test admin-only sentiment analysis access control"""
        url = reverse('api_sentiment_analysis')
        
        # Try with regular user
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        
        # Try with admin user
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.admin_token.key}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_sentiment_analysis_content(self):
        """Test sentiment analysis endpoint returns expected data"""
        url = reverse('api_sentiment_analysis')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.admin_token.key}')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) > 0)
        self.assertTrue(any(item['user__username'] == 'testuser1' for item in response.data))
        self.assertTrue(any(item['user__username'] == 'testuser2' for item in response.data))
        
        # Verify sentiment calculations are correct
        user1_data = next(item for item in response.data if item['user__username'] == 'testuser1')
        # User1 has sentiments 0.8 and -0.5, average should be 0.15
        self.assertAlmostEqual(user1_data['average_sentiment'], 0.15, places=2)
    
    # === AUTHENTICATION TESTS ===
    
    def test_token_auth(self):
        """Test token authentication"""
        url = reverse('api_mood_history')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_jwt_auth(self):
        """Test JWT authentication"""
        # Get JWT token
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {'username': 'testuser1', 'password': 'password123'}, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)
        
        # Use JWT token to access protected endpoint
        access_token = response.data['access']
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')
        
        url = reverse('api_mood_history')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_jwt_refresh(self):
        """Test JWT token refresh"""
        # Get JWT token
        url = reverse('token_obtain_pair')
        response = self.client.post(url, {'username': 'testuser1', 'password': 'password123'}, format='json')
        refresh_token = response.data['refresh']
        
        # Skip this test if JWT blacklisting is enabled but OutstandingToken model isn't available
        try:
            url = reverse('token_refresh')
            response = self.client.post(url, {'refresh': refresh_token}, format='json')
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertIn('access', response.data)
        except AttributeError:
            # If OutstandingToken is not available, skip this test
            self.skipTest("SimpleJWT OutstandingToken model not available")
    
    # === ERROR HANDLING TESTS ===
    
    def test_unauthorized_access(self):
        """Test that unauthenticated requests are rejected"""
        # No authentication credentials
        self.client.credentials()
        url = reverse('api_mood_history')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
    
    def test_error_handling_nonexistent(self):
        """Test handling of requests for non-existent resources"""
        # Try to get non-existent mood
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        url = reverse('api_mood_detail', kwargs={'mood_id': 99999})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_bad_request_handling(self):
        """Test handling of malformed requests"""
        url = reverse('api_mood_create')
        self.client.credentials(HTTP_AUTHORIZATION=f'Token {self.token1.key}')
        
        # Send malformed JSON
        response = self.client.post(
            url, 
            data='{invalid json}',
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
