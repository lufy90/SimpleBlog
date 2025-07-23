from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone


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
                self.slug = slugify(self.title)
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
        # Use slug for public posts, pk for user's posts
        if self.visibility == 'public':
            return reverse('entries:post_detail', args=[self.slug])
        else:
            return reverse('entries:my_post_detail', args=[self.pk])
    
    @property
    def is_published(self):
        return self.visibility == 'public'
