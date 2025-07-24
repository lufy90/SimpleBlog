from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
import json
from .models import SiteSettings
from .forms import SiteSettingsForm


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


@login_required
@user_passes_test(lambda u: u.is_staff)
def manage_settings(request):
    """View to manage site settings"""
    settings = SiteSettings.get_settings()
    
    if request.method == 'POST':
        form = SiteSettingsForm(request.POST, request.FILES, instance=settings)
        if form.is_valid():
            form.save()
            messages.success(request, 'Site settings updated successfully!')
            return redirect('settings:manage_settings')
    else:
        form = SiteSettingsForm(instance=settings)
    
    context = {
        'form': form,
        'settings': settings,
    }
    return render(request, 'settings/manage_settings.html', context)


@login_required
@require_http_methods(["POST"])
def update_theme(request):
    """Update theme preference via AJAX"""
    try:
        data = json.loads(request.body)
        theme = data.get('theme')
        
        if theme:
            settings = SiteSettings.get_settings()
            if settings:
                settings.theme = theme
                settings.save()
                return JsonResponse({'status': 'success', 'theme': theme})
        
        return JsonResponse({'status': 'error', 'message': 'Invalid theme'})
    except Exception as e:
        return JsonResponse({'status': 'error', 'message': str(e)})
