try:
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps  # Python 2.4 fallback.

from django.contrib import messages

default_message = "Please log in, in order to see the requested page."


def user_passes_test(test_func, message=default_message):
    """
    Decorator for views that checks that the user passes the given test,
    setting a message in case of no success. The test should be a callable
    that takes the user object and returns True if the user passes.
    """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if not test_func(request.user):
                messages.warning(request, message)
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator


def login_required_message(function=None, message=default_message):
    """
    Decorator for views that checks that the user is logged in, redirecting
    to the log-in page if necessary.
    """
    actual_decorator = user_passes_test(
        lambda u: u.is_authenticated,  # fixed by removing ()
        message=message,
    )
    if function:
        return actual_decorator(function)
    return actual_decorator
