from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone
from django.db.models import Q
import os


def file_upload_path(instance, filename):
    """Generate file path for uploaded files"""
    # Create path like: media/files/2024/01/15/filename.ext
    date_path = timezone.now().strftime('%Y/%m/%d')
    return os.path.join('files', date_path, filename)


class FileModel(models.Model):
    """Model to store uploaded files"""
    file = models.FileField(upload_to=file_upload_path)
    original_filename = models.CharField(max_length=255)
    file_type = models.CharField(max_length=50, blank=True)
    file_size = models.IntegerField(default=0)  # Size in bytes
    is_image_file = models.BooleanField(default=False)  # Database field for admin filtering
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='uploaded_files')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=500, blank=True)
    
    class Meta:
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return self.original_filename
    
    def save(self, *args, **kwargs):
        if not self.original_filename and self.file:
            self.original_filename = os.path.basename(self.file.name)
        
        if not self.file_type and self.file:
            # Get file extension
            ext = os.path.splitext(self.file.name)[1].lower()
            self.file_type = ext
        
        if not self.file_size and self.file:
            try:
                self.file_size = self.file.size
            except:
                pass
        
        # Set is_image_file based on file type
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
        self.is_image_file = self.file_type.lower() in image_extensions
        
        super().save(*args, **kwargs)
    
    @property
    def is_image(self):
        """Check if file is an image (property for backward compatibility)"""
        return self.is_image_file
    
    @property
    def file_url(self):
        """Get the URL for the file"""
        return self.file.url if self.file else None
    
    @property
    def file_size_mb(self):
        """Get file size in MB"""
        return round(self.file_size / (1024 * 1024), 2)


class Category(models.Model):
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=1024, null=True, blank=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='entry_categories')
    created_on = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name_plural = 'Categories'
        unique_together = ['name', 'author']
    
    def __str__(self):
        return self.name


class Entry(models.Model):
    MOOD_CHOICES = [
        ('happy', 'Happy'),
        ('sad', 'Sad'),
        ('excited', 'Excited'),
        ('calm', 'Calm'),
        ('anxious', 'Anxious'),
        ('neutral', 'Neutral'),
    ]
    
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
    ]
    
    VISIBILITY_CHOICES = [
        ('private', 'Private'),
        ('public', 'Public'),
    ]
    
    # Core fields
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='entries')
    title = models.CharField(max_length=200, null=True, blank=True)
    content = models.TextField(null=True, blank=True)
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    published_on = models.DateTimeField(null=True, blank=True)
    
    date = models.DateField(null=True, blank=True)  # For diary entries
    mood = models.CharField(max_length=10, choices=MOOD_CHOICES, blank=True)
    visibility = models.CharField(max_length=10, choices=VISIBILITY_CHOICES, default='private')
    
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='entries')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    is_pinned = models.BooleanField(default=False)
    
    # Files relationship
    files = models.ManyToManyField(FileModel, blank=True, related_name='entries')
    
    # Common fields
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-is_pinned', '-updated_on']
        verbose_name_plural = 'Entries'
        indexes = [
            models.Index(fields=['author', '-updated_on']),
            models.Index(fields=['date', '-created_on']),
            models.Index(fields=['category', '-updated_on']),
        ]
    
    def __str__(self):
        return self.title or f"Post {self.id}"
    
    def save(self, *args, **kwargs):
        # Auto-generate slug for posts
        if not self.slug:
            if self.title:
                self.slug = slugify(self.title, allow_unicode=True)
            else:
                # Use timestamp if no title
                self.slug = slugify(f"post-{timezone.now().strftime('%Y%m%d-%H%M%S')}")

        if not self._state.adding:
            original = Entry.objects.get(pk=self.pk)
            if not original.is_published and self.is_published:
                self.published_on = timezone.now()
            elif original.is_published and not self.is_published:
                self.published_on = None
            else:
                self.published_on = original.published_on

        # Set date to created_on date if not set
        if not self.date:
            self.date = self.created_on.date() if self.created_on else timezone.now().date()

        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        """Get the canonical URL for this post (public URL if published, private URL if not)"""
        if self.visibility == 'public':
            return self.get_public_url()
        else:
            return self.get_private_url()
    
    def get_public_url(self):
        """Get the public URL for this post (post/<slug>/)"""
        return reverse('entries:post_detail', args=[self.slug])
    
    def get_private_url(self):
        """Get the private URL for this post (my-post/<pk>/)"""
        return reverse('entries:my_post_detail', args=[self.pk])
    
    @property
    def is_published(self):
        return self.visibility == 'public'
    
    @property
    def attached_images(self):
        """Get all attached image files"""
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
        q_objects = Q()
        for ext in image_extensions:
            q_objects |= Q(file__endswith=ext)
        return self.files.filter(q_objects)
    
    @property
    def attached_files(self):
        """Get all attached non-image files"""
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.webp']
        q_objects = Q()
        for ext in image_extensions:
            q_objects |= Q(file__endswith=ext)
        return self.files.exclude(q_objects)
