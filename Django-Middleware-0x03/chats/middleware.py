# Django-Middleware-0x03/chats/middleware.py
import logging
from datetime import datetime
from pathlib import Path
from django.http import HttpResponseForbidden

# Define the absolute path for the log file in the project root
project_root = Path(__file__).resolve().parent.parent  # Go up to project root from chats
log_file = project_root / 'requests.log'

# Configure a basic logger
logger = logging.getLogger('request_logger')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(log_file)  # Use absolute path
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

class RequestLoggingMiddleware:
    """Middleware to log user requests with timestamp, user, and path."""
    
    def __init__(self, get_response):
        """Initialize the middleware with the get_response callable."""
        self.get_response = get_response
    
    def __call__(self, request):
        """Process the request and log the details before passing to the next middleware."""
        # Get the authenticated user, default to 'Anonymous' if not authenticated
        user = request.user.username if request.user.is_authenticated else 'Anonymous'
        
        # Log the request details as specified
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)
        
        # Pass the request to the next middleware or view
        response = self.get_response(request)
        
        return response

class RestrictAccessByTimeMiddleware:
    """Middleware to restrict access to the messaging app outside 9 PM to 6 PM UTC."""
    
    def __init__(self, get_response):
        """Initialize the middleware with the get_response callable."""
        self.get_response = get_response
    
    def __call__(self, request):
        """Check the current time and deny access outside 9 PM to 6 PM UTC."""
        current_time = datetime.now().time()
        start_time = datetime.strptime("21:00:00", "%H:%M:%S").time()  # 9 PM UTC
        end_time = datetime.strptime("06:00:00", "%H:%M:%S").time()    # 6 AM UTC

        # Check if current time is outside the allowed range (9 PM to 6 AM next day)
        if current_time >= start_time or current_time < end_time:
            return HttpResponseForbidden("Access restricted outside 9 PM to 6 PM UTC.")
        
        # Allow the request if within the allowed time
        response = self.get_response(request)
        return response