from django.urls import path, include
from .views import ProfileDetailView, FollowersView, FollowingView, ProfileUpdateView, ProfilesSearch, toggle_follow
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static

#Profiles urls

app_name = 'profiles'

urlpatterns = [
    path('<int:user_id>/', login_required(ProfileDetailView.as_view()), name='detail',),
    path('<int:user_id>/update', login_required(ProfileUpdateView.as_view()), name='update'),
    path('<int:user_id>/followers/', login_required(FollowersView.as_view()), name='followers'),
    path('<int:user_id>/following/', login_required(FollowingView.as_view()), name="following"),
    path('<int:user_id>/follow/', toggle_follow, name='toggle_follow'),
    path('search/', login_required(ProfilesSearch.as_view()), name='search')
]

if settings.DEBUG:  # Solo durante el desarrollo
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
