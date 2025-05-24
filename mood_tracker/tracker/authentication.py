from rest_framework_simplejwt.authentication import JWTAuthentication
from django.conf import settings
from rest_framework import exceptions

class CustomJWTAuthentication(JWTAuthentication):
    """
    Custom JWT Authentication that adds extra validation and security features
    """
    
    def authenticate(self, request):
        # Call the parent authenticate method
        authenticated = super().authenticate(request)
        
        if authenticated:
            user, token = authenticated
            
            # Add additional validation if needed
            if not user.is_active:
                raise exceptions.AuthenticationFailed('User account is disabled')
                
            return user, token
        
        return None
