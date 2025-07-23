from django.contrib import admin
from .models import Entry, Category, FileModel


@admin.register(FileModel)
class FileModelAdmin(admin.ModelAdmin):
    list_display = ['original_filename', 'file_type', 'file_size_mb', 'uploaded_by', 'uploaded_at', 'is_image_file']
    list_filter = ['file_type', 'uploaded_by', 'uploaded_at', 'is_image_file']
    search_fields = ['original_filename', 'description']
    readonly_fields = ['file_size', 'uploaded_at', 'is_image_file']
    
    fieldsets = (
        ('File Information', {
            'fields': ('file', 'original_filename', 'description')
        }),
        ('File Details', {
            'fields': ('file_type', 'file_size', 'is_image_file', 'uploaded_by', 'uploaded_at'),
            'classes': ('collapse',)
        }),
    )


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'created_on']
    list_filter = ['author', 'created_on']
    search_fields = ['name', 'desc']


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'visibility', 'category', 'priority', 'is_pinned', 'created_on']
    list_filter = ['visibility', 'category', 'priority', 'is_pinned', 'mood', 'created_on', 'author']
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ['created_on', 'updated_on', 'published_on']
    
    fieldsets = (
        ('Content', {
            'fields': ('title', 'content', 'slug')
        }),
        ('Metadata', {
            'fields': ('author', 'visibility', 'category', 'priority', 'is_pinned')
        }),
        ('Additional Info', {
            'fields': ('date', 'mood'),
            'classes': ('collapse',)
        }),
        ('Files', {
            'fields': ('files',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_on', 'updated_on', 'published_on'),
            'classes': ('collapse',)
        }),
    )
    
    filter_horizontal = ['files']
