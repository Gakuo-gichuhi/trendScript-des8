from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login
from django.contrib import messages
from django.db.models import Q, Count
from django.utils import timezone
from .models import Blog, Comment, Like, DailyVisitor, ContactMessage
from django.contrib.auth.forms import UserCreationForm
from django.template.loader import render_to_string

# -------------------------
# Home Page
# -------------------------
def home(request):
    blogs = Blog.objects.order_by('-time')[:5]
    featured = blogs.first() if blogs.exists() else None
    trending = Blog.objects.annotate(num_likes=Count('likes')).order_by('-num_likes')[:5]
    
    return render(request, 'bloghome.html', {
        'blogs': blogs,
        'featured': featured,
        'trending': trending,
        
    })

# -------------------------
# Blog Listing Page
# -------------------------
def blog(request):
    blogs = Blog.objects.order_by('-time')
    trending = Blog.objects.annotate(num_likes=Count('likes')).order_by('-num_likes')[:5]
    return render(request, 'blog_list.html', {
        'blogs': blogs,
        'trending': trending,
    })

# -------------------------
# Single Blog Post
# -------------------------
def blogpost(request, slug):
    blog = get_object_or_404(Blog, Slug=slug)
    comments = blog.comments.all().order_by('-time')

    # Track daily visitors
    visitor, created = DailyVisitor.objects.get_or_create(date=timezone.now().date())
    visitor.count += 1
    visitor.save()

    return render(request, 'blogpost.html', {
        'blog': blog,
        'comments': comments
    })

# -------------------------
# Like Blog (AJAX)
# -------------------------
@login_required
def like_blog(request, slug):
    if request.method != 'POST':
        return JsonResponse({'error': 'Invalid request'}, status=400)

    blog = get_object_or_404(Blog, Slug=slug)
    like_obj, created = Like.objects.get_or_create(user=request.user, blog=blog)

    if not created:
        like_obj.delete()
        liked = False
    else:
        liked = True

    return JsonResponse({
        'liked': liked,
        'likes': blog.likes.count()
    })

# -------------------------
# Post Comment (AJAX)
# -------------------------
@login_required
def post_comment(request, slug):
    if request.method != 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid request'}, status=400)

    blog = get_object_or_404(Blog, Slug=slug)
    content = request.POST.get('comment', '').strip()

    if not content:
        return JsonResponse({'success': False, 'error': 'Comment cannot be empty'}, status=400)

    comment = Comment.objects.create(
        blog=blog,
        user=request.user,
        content=content,
        time=timezone.now()
    )

    comment_html = render_to_string('partials/_single_comment.html', {'comment': comment})
    return JsonResponse({'success': True, 'comment_html': comment_html})

# -------------------------
# Search
# -------------------------
def search(request):
    query = request.GET.get('q', '').strip()
    blogs = Blog.objects.none()
    if query:
        blogs = Blog.objects.filter(
            Q(Title__icontains=query) |
            Q(Content__icontains=query) |
            Q(short_description__icontains=query)
        ).distinct()
    trending = Blog.objects.annotate(num_likes=Count('likes')).order_by('-num_likes')[:5]

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.GET.get('ajax') == '1':
        html = render_to_string('partials/_search_results.html', {
            'results': blogs,
            'query': query
        })
        return JsonResponse({'html': html})

    return render(request, 'search.html', {
        'blogs': blogs,
        'query': query,
        'trending': trending
    })

# -------------------------
# Contact Form
# -------------------------
def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        ContactMessage.objects.create(name=name, email=email, message=message)
        messages.success(request, "Your message has been submitted!")
        return redirect('blog:contact')
    return render(request, 'contact.html')

# -------------------------
# User Registration
# -------------------------
def register(request):
    form = UserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        login(request, user)
        messages.success(request, "Account created successfully!")
        return redirect('blog:home')
    return render(request, 'register.html', {'form': form})
