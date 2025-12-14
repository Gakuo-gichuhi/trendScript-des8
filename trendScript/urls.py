from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from blog import views as blog_views

urlpatterns = [
    path('admin/', admin.site.urls),

    # Login / Logout
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),

    # Register
    path('register/', blog_views.register, name='register'),

    # Blog app
    path('', include('blog.urls', namespace='blog')),

    # Monetize app
    path('monetize/', include('monetize.urls', namespace='monetize')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
