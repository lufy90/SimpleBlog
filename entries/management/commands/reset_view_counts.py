from django.core.management.base import BaseCommand
from django.db import transaction
from entries.models import Entry


class Command(BaseCommand):
    help = 'Reset view counts for entries'

    def add_arguments(self, parser):
        parser.add_argument(
            '--all',
            action='store_true',
            help='Reset view counts for all entries',
        )
        parser.add_argument(
            '--public-only',
            action='store_true',
            help='Reset view counts for public entries only',
        )
        parser.add_argument(
            '--entry-id',
            type=int,
            help='Reset view count for a specific entry ID',
        )

    def handle(self, *args, **options):
        with transaction.atomic():
            if options['entry_id']:
                try:
                    entry = Entry.objects.get(id=options['entry_id'])
                    entry.view_count = 0
                    entry.save(update_fields=['view_count'])
                    self.stdout.write(
                        self.style.SUCCESS(
                            f'Successfully reset view count for entry "{entry.title}" (ID: {entry.id})'
                        )
                    )
                except Entry.DoesNotExist:
                    self.stdout.write(
                        self.style.ERROR(f'Entry with ID {options["entry_id"]} does not exist')
                    )
            
            elif options['public_only']:
                count = Entry.objects.filter(visibility='public').update(view_count=0)
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully reset view counts for {count} public entries')
                )
            
            elif options['all']:
                count = Entry.objects.all().update(view_count=0)
                self.stdout.write(
                    self.style.SUCCESS(f'Successfully reset view counts for {count} entries')
                )
            
            else:
                self.stdout.write(
                    self.style.WARNING(
                        'Please specify --all, --public-only, or --entry-id. Use --help for more information.'
                    )
                ) 