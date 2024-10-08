from django.shortcuts import redirect
from django.core.exceptions import PermissionDenied
from .models import Profile

def role_required(allowed_roles=[]):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            try:
                # Retrieve the profile using the username or roll number
                profile = Profile.objects.get(roll_no=request.user.username)
                if profile.role in allowed_roles:
                    return view_func(request, *args, **kwargs)
                raise PermissionDenied
            except Profile.DoesNotExist:
                raise PermissionDenied  # Handle the case where the profile does not exist
        return _wrapped_view
    return decorator
