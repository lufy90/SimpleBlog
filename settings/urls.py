from django.urls import path
from . import views

app_name = 'settings'

urlpatterns = [
    path('test/', views.test_settings, name='test_settings'),
] 