from django.contrib.auth import get_user_model

User = get_user_model()

def user_profile_context(request):
    if request.user.is_authenticated:
        return {'user_uuid': request.user.uuid}  # cambia user_id por user_uuid
    return {}

