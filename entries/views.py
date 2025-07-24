from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth import logout
from django.utils.html import strip_tags
import re
from .models import Entry, Category, FileModel
from .forms import EntryForm


# Post Views
class PostListView(ListView):
    model = Entry
    template_name = 'entries/post_list.html'
    context_object_name = 'posts'
    paginate_by = 10
    
    def get_queryset(self):
        return Entry.objects.filter(
            visibility='public'
        ).order_by('-published_on', '-created_on')


class PostDetailView(DetailView):
    model = Entry
    template_name = 'entries/post_detail.html'
    context_object_name = 'post'
    
    def get_queryset(self):
        return Entry.objects.filter(
            visibility='public'
        )
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        
        # Get previous and next posts
        try:
            # For public posts, order by published_on first, then created_on as fallback
            context['next_post'] = Entry.objects.filter(
                visibility='public'
            ).exclude(
                id=post.id
            ).filter(
                Q(published_on__lt=post.published_on) if post.published_on else Q(created_on__lt=post.created_on)
            ).order_by(
                '-published_on', '-created_on'
            ).first()
        except:
            context['next_post'] = None
            
        try:
            context['previous_post'] = Entry.objects.filter(
                visibility='public'
            ).exclude(
                id=post.id
            ).filter(
                Q(published_on__gt=post.published_on) if post.published_on else Q(created_on__gt=post.created_on)
            ).order_by(
                'published_on', 'created_on'
            ).first()
        except:
            context['previous_post'] = None
        
        # Indicate this is the public post view
        context['is_my_post_view'] = False
        
        return context


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Entry
    template_name = 'entries/post_form.html'
    form_class = EntryForm
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        if form.instance.visibility == 'public' and not form.instance.published_on:
            form.instance.published_on = timezone.now()
        response = super().form_valid(form)
        # Handle file uploads
        files = self.request.FILES.getlist('files')
        uploaded_files = []
        for uploaded_file in files:
            if uploaded_file:
                file_model = FileModel.objects.create(
                    file=uploaded_file,
                    uploaded_by=self.request.user,
                    original_filename=uploaded_file.name
                )
                self.object.files.add(file_model)
                uploaded_files.append(file_model)
        
        # Store uploaded files in session for template access
        if uploaded_files:
            self.request.session['recently_uploaded_files'] = [
                {'url': f.file.url, 'name': f.original_filename, 'is_image': f.is_image_file}
                for f in uploaded_files
            ]
        
        messages.success(self.request, 'Post created successfully!')
        # Clear recently uploaded files from session
        if 'recently_uploaded_files' in self.request.session:
            del self.request.session['recently_uploaded_files']
        return response
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(author=self.request.user)
        return context


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Entry
    template_name = 'entries/post_form.html'
    form_class = EntryForm
    
    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['user'] = self.request.user
        return kwargs
    
    def form_valid(self, form):
        if form.instance.visibility == 'public' and not form.instance.published_on:
            form.instance.published_on = timezone.now()
        response = super().form_valid(form)
        # Handle file uploads
        files = self.request.FILES.getlist('files')
        for uploaded_file in files:
            if uploaded_file:
                file_model = FileModel.objects.create(
                    file=uploaded_file,
                    uploaded_by=self.request.user,
                    original_filename=uploaded_file.name
                )
                self.object.files.add(file_model)
        messages.success(self.request, 'Post updated successfully!')
        return response
    
    def test_func(self):
        entry = self.get_object()
        return self.request.user == entry.author
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(author=self.request.user)
        return context


class PostDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
    model = Entry
    template_name = 'entries/post_confirm_delete.html'
    success_url = reverse_lazy('entries:post_list')
    
    def test_func(self):
        entry = self.get_object()
        return self.request.user == entry.author


# User's Posts Views
class MyPostsListView(LoginRequiredMixin, ListView):
    model = Entry
    template_name = 'entries/my_posts.html'
    context_object_name = 'posts'
    paginate_by = 20
    
    def get_queryset(self):
        return Entry.objects.filter(
            author=self.request.user
        ).order_by('-is_pinned', '-created_on')


class MyPostDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Entry
    template_name = 'entries/post_detail.html'
    context_object_name = 'post'
    
    def test_func(self):
        entry = self.get_object()
        return self.request.user == entry.author
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        post = self.get_object()
        
        # Get previous and next posts for the same user
        try:
            context['next_post'] = Entry.objects.filter(
                author=post.author
            ).exclude(
                id=post.id
            ).filter(
                #Q(published_on__lt=post.published_on) if post.published_on else Q(created_on__lt=post.created_on)
                Q(created_on__lt=post.created_on)
            ).order_by(
                '-is_pinned', '-created_on'
            ).first()
        except:
            context['next_post'] = None
            
        try:
            context['previous_post'] = Entry.objects.filter(
                author=post.author
            ).exclude(
                id=post.id
            ).filter(
                #Q(published_on__gt=post.published_on) if post.published_on else Q(created_on__gt=post.created_on)
                Q(created_on__gt=post.created_on)
            ).order_by(
                'is_pinned', 'created_on'
            ).first()
        except:
            context['previous_post'] = None
        
        # Indicate this is the my post view
        context['is_my_post_view'] = True
        
        return context


# Category and Filtered Views
@login_required
def posts_by_category(request, category_id):
    category = get_object_or_404(Category, id=category_id, author=request.user)
    posts = Entry.objects.filter(
        author=request.user,
        category=category
    ).order_by('-is_pinned', '-updated_on')
    return render(request, 'entries/posts_by_category.html', {
        'category': category,
        'posts': posts
    })


@login_required
def pinned_posts(request):
    posts = Entry.objects.filter(
        author=request.user,
        is_pinned=True
    ).order_by('-updated_on')
    return render(request, 'entries/pinned_posts.html', {'posts': posts})


@login_required
def all_posts(request):
    """View all user's posts"""
    posts = Entry.objects.filter(
        author=request.user
    ).order_by('-created_on')
    return render(request, 'entries/all_posts.html', {'posts': posts})


@login_required
def custom_logout(request):
    """Custom logout view that handles GET requests"""
    logout(request)
    messages.success(request, 'You have been successfully logged out!')
    return redirect('entries:post_list')


def search_posts(request):
    """Search posts by title, content, category, and mood"""
    query = request.GET.get('q', '').strip()
    search_type = request.GET.get('type', 'public')  # 'public' or 'my_posts'
    
    if not query:
        if search_type == 'my_posts':
            return redirect('entries:my_posts')
        else:
            return redirect('entries:post_list')
    
    # Build the search query
    search_query = Q(title__icontains=query) | Q(content__icontains=query)
    
    if search_type == 'my_posts':
        # Search user's own posts
        if not request.user.is_authenticated:
            return redirect('login')
        
        posts = Entry.objects.filter(
            author=request.user
        ).filter(search_query).order_by('-is_pinned', '-created_on')
        
        # Also search by category name and mood
        category_posts = Entry.objects.filter(
            author=request.user,
            category__name__icontains=query
        ).order_by('-is_pinned', '-created_on')
        
        mood_posts = Entry.objects.filter(
            author=request.user,
            mood__icontains=query
        ).order_by('-is_pinned', '-created_on')
        
        # Combine all results and remove duplicates
        all_posts = list(posts) + list(category_posts) + list(mood_posts)
        seen_ids = set()
        unique_posts = []
        for post in all_posts:
            if post.id not in seen_ids:
                seen_ids.add(post.id)
                unique_posts.append(post)
        
        # Sort by pinned status and creation date
        unique_posts.sort(key=lambda x: (-x.is_pinned, -x.created_on.timestamp()))
        
        template_name = 'entries/search_results.html'
        context = {
            'posts': unique_posts,
            'query': query,
            'search_type': 'my_posts',
            'results_count': len(unique_posts)
        }
    else:
        # Search public posts
        posts = Entry.objects.filter(
            visibility='public'
        ).filter(search_query).order_by('-published_on', '-created_on')
        
        # Also search by category name and mood
        category_posts = Entry.objects.filter(
            visibility='public',
            category__name__icontains=query
        ).order_by('-published_on', '-created_on')
        
        mood_posts = Entry.objects.filter(
            visibility='public',
            mood__icontains=query
        ).order_by('-published_on', '-created_on')
        
        # Combine all results and remove duplicates
        all_posts = list(posts) + list(category_posts) + list(mood_posts)
        seen_ids = set()
        unique_posts = []
        for post in all_posts:
            if post.id not in seen_ids:
                seen_ids.add(post.id)
                unique_posts.append(post)
        
        # Sort by published date and creation date
        unique_posts.sort(key=lambda x: (-x.published_on.timestamp() if x.published_on else -x.created_on.timestamp(), -x.created_on.timestamp()))
        
        template_name = 'entries/search_results.html'
        context = {
            'posts': unique_posts,
            'query': query,
            'search_type': 'public',
            'results_count': len(unique_posts)
        }
    
    return render(request, template_name, context)


@login_required
def toggle_pin(request, pk):
    """Toggle pin status of a post"""
    post = get_object_or_404(Entry, pk=pk, author=request.user)
    
    # Toggle the pin status
    post.is_pinned = not post.is_pinned
    post.save()
    
    # Set appropriate message
    if post.is_pinned:
        messages.success(request, f'Post "{post.title}" has been pinned!')
    else:
        messages.success(request, f'Post "{post.title}" has been unpinned!')
    
    # Redirect back to the appropriate page
    # Check if we came from a specific page and redirect accordingly
    referer = request.META.get('HTTP_REFERER', '')
    
    if 'my-post' in referer:
        # We're on a post detail page, stay there
        return redirect('entries:my_post_detail', pk=pk)
    elif 'pinned' in referer:
        # We're on the pinned posts page
        return redirect('entries:pinned_posts')
    else:
        # Default to my posts list
        return redirect('entries:my_posts')
