from profiles.models import UserProfile

def user_profile_context(request):
    if request.user.is_authenticated:
        try:
            return {'user_id': request.user.uuid}
        except UserProfile.DoesNotExist:
            return {}
    return {}
