from django.http import Http404
from functools import wraps


def allowed_roles(allowed=None):
    if allowed is None:
        allowed = []

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            user = request.user
            if user and user.groups.exists() and user.groups.all()[0].name in allowed:
                return view_func(request, *args, **kwargs)
            else:
                raise Http404

        return _wrapped_view

    return decorator

