
from django.contrib import admin
from django.urls import path, include
from debug_toolbar.toolbar import debug_toolbar_urls
from .views import HomeView, ContactView, LoginView, LogoutView, RegisterView, LegalView, ExploreView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name='home'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegisterView.as_view(), name='register'),
    path('legal/', LegalView.as_view(), name='legal'),
    path('explore/', ExploreView.as_view(), name='explore'),

    path('profiles/', include('profiles.urls', namespace='profiles')),

    path('posts/', include('posts.urls', namespace='posts')),

    path('chat/', include('chat.urls')),

    path("prose/", include("prose.urls")),
] + debug_toolbar_urls()

from django.urls import path

