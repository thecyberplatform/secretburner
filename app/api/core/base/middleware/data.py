import json
from core.base.functions.data import replace_with_null


class ConvertRequestEmptyStringToNull:
    """
    Middleware to convert empty string values in JSON request bodies to None (null).

    This middleware intercepts incoming requests and modifies any JSON data where
    empty string values ('') are converted to None. This can be particularly useful
    to ensure that the backend consistently handles empty strings from frontends as None.

    Attributes:
        get_response: A callable that takes a request and returns a response. This is the
                      next middleware or view in the Django middleware chain.

    Methods:
        __call__(request): Processes the incoming request, converts empty strings in JSON
                           bodies to None, and forwards the request down the middleware chain.
    """

    def __init__(self, get_response):
        """
        Initializes the middleware with the next item in the middleware chain.

        Parameters:
            get_response (callable): The next middleware or view in the chain that
                                     takes a request and returns a response.
        """
        self.get_response = get_response

    def __call__(self, request):
        """
        Called for each request before it reaches the view. Converts empty strings in JSON
        request bodies to None.

        Parameters:
            request: The HttpRequest object containing the request data.

        Returns:
            The response object obtained from calling the next middleware or view.
        """
        try:
            if getattr(request, "body", None):
                # Decode and parse the JSON body of the request
                data = json.loads(getattr(request, "_body", request.body).decode())
                # Replace all empty string values with None
                replace_with_null(data, "")
                # Re-encode the modified data and update the request body
                setattr(request, "_body", json.dumps(data).encode())

        except json.JSONDecodeError:
            # Handle cases where the request body is not valid JSON
            pass

        except UnicodeDecodeError:
            # Handle cases where decoding fails
            pass

        finally:
            # Proceed to the next middleware or view and return its response
            return self.get_response(request)
