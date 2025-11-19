from django.urls import path
from .views import RegisterView, CustomLoginView, PingView
from rest_framework_simplejwt.views import TokenRefreshView

app_name = 'api'
urlpatterns = [
    path('register/', RegisterView.as_view(), name='auth_register'),
    path('login/', CustomLoginView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('ping/', PingView.as_view(), name="ping"),
]