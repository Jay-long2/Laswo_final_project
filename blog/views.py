from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Count, F, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .models import Category, NewsletterSubscriber, Post, Tag


def post_list(request):
    posts_list = Post.objects.filter(status='published').select_related('author', 'category')

    category_slug = request.GET.get('category')
    tag_slug = request.GET.get('tag')
    query = request.GET.get('q')

    if category_slug:
        posts_list = posts_list.filter(category__slug=category_slug)
    if tag_slug:
        posts_list = posts_list.filter(tags__slug=tag_slug)
    if query:
        posts_list = posts_list.filter(
            Q(title__icontains=query)
            | Q(excerpt__icontains=query)
            | Q(content__icontains=query)
        )

    paginator = Paginator(posts_list, 6)
    posts = paginator.get_page(request.GET.get('page'))

    context = {
        'posts': posts,
        'categories': Category.objects.annotate(post_count=Count('posts')),
        'active_category': category_slug or '',
        'active_tag': tag_slug or '',
        'query': query or '',
    }
    return render(request, 'blog/list.html', context)


def category_detail(request, slug):
    """Categories are shown as a filter on the list page."""
    category = get_object_or_404(Category, slug=slug)
    return redirect(f"{reverse('blog:list')}?category={category.slug}")


def tag_detail(request, slug):
    """Tags are shown as a filter on the list page."""
    tag = get_object_or_404(Tag, slug=slug)
    return redirect(f"{reverse('blog:list')}?tag={tag.slug}")


def post_detail(request, slug):
    post = get_object_or_404(
        Post.objects.select_related('author', 'category'), slug=slug, status='published'
    )

    # Atomic bump: avoids the lost-update race and leaves updated_at alone.
    Post.objects.filter(pk=post.pk).update(view_count=F('view_count') + 1)

    context = {
        'post': post,
        'related_posts': Post.objects.filter(
            category=post.category, status='published'
        ).exclude(pk=post.pk)[:3],
        'comments': post.comments.filter(is_approved=True),
    }
    return render(request, 'blog/detail.html', context)


def add_comment(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')

    if request.method == 'POST':
        # Honeypot: bots fill every field, people never see this one.
        if request.POST.get('website'):
            return redirect(post)

        name = (request.POST.get('name') or '').strip()
        email = (request.POST.get('email') or '').strip()
        content = (request.POST.get('content') or '').strip()

        if name and email and content:
            post.comments.create(name=name, email=email, content=content)
            messages.success(request, 'Thank you. Your comment will appear once approved.')
        else:
            messages.error(request, 'Please fill in your name, email and comment.')

    return redirect(post)


def newsletter_subscribe(request):
    if request.method == 'POST':
        email = (request.POST.get('email') or '').strip()
        if email:
            NewsletterSubscriber.objects.get_or_create(
                email=email, defaults={'is_active': True}
            )
            messages.success(request, 'You are subscribed. Thank you.')
        else:
            messages.error(request, 'Please enter a valid email address.')

    # Never redirect to a user-supplied header - that is an open redirect.
    return redirect('blog:list')
