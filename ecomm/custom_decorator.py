from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from functools import wraps

def ajax_login_required(view_func):
    @wraps(view_func)
    def wrapped_view(request, *args, **kwargs):
        if not request.user.is_authenticated:
            # Check if this is an AJAX request
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'message': 'User not authenticated'}, status=401)
            else:
                # For non-AJAX requests, behave as normal login_required decorator
                return login_required(view_func)(request, *args, **kwargs)
        return view_func(request, *args, **kwargs)
    
    return wrapped_view
