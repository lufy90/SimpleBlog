from django.shortcuts import render
from django.http import JsonResponse
from .models import SiteSettings


def test_settings(request):
    """Test view to check if settings are working"""
    try:
        settings = SiteSettings.objects.first()
        if settings:
            return JsonResponse({
                'status': 'success',
                'site_name': settings.site_name,
                'settings_id': settings.id
            })
        else:
            return JsonResponse({
                'status': 'error',
                'message': 'No settings found'
            })
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        })
