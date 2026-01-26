from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import (
PostsListView, 
PostCreateOrUpdateView, 
PostDeleteView, 
PostDetailView, 
like_post_ajax, 
like_comment_ajax, 
ReelFeedView, 
like_reel_ajax,
ReelCreateView
)
#Posts urls
app_name = 'posts'

urlpatterns = [
    path('<uuid:user_uuid>/list', login_required(PostsListView.as_view()), name='list'),
    path('<uuid:user_uuid>/create', login_required(PostCreateOrUpdateView.as_view()), name='create'),
    path('<uuid:user_uuid>/<int:pk>/edit', login_required(PostCreateOrUpdateView.as_view()), name='edit'),
    path('<int:pk>/delete', login_required(PostDeleteView.as_view()), name='delete'),
    path('<int:pk>/detail', login_required(PostDetailView.as_view()), name='detail'),
    path('<int:pk>/like', like_post_ajax, name='like_ajax'),
    path('<int:pk>/like_comment', like_comment_ajax, name='like_comment_ajax'),

    path('reels/feed', ReelFeedView.as_view(), name='reels_feed'), 
    path('reel/<int:pk>/like', like_reel_ajax, name='like_reel_ajax'),
    path('reels/<uuid:user_uuid>/create', ReelCreateView.as_view(), name='create_reel'),
]
