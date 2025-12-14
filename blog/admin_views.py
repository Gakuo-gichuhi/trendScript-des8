from django.db.models import Count
from .models import Blog, Comment, Like, DailyVisitor
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render


@staff_member_required
def analytics_dashboard(request):
    # Analytics
    total_blogs = Blog.objects.count()
    total_comments = Comment.objects.count()
    total_likes = Like.objects.count()

    # Most liked
    most_liked = Blog.objects.annotate(like_count=Count('likes')).order_by('-like_count').first()
    most_liked_count = most_liked.like_count if most_liked else 0

    # Popularity chart
    popularity = Blog.objects.annotate(like_count=Count('likes')).order_by('-like_count')
    blog_titles = [b.Title for b in popularity]
    blog_likes = [b.like_count for b in popularity]

    # Visitors last 14 days
    visitors = DailyVisitor.objects.order_by('-date')[:14][::-1]
    visitor_dates = [v.date.strftime("%b %d") for v in visitors]
    visitor_counts = [v.count for v in visitors]

    return render(request, "analytics.html", {
        "total_blogs": total_blogs,
        "total_comments": total_comments,
        "total_likes": total_likes,
        "most_liked": most_liked,
        "most_liked_count": most_liked_count,
        "blog_titles": blog_titles,
        "blog_likes": blog_likes,
        "visitor_dates": visitor_dates,
        "visitor_counts": visitor_counts,
    })