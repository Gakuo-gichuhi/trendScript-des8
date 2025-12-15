from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django_quill.fields import QuillField
from django.core.exceptions import ValidationError
import re

# ===========================
# DAILY VISITORS MODEL
# ===========================
class DailyVisitor(models.Model):
    date = models.DateField(auto_now_add=True)
    count = models.IntegerField(default=0)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.date} — {self.count} visitors"


# ===========================
# BLOG MODEL
# ===========================
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name


CATEGORY_CHOICES = [
    ('politics', 'Politics'),
    ('sports', 'Sports'),
    ('education', 'Education'),
    ('culture', 'Culture'),
    ('economics', 'Economics'),
]

class Blog(models.Model):
    sno = models.AutoField(primary_key=True)
    Title = models.CharField(max_length=200)
    Content = QuillField()
    Slug = models.SlugField(max_length=200, unique=True)
    time = models.DateTimeField(auto_now_add=True)
    Image = models.ImageField(upload_to='blog_images/', default='default.jpg')
    Category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default='politics')
    overlay_text = models.CharField(max_length=200, blank=True, null=True)
    event_time = models.DateTimeField(blank=True, null=True)
    event_place = models.CharField(max_length=200, blank=True, null=True)
    short_description = models.TextField(blank=True, null=True)
    
    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.Title


# ===========================
# LIKE MODEL
# ===========================
class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='likes')
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'blog')

    def __str__(self):
        return f"{self.user.username} likes {self.blog.Title}"


# ===========================
# COMMENT MODEL
# ===========================
class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    content = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    def clean(self):
        url_pattern = r'(https?://|www\.)'
        if self.user.is_staff:
            return
        if re.search(url_pattern, self.content):
            raise ValidationError("Links are not allowed in comments.")

    def __str__(self):
        return f"Comment by {self.name} on {self.blog.Title}"


# ===========================
# CONTACT MESSAGE MODEL
# ===========================
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    message = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.email}"




class AffiliateLink(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    image = models.ImageField(upload_to="affiliate_images/", blank=True, null=True)
    active = models.BooleanField(default=True)
    
    position = models.CharField(
        max_length=50, 
        blank=True, 
        null=True, 
        help_text="Optional position for template placement (e.g., sidebar, footer, inpost)"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class FeaturedPost(models.Model):
    title = models.CharField(max_length=255)
    featured_image = models.ImageField(upload_to="featured_posts/", blank=True, null=True)
    blog_post = models.ForeignKey("Blog", on_delete=models.CASCADE, related_name="blog_featured_posts")  # assuming Blog model exists
    active = models.BooleanField(default=True)
    position = models.CharField(
        max_length=50, 
        blank=True, 
        null=True, 
        help_text="Optional position for template placement (e.g., sidebar, footer, inpost)"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return self.blog_post.get_absolute_url()
    
POSITION_CHOICES = [
    ('sidebar', 'Sidebar'),
    ('footer', 'Footer'),
    ('inpost', 'In Post'),
]

position = models.CharField(max_length=20, choices=POSITION_CHOICES)
active = models.BooleanField(default=True)

