from django.core.management.base import BaseCommand
from entries.models import FileModel, Entry


class Command(BaseCommand):
    help = 'Check video file types in database'

    def handle(self, *args, **options):
        # Get all files
        files = FileModel.objects.all()
        
        self.stdout.write("=== All Files ===")
        for file_obj in files:
            self.stdout.write(
                f"ID: {file_obj.id}, "
                f"Name: {file_obj.original_filename}, "
                f"Type: '{file_obj.file_type}', "
                f"Is Video: {file_obj.is_video}, "
                f"File Path: {file_obj.file.name if file_obj.file else 'None'}"
            )
        
        # Get all entries with files
        entries = Entry.objects.prefetch_related('files').all()
        
        self.stdout.write("\n=== Entries with Files ===")
        for entry in entries:
            if entry.files.exists():
                self.stdout.write(f"\nEntry: {entry.title} (ID: {entry.id})")
                self.stdout.write(f"  All Files: {entry.files.count()}")
                self.stdout.write(f"  Video Files: {entry.attached_videos.count()}")
                self.stdout.write(f"  Image Files: {entry.attached_images.count()}")
                self.stdout.write(f"  Other Files: {entry.attached_files.count()}")
                
                for file_obj in entry.files.all():
                    self.stdout.write(
                        f"    - {file_obj.original_filename} "
                        f"(Type: '{file_obj.file_type}', "
                        f"Is Video: {file_obj.is_video})"
                    ) 