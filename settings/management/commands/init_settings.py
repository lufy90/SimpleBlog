from django.core.management.base import BaseCommand
from settings.models import SiteSettings


class Command(BaseCommand):
    help = 'Initialize default site settings'

    def handle(self, *args, **options):
        if SiteSettings.objects.exists():
            self.stdout.write(
                self.style.WARNING('Site settings already exist. Use admin interface to modify.')
            )
            return

        settings = SiteSettings.objects.create(
            site_name="SimpleBlog",
            site_description="A personal blog built with Django",
            site_tagline="Share your thoughts and experiences",
            contact_email="",
            posts_per_page=10,
            my_posts_per_page=20,
            search_results_per_page=15,
            show_author_info=True,
            show_post_dates=True,
            show_categories=True,
            show_mood_badges=True,
            show_priority_badges=True,
            copyright_text="© 2025 SimpleBlog. All rights reserved.",
            footer_text="",
            powered_by_text="Built with Django",
            enable_search=True,
            enable_categories=True,
            enable_file_uploads=True,
            enable_mood_tracking=True,
            enable_priority_tracking=True,
            enable_pinning=True,
        )

        self.stdout.write(
            self.style.SUCCESS(f'Successfully created default site settings: {settings.site_name}')
        ) 
