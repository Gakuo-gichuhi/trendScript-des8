from django.urls import path
from . import views

app_name = "monetize"



urlpatterns = [
    path('featured-posts/', views.featured_posts_view, name='featured_posts'),
    path('affiliate-links/', views.affiliate_links_view, name='affiliate_links'),
]
