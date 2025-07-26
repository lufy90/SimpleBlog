from django.urls import path, re_path
from . import views

app_name = 'entries'

urlpatterns = [
    # Post Views
    path('', views.PostListView.as_view(), name='post_list'),
    path('post/new/', views.PostCreateView.as_view(), name='post_create'),
    re_path(r'^post/(?P<slug>[\w\-]+)/$', views.PostDetailView.as_view(), name='post_detail'),
    #path('post/<slug:slug>/', views.PostDetailView.as_view(), name='post_detail'),
    path('post/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_update'),
    path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post_delete'),
    
    # User's Posts Views
    path('my-posts/', views.MyPostsListView.as_view(), name='my_posts'),
    path('my-post/<int:pk>/', views.MyPostDetailView.as_view(), name='my_post_detail'),
    
    # Category and Filtered Views
    path('category/<int:category_id>/', views.posts_by_category, name='posts_by_category'),
    path('pinned/', views.pinned_posts, name='pinned_posts'),
    path('all/', views.all_posts, name='all_posts'),
    
    # Search
    path('search/', views.search_posts, name='search_posts'),
    
    # Pin/Unpin
    path('post/<int:pk>/toggle-pin/', views.toggle_pin, name='toggle_pin'),
    
    # Authentication
    path('logout/', views.custom_logout, name='logout'),
    
    # Comment URLs
    path('post/<int:post_id>/comment/', views.add_comment, name='add_comment'),
    path('comment/<int:comment_id>/reply/', views.add_reply, name='add_reply'),
    path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),
    path('comment/<int:comment_id>/edit/', views.edit_comment, name='edit_comment'),
    
    # Debug
    path('debug-files/<int:post_id>/', views.debug_files, name='debug_files'),
] 
