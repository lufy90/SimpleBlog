from .models import SiteSettings


def site_settings(request):
    """Add site settings to template context"""
    try:
        settings = SiteSettings.get_settings()
        if settings:
            return {
                'site_settings': settings,
                'site_name': settings.site_name,
                'site_description': settings.site_description,
                'site_tagline': settings.site_tagline,
                'copyright_text': settings.copyright_text,
                'footer_text': settings.footer_text,
                'powered_by_text': settings.powered_by_text,
            }
        else:
            # Fallback if no settings exist
            return get_fallback_settings()
    except Exception as e:
        # Fallback values if settings are not available
        print(f"Settings context processor error: {e}")
        return get_fallback_settings()


def get_fallback_settings():
    """Return fallback settings when database is not available"""
    return {
        'site_settings': None,
        'site_name': 'My Blog',
        'site_description': '',
        'site_tagline': '',
        'copyright_text': '© 2025 My Blog. All rights reserved.',
        'footer_text': '',
        'powered_by_text': 'Built with Django',
    } 