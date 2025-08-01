# Django-Middleware-0x03/chats/middleware.py
import logging
from datetime import datetime, timedelta
from pathlib import Path
from django.http import HttpResponseForbidden, JsonResponse
import json
from collections import defaultdict

# Define the absolute path for the log file in the project root
project_root = Path(__file__).resolve().parent.parent
log_file = project_root / 'requests.log'

# Configure a basic logger
logger = logging.getLogger('request_logger')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(log_file)
formatter = logging.Formatter('%(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)

# Store message counts per IP address with timestamps
message_counts = defaultdict(list)

class RequestLoggingMiddleware:
    """Middleware to log user requests with timestamp, user, and path."""
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        user = request.user.username if request.user.is_authenticated else 'Anonymous'
        log_message = f"{datetime.now()} - User: {user} - Path: {request.path}"
        logger.info(log_message)
        response = self.get_response(request)
        return response

class RestrictAccessByTimeMiddleware:
    """Middleware to restrict access to the messaging app outside 9 PM to 6 PM UTC."""
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        current_time = datetime.now().time()
        start_time = datetime.strptime("21:00:00", "%H:%M:%S").time()
        end_time = datetime.strptime("06:00:00", "%H:%M:%S").time()
        if current_time >= start_time or current_time < end_time:
            return HttpResponseForbidden("Access restricted outside 9 PM to 6 PM UTC.")
        response = self.get_response(request)
        return response

class OffensiveLanguageMiddleware:
    """Middleware to limit the number of chat messages per IP address within a time window."""
    def __init__(self, get_response):
        self.get_response = get_response
        self.message_limit = 5  # Max 5 messages
        self.time_window = timedelta(minutes=1)  # 1-minute window
    
    def __call__(self, request):
        global message_counts
        ip_address = request.META.get('REMOTE_ADDR', 'unknown_ip')
        if request.method == 'POST' and '/api/conversations/' in request.path:
            current_time = datetime.now()
            message_counts[ip_address] = [t for t in message_counts[ip_address] if current_time - t < self.time_window]
            if len(message_counts[ip_address]) >= self.message_limit:
                return HttpResponseForbidden("Message limit of 5 per minute exceeded for your IP.")
            message_counts[ip_address].append(current_time)
        response = self.get_response(request)
        return response

class RolepermissionMiddleware:
    """Middleware to enforce role-based access permissions for chat actions."""
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if request.user.is_authenticated:
            is_admin = getattr(request.user, 'is_admin', False)
            is_moderator = getattr(request.user, 'is_moderator', False)
            if not (is_admin or is_moderator):
                return HttpResponseForbidden("Access denied. Only admins and moderators are allowed.")
        response = self.get_response(request)
        return response

class BannedIPMiddleware:
    """Middleware to block requests from banned IPs."""
    def __init__(self, get_response):
        self.get_response = get_response
        self.banned_ips = {'192.168.1.1', '10.0.0.1'}  # Use env var in production
    
    def __call__(self, request):
        ip_address = request.META.get('REMOTE_ADDR')
        if ip_address in self.banned_ips:
            return HttpResponseForbidden("Your IP is banned.")
        response = self.get_response(request)
        return response

class PayloadValidationMiddleware:
    """Middleware to validate incoming JSON payloads."""
    def __init__(self, get_response):
        self.get_response = get_response
    
    def __call__(self, request):
        if request.method in ['POST', 'PUT', 'PATCH'] and request.content_type == 'application/json':
            try:
                data = json.loads(request.body)
                if not isinstance(data, dict) or 'content' not in data:
                    return JsonResponse({"error": "Invalid JSON payload; 'content' field required"}, status=400)
                request.data = data
            except json.JSONDecodeError:
                return JsonResponse({"error": "Invalid JSON"}, status=400)
        response = self.get_response(request)
        return response