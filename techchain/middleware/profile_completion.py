from django.shortcuts import redirect, reverse
from django.conf import settings

class ProfileCompletionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.EXCLUDED_URLS = getattr(settings, 'PROFILE_EXCLUDE_URLS', ['/accounts/'])

    def __call__(self, request):

        for url in self.EXCLUDED_URLS:
            if request.path.startswith(url):
                return self.get_response(request)
        
        if request.user.is_authenticated:
            profile = getattr(request.user, 'profile', None)

            if profile and not profile.bio:
                profile_url = reverse('profiles:update')

                if not request.path.startswith(profile_url) and request.path != reverse('logout'):
                    return redirect(profile_url)
        return self.get_response(request)
