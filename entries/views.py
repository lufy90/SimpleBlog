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
from .models import Entry, Category


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


class PostCreateView(LoginRequiredMixin, CreateView):
    model = Entry
    template_name = 'entries/post_form.html'
    fields = ['title', 'content', 'visibility', 'category', 'priority', 'is_pinned']
    
    def form_valid(self, form):
        form.instance.author = self.request.user
        if form.instance.visibility == 'public' and not form.instance.published_on:
            form.instance.published_on = timezone.now()
        messages.success(self.request, 'Post created successfully!')
        return super().form_valid(form)
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(author=self.request.user)
        return context


class PostUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Entry
    template_name = 'entries/post_form.html'
    fields = ['title', 'content', 'visibility', 'category', 'priority', 'is_pinned']
    
    def form_valid(self, form):
        if form.instance.visibility == 'public' and not form.instance.published_on:
            form.instance.published_on = timezone.now()
        messages.success(self.request, 'Post updated successfully!')
        return super().form_valid(form)
    
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
        ).order_by('-is_pinned', '-updated_on')


class MyPostDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Entry
    template_name = 'entries/post_detail.html'
    context_object_name = 'post'
    
    def test_func(self):
        entry = self.get_object()
        return self.request.user == entry.author


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
