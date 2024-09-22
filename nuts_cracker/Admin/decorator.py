from django.contrib import messages
from django.shortcuts import redirect
from functools import wraps

def admin_required(fn):
    @wraps(fn)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, "You need to log in first.")
            return redirect("admin_login")
        
        if not request.user.is_superuser:
            messages.error(request, "You are not authorized to access this page.")
            return redirect("index")  # Redirect to a different page if not an admin
        
        return fn(request, *args, **kwargs)
    return wrapper

