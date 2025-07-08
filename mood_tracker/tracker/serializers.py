from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Mood, Comment, Profile, AISuggestionFeedback, Challenge, CoinTransaction, Nudge
import bleach # Added for sanitization

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['age', 'coin_balance', 'clarity_score', 'streak_count', 'last_mood_log']
        read_only_fields = ['coin_balance', 'clarity_score', 'streak_count', 'last_mood_log']

class ChallengeSerializer(serializers.ModelSerializer):
    days_remaining = serializers.ReadOnlyField()
    is_active = serializers.ReadOnlyField()
    
    class Meta:
        model = Challenge
        fields = ['id', 'challenge_type', 'stake', 'start_date', 'end_date', 
                 'completed', 'settled', 'is_active', 'days_remaining', 'created_at']
        read_only_fields = ['completed', 'settled', 'created_at']
    
    def validate_stake(self, value):
        """Ensure stake is within allowed range"""
        if value < 10 or value > 50:
            raise serializers.ValidationError("Stake must be between 10 and 50 coins")
        return value
    
    def validate(self, data):
        """Validate challenge creation"""
        request = self.context.get('request')
        if request and request.user:
            profile = getattr(request.user, 'profile', None)
            if profile:
                # Check if user can stake coins (age >= 18)
                if not profile.can_stake_coins():
                    raise serializers.ValidationError("Users under 18 cannot participate in staking challenges")
                
                # Check if user has enough coins
                if profile.coin_balance < data.get('stake', 0):
                    raise serializers.ValidationError("Insufficient coin balance for this stake")
        
        return data

class CoinTransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CoinTransaction
        fields = ['id', 'transaction_type', 'amount', 'balance_after', 'created_at']
        read_only_fields = ['id', 'transaction_type', 'amount', 'balance_after', 'created_at']

class NudgeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nudge
        fields = ['id', 'nudge_type', 'message', 'tone', 'viewed', 'created_at']
        read_only_fields = ['id', 'nudge_type', 'message', 'tone', 'created_at']

class UserSerializer(serializers.ModelSerializer):
    profile = ProfileSerializer(required=False)
    age = serializers.IntegerField(required=False, write_only=True, help_text="Age (will be saved to profile)")
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'profile', 'age']

    def update(self, instance, validated_data):
        # Handle both nested profile data and flat age field
        profile_data = validated_data.pop('profile', {})
        flat_age = validated_data.pop('age', None)
        
        # If age is provided at top level, add it to profile_data
        if flat_age is not None:
            profile_data['age'] = flat_age
        
        user = super().update(instance, validated_data)
        
        # Update or create profile if there's profile data
        if profile_data:
            Profile.objects.update_or_create(user=user, defaults=profile_data)
        
        return user

class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'})
    password_confirm = serializers.CharField(write_only=True, style={'input_type': 'password'})
    profile = ProfileSerializer(required=False)  # Allow age at registration
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password', 'password_confirm', 'first_name', 'last_name', 'profile']
    
    def validate(self, data):
        # Check if passwords match
        if data['password'] != data['password_confirm']:
            raise serializers.ValidationError({"password_confirm": "Passwords don't match"})
        
        # Check if username already exists
        if User.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({"username": "This username is already in use"})
        
        # Check if email already exists and is provided
        email = data.get('email')
        if email and User.objects.filter(email=email).exists():
            raise serializers.ValidationError({"email": "This email is already registered"})
        
        # Check password strength
        if len(data['password']) < 8:
            raise serializers.ValidationError({"password": "Password must be at least 8 characters long"})
            
        return data
    
    def create(self, validated_data):
        profile_data = validated_data.pop('profile', None)
        validated_data.pop('password_confirm')  # Remove password_confirm field
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        if profile_data:
            Profile.objects.update_or_create(user=user, defaults=profile_data)
        return user

class PasswordChangeSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    new_password_confirm = serializers.CharField(required=True, write_only=True)

    def validate(self, data):
        if data['new_password'] != data['new_password_confirm']:
            raise serializers.ValidationError({"new_password_confirm": "Passwords don't match"})
        
        if len(data['new_password']) < 8:
            raise serializers.ValidationError({"new_password": "Password must be at least 8 characters long"})
        
        return data

# Add a simple LoginSerializer for Swagger documentation
class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)
    # Make class non-abstract for openapi.Schema
    class Meta:
        pass # Required for openapi.Schema to work if no model is associated

# class MoodCommentSerializer(serializers.ModelSerializer):
#     """
#     LEGACY SERIALIZER: This serializer is for the MoodComment model, which is considered legacy.
#     Please use the CommentSerializer for new development.
#     This will be removed in a future version.
#     """
#     class Meta:
#         model = MoodComment
#         fields = ['id', 'content', 'created_at', 'updated_at']
#         read_only_fields = ['created_at', 'updated_at']

#     def validate_content(self, value):
#         """
#         Validate comment content - implement sanitization
#         """
#         if not value:
#             raise serializers.ValidationError("Comment cannot be empty.")
        
#         if len(value) > 500:
#             raise serializers.ValidationError("Comment too long (max 500 characters)")
        
#         # Simple sanitization (a more robust solution would use bleach or similar)
#         # value = value.replace('<', '&lt;').replace('>', '&gt;')
#         value = bleach.clean(value, tags=[], strip=True) # Using bleach
        
#         return value

# Define CommentSerializer first to avoid circular imports
class CommentSerializer(serializers.ModelSerializer):
    """Serializer for the Comment model"""
    username = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = Comment
        fields = ['id', 'content', 'username', 'created_at', 'updated_at']
        read_only_fields = ['id', 'username', 'created_at', 'updated_at']
        
    def validate_content(self, value):
        """
        Validate and sanitize comment content.
        """
        if not value:
            raise serializers.ValidationError("Comment content cannot be empty.")
        if len(value) > 1000: # Max length for comments
            raise serializers.ValidationError("Comment content is too long (max 1000 characters).")
        # Sanitize HTML content
        return bleach.clean(value, tags=[], strip=True)

    def create(self, validated_data):
        """Create and return a new comment"""
        validated_data['user'] = self.context['request'].user
        validated_data['mood_id'] = self.context.get('mood_id')
        return Comment.objects.create(**validated_data)

# Now define MoodSerializer which uses CommentSerializer
class MoodSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    username = serializers.ReadOnlyField(source='user.username')
    
    class Meta:
        model = Mood
        fields = ['id', 'mood', 'notes', 'sentiment', 'activities', 'rating', 'created_at', 'username', 'comments']
        read_only_fields = ['id', 'sentiment', 'created_at', 'username']

    def validate_mood(self, value):
        """
        Validate the mood field - ensure it's a known mood type or at least reasonable
        """
        if not value:
            raise serializers.ValidationError("Mood cannot be empty.")
        
        if len(value) > 50:
            raise serializers.ValidationError("Mood description too long.")
        
        # Add predefined mood list for better categorization
        common_moods = ['happy', 'sad', 'angry', 'excited', 'anxious', 'calm', 
                       'frustrated', 'content', 'tired', 'energetic', 'bored', 
                       'stressed', 'relaxed', 'motivated', 'productive']
                       
        # Suggest standardization for common moods
        if value.lower() not in common_moods:
            # Not raising an error, just a recommendation that could be logged or noted
            pass
            
        return value.capitalize()  # Standardize mood capitalization

    def validate_notes(self, value):
        """
        Validate notes - implement sanitization
        """
        if value and len(value) > 1000:
            raise serializers.ValidationError("Notes too long (max 1000 characters)")
        
        # Sanitize HTML content if notes are provided
        if value:
            value = bleach.clean(value, tags=[], strip=True)
        
        return value

class AISuggestionFeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = AISuggestionFeedback
        fields = ['id', 'suggestion_type', 'suggestion_text', 'rating', 'created_at']
