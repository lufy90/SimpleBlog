from django.urls import path
from . import views

app_name = 'entries'

urlpatterns = [
    # Public Post URLs
    path('', views.PostListView.as_view(), name='post_list'),
    path('posts/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    
    # User's Posts URLs
    path('my-posts/', views.MyPostsListView.as_view(), name='my_posts'),
    path('new/', views.PostCreateView.as_view(), name='post_create'),
    path('my-posts/<int:pk>/', views.MyPostDetailView.as_view(), name='my_post_detail'),
    path('<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_update'),
    path('<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    
    # Filtered Views
    path('pinned/', views.pinned_posts, name='pinned_posts'),
    path('category/<int:category_id>/', views.posts_by_category, name='posts_by_category'),
    path('all/', views.all_posts, name='all_posts'),
    
    # Authentication
    path('logout/', views.custom_logout, name='logout'),
] 