from django.core.management.base import BaseCommand
from entries.models import FileModel
import os


class Command(BaseCommand):
    help = 'Fix video file detection for existing files'

    def handle(self, *args, **options):
        video_extensions = ['.mp4', '.avi', '.mov', '.wmv', '.flv', '.webm', '.mkv', '.m4v', '.mpeg']
        
        # Get all files
        files = FileModel.objects.all()
        updated_count = 0
        
        for file_obj in files:
            if file_obj.file:
                # Get the file extension from the actual file
                filename = file_obj.file.name
                ext = os.path.splitext(filename)[1]  # Keep original case
                
                # Check if this is a video file (case-insensitive)
                if ext.lower() in [ext.lower() for ext in video_extensions]:
                    # Update the file_type if it's not correct
                    if file_obj.file_type.lower() != ext.lower():
                        file_obj.file_type = ext
                        file_obj.save()
                        updated_count += 1
                        self.stdout.write(
                            self.style.SUCCESS(f'Updated {file_obj.original_filename} to video type: {ext}')
                        )
                    else:
                        self.stdout.write(
                            self.style.WARNING(f'File {file_obj.original_filename} already has correct type: {file_obj.file_type}')
                        )
        
        self.stdout.write(
            self.style.SUCCESS(f'Successfully updated {updated_count} video files')
        ) 