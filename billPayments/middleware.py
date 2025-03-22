import threading

# Thread-local storage for request
request_local = threading.local()

class RequestMiddleware:
    """Middleware to store the current request in thread-local storage."""
    
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        request_local.current_request = request  # Store request in thread-local
        response = self.get_response(request)
        return response

    @staticmethod
    def get_request():
        """Retrieve the stored request."""
        return getattr(request_local, 'current_request', None)
