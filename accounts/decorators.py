from django.http import HttpResponseForbidden
from functools import wraps

def role_required(required_roles):
    """ Decorator to restrict views based on user role """
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.role not in required_roles:
                return HttpResponseForbidden("🚫 You do not have permission to access this page.")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
