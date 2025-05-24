import json
import time
import logging
from django.http import JsonResponse

logger = logging.getLogger(__name__)

class APIDebugMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Skip non-API paths
        if not request.path.startswith('/api/'):
            return self.get_response(request)
        
        # Log request details
        start_time = time.time()
        
        # Process the request
        response = self.get_response(request)
        
        # Calculate duration
        duration = time.time() - start_time
        
        # Log details for debugging
        log_data = {
            'path': request.path,
            'method': request.method,
            'status_code': response.status_code,
            'duration': f"{duration:.2f}s",
        }
        
        # Add authentication debug info (safely)
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if auth_header:
            if auth_header.startswith('Token '):
                log_data['auth'] = 'Token authentication attempt'
            elif auth_header.startswith('Bearer '):
                log_data['auth'] = 'JWT authentication attempt'
            else:
                log_data['auth'] = 'Unknown authentication format'
        else:
            log_data['auth'] = 'No authentication provided'
            
        # Log the data
        logger.debug(f"API Request: {json.dumps(log_data)}")
        
        # For 401s, add helpful info to the response
        if response.status_code == 401:
            try:
                response_data = json.loads(response.content.decode('utf-8'))
                
                if 'detail' in response_data and response_data['detail'] == 'Authentication credentials were not provided.':
                    response_data['help'] = "Ensure you're including the token correctly in the Authorization header: 'Authorization: Token YOUR_TOKEN_HERE' or 'Authorization: Bearer YOUR_JWT_HERE'"
                    
                    from django.http import JsonResponse
                    return JsonResponse(response_data, status=401)
            except:
                # If we can't modify the response, just return it as is
                pass
                
        return response
