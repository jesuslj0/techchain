from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import PostsListView, PostsCreateView, PostDeleteView, PostDetailView, like_post_ajax

#Posts urls
app_name = 'posts'

urlpatterns = [
    path('<uuid:user_uuid>/list', login_required(PostsListView.as_view()), name='list',),
    path('<uuid:user_uuid>/create', login_required(PostsCreateView.as_view()), name='create',),
    path('<int:pk>/delete', login_required(PostDeleteView.as_view()), name='delete'),
    path('<int:pk>/detail', login_required(PostDetailView.as_view()), name='detail'),
    path('<int:pk>/like', like_post_ajax, name='like_ajax'),
]
