from django.shortcuts import redirect, reverse
from profiles.models import UserProfile

class ProfileCompletionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.user.is_authenticated:
            profile = getattr(request.user, 'profile', None)
            if profile and not profile.bio:
                profile_url = reverse('profiles:update')
                if not request.path.startswith(profile_url) and request.path != reverse('logout'):
                    return redirect(profile_url)
        return self.get_response(request)
