from django.urls import path
from . import views

app_name = 'settings'

urlpatterns = [
    path('test/', views.test_settings, name='test_settings'),
    path('manage/', views.manage_settings, name='manage_settings'),
    path('update-theme/', views.update_theme, name='update_theme'),
] 