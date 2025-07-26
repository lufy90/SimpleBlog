from django.contrib import admin
from .models import Entry, Category, FileModel, Comment


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


@admin.register(FileModel)
class FileModelAdmin(admin.ModelAdmin):
    list_display = ['original_filename', 'file_type', 'file_size_mb', 'uploaded_by', 'uploaded_at', 'is_image_file', 'is_video']
    list_filter = ['file_type', 'uploaded_by', 'uploaded_at', 'is_image_file']
    search_fields = ['original_filename', 'description']
    readonly_fields = ['file_size', 'uploaded_at', 'is_image_file', 'is_video']
    
    fieldsets = (
        ('File Information', {
            'fields': ('file', 'original_filename', 'description')
        }),
        ('File Details', {
            'fields': ('file_type', 'file_size', 'is_image_file', 'is_video', 'uploaded_by', 'uploaded_at'),
            'classes': ('collapse',)
        }),
    )
    
    def is_video(self, obj):
        return obj.is_video
    is_video.boolean = True
    is_video.short_description = 'Is Video'


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['get_author_display', 'entry', 'is_approved', 'created_on', 'is_reply']
    list_filter = ['is_approved', 'created_on', 'parent', 'entry__author']
    search_fields = ['content', 'author_name', 'entry__title']
    readonly_fields = ['created_on', 'updated_on']
    list_editable = ['is_approved']
    
    fieldsets = (
        ('Comment Content', {
            'fields': ('content', 'entry')
        }),
        ('Author Information', {
            'fields': ('author', 'author_name', 'author_email')
        }),
        ('Comment Details', {
            'fields': ('parent', 'is_approved')
        }),
        ('Timestamps', {
            'fields': ('created_on', 'updated_on'),
            'classes': ('collapse',)
        }),
    )
    
    def get_author_display(self, obj):
        return obj.get_author_display()
    get_author_display.short_description = 'Author'
    
    def is_reply(self, obj):
        return obj.is_reply
    is_reply.boolean = True
    is_reply.short_description = 'Is Reply'
