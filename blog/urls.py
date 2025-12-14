from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from .admin_views import analytics_dashboard

app_name = "blog"

urlpatterns = [
    # Home & Blog
    path('', views.home, name='home'),
    path('blog/', views.blog, name='blog'),
    path('blog/<slug:slug>/like/', views.like_blog, name='like_blog'),
    path('blogpost/<slug:slug>/', views.blogpost, name='blogpost'),
    path('search/', views.search, name='search'),


    # AJAX endpoints
    path('blog/<slug:slug>/like/', views.like_blog, name='like_blog'),
    path('blog/<slug:slug>/comment/', views.post_comment, name='post_comment'),



    # Contact
    path('contact/', views.contact, name='contact'),

    # Authentication
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    # Admin Analytics
    path('admin/analytics/', analytics_dashboard, name='analytics_dashboard'),
]
