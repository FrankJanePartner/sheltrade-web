import threading

# Thread-local storage for request
request_local = threading.local()

class RequestMiddleware:
    """
    Middleware to store the current request in thread-local storage.

    This middleware captures the incoming HTTP request and stores it in a thread-local
    variable so that it can be accessed globally during the request lifecycle.

    Attributes:
        get_response (callable): The next middleware or view to be called.
    """
    
    def __init__(self, get_response):
        """
        Initialize the middleware with the next callable in the chain.

        Args:
            get_response (callable): The next middleware or view.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Process the incoming request, store it in thread-local storage, and get the response.

        Args:
            request (HttpRequest): The incoming HTTP request.

        Returns:
            HttpResponse: The response from the next middleware or view.
        """
        request_local.current_request = request  # Store request in thread-local
        response = self.get_response(request)
        return response

    @staticmethod
    def get_request():
        """
        Retrieve the stored request from thread-local storage.

        Returns:
            HttpRequest or None: The current request if available, else None.
        """
        return getattr(request_local, 'current_request', None)
