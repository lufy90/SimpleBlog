from django.contrib import admin
from .models import Entry, Category


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'author', 'created_on']
    list_filter = ['author']
    search_fields = ['name']


@admin.register(Entry)
class EntryAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'visibility', 'category', 'priority', 'is_pinned', 'created_on']
    list_filter = [
        'author', 
        'visibility',
        'priority', 
        'is_pinned',
        'category',
        'mood',
        'created_on'
    ]
    search_fields = ['title', 'content']
    prepopulated_fields = {'slug': ('title',)}
    raw_id_fields = ['author', 'category']
    date_hierarchy = 'created_on'
    ordering = ['-is_pinned', '-updated_on']
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('author', 'title', 'content')
        }),
        ('Settings', {
            'fields': ('slug', 'visibility', 'category', 'priority', 'is_pinned')
        }),
        ('Additional Information', {
            'fields': ('date', 'mood', 'published_on'),
            'classes': ('collapse',),
        }),
        ('Timestamps', {
            'fields': ('created_on', 'updated_on'),
            'classes': ('collapse',),
        }),
    )
    
    readonly_fields = ('created_on', 'updated_on')
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related('author', 'category')
