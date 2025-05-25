# core/middleware.py
import threading

_user = threading.local()


class CurrentUserMiddleware:
    """
    Middleware that saves the current logged-in user in thread-local storage.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _user.value = request.user
        response = self.get_response(request)
        return response


def get_current_user():
    return getattr(_user, "value", None)
