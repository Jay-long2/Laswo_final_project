from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Count, Q
from django.core.paginator import Paginator
from .models import Post, Category, Tag, Comment, NewsletterSubscriber

# Create your views here.
def post_list(request):
    posts_list = Post.objects.filter(status='published').select_related('author', 'category')
    
    # Get filter parameters
    category_slug = request.GET.get('category')
    tag_slug = request.GET.get('tag')
    query = request.GET.get('q')
    
    if category_slug:
        posts_list = posts_list.filter(category__slug=category_slug)
    if tag_slug:
        posts_list = posts_list.filter(tags__slug=tag_slug)
    if query:
        posts_list = posts_list.filter(
            Q(title__icontains=query) |
            Q(excerpt__icontains=query) |
            Q(content__icontains=query)
        )
    
    # Pagination
    paginator = Paginator(posts_list, 6)  # 6 posts per page
    page_number = request.GET.get('page')
    posts = paginator.get_page(page_number)
    
    categories = Category.objects.annotate(post_count=Count('posts'))
    featured_posts = Post.objects.filter(status='published', is_featured=True)[:3]
    recent_posts = Post.objects.filter(status='published').exclude(id__in=[p.id for p in featured_posts])[:5]
    
    context = {
        'posts': posts,
        'featured_posts': featured_posts,
        'recent_posts': recent_posts,
        'categories': categories,
        'active_filters': {
            'category': category_slug,
            'tag': tag_slug,
            'query': query,
        }
    }
    return render(request, 'blog/list.html', context)

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    
    # Increment view count
    post.view_count += 1
    post.save()
    
    # Get related posts (same category, excluding current post)
    related_posts = Post.objects.filter(
        category=post.category,
        status='published'
    ).exclude(id=post.id)[:3]
    
    # Get approved comments
    comments = post.comments.filter(is_approved=True)
    
    context = {
        'post': post,
        'related_posts': related_posts,
        'comments': comments,
    }
    return render(request, 'blog/detail.html', context)

def category_detail(request, slug):
    category = get_object_or_404(Category, slug=slug)
    posts = Post.objects.filter(category=category, status='published')
    
    context = {
        'category': category,
        'posts': posts,
    }
    return render(request, 'blog/category.html', context)

def tag_detail(request, slug):
    tag = get_object_or_404(Tag, slug=slug)
    posts = Post.objects.filter(tags=tag, status='published')
    
    context = {
        'tag': tag,
        'posts': posts,
    }
    return render(request, 'blog/tag.html', context)

def add_comment(request, slug):
    if request.method == 'POST':
        post = get_object_or_404(Post, slug=slug)
        name = request.POST.get('name')
        email = request.POST.get('email')
        website = request.POST.get('website', '')
        content = request.POST.get('content')
        
        if name and email and content:
            Comment.objects.create(
                post=post,
                name=name,
                email=email,
                website=website,
                content=content
            )
            # In a real app, you might want to send an email notification here
        
    return redirect('blog:detail', slug=slug)

def newsletter_subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        if email:
            NewsletterSubscriber.objects.get_or_create(
                email=email,
                defaults={'is_active': True}
            )
            # In a real app, you might want to send a welcome email here
    
    return redirect(request.META.get('HTTP_REFERER', 'blog:list'))