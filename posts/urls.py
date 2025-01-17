from django.urls import path, include
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.conf.urls.static import static
from .views import PostsListView, PostsCreateView, PostDeleteView, PostDetailView, like_post_ajax

#Profiles urls

app_name = 'posts'

urlpatterns = [
    path('<int:user_id>/list', login_required(PostsListView.as_view()), name='list',),
    path('<int:user_id>/create', login_required(PostsCreateView.as_view()), name='create',),
    path('<int:pk>/delete', login_required(PostDeleteView.as_view()), name='delete'),
    path('<int:pk>/detail', login_required(PostDetailView.as_view()), name='detail'),
    path('<int:pk>/like', like_post_ajax, name='like_ajax'),
]

if settings.DEBUG:  # Solo durante el desarrollo
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)