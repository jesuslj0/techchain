from django.urls import path
from .views import RegisterView, CustomLoginView, PingView, PostCreateView, PostListView
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'api'
urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('login/', CustomLoginView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('posts/', PostCreateView.as_view(), name='post-create'),
    path('posts/user/<str:username>', PostListView.as_view(), name='user-posts-list'),
    path('ping/', PingView.as_view(), name="ping"),
]