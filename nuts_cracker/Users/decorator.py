from django.contrib import messages
from django.shortcuts import redirect

def login_required(fn):
  def wrapper(request, *args, **kwargs):
    # Check if the user is authenticated
    if not request.user.is_authenticated:
        messages.warning(request, "You have to log in first.")
        return redirect("login")  # Redirect to the login page
    
    # If the user is authenticated, allow access
    return fn(request, *args, **kwargs)
  
  return wrapper


# def non_superuser_required(fn):
#     """Decorator to allow only non-superusers to access a view."""
#     @wraps(fn)
#     def wrapper(request, *args, **kwargs):
#         if not request.user.is_authenticated:
#             messages.warning(request, "You need to log in first.")
#             return redirect("log_view")  # Redirect to the login page if not logged in
        
#         if request.user.is_superuser:
#             messages.error(request, "Superusers are not allowed to access this page.")
#             return redirect("home")  # Redirect superusers to another page (e.g., home)

#         return fn(request, *args, **kwargs)
    
#     return wrapper
