"""
Middleware to bypass authentication for Swagger/ReDoc documentation endpoints
"""

class SwaggerAuthBypassMiddleware:
    """
    Middleware that bypasses authentication for API documentation endpoints
    """
    
    def __init__(self, get_response):
        self.get_response = get_response
        # Define patterns for endpoints that should be public
        self.public_paths = [
            '/swagger/',
            '/redoc/',
            '/swagger.json',
            '/swagger.yaml',
        ]
    
    def __call__(self, request):
        # Check if this is a documentation endpoint
        for path in self.public_paths:
            if request.path.startswith(path):
                # Remove authentication requirements for these paths
                request.user = None
                # Add a flag to indicate this is a public endpoint
                request._swagger_public = True
                break
                
        response = self.get_response(request)
        return response
