from django.shortcuts import redirect
from django.contrib import messages

def login_required_message(view_func):
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.warning(request, 'Please login first to continue')
            return redirect('login')
        return view_func(request, *args, **kwargs)
    return wrapper