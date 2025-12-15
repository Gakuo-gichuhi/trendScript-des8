from django.db import models
from blog.models import Blog  # If you want to link featured posts to your blog

class FeaturedPost(models.Model):
    blog_post = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name="monetize_featured_posts")
    headline = models.CharField(max_length=255, blank=True, help_text="Optional copywriting text")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.blog_post.title} - {'Active' if self.is_active else 'Inactive'}"


class AffiliateLink(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    description = models.TextField(blank=True, help_text="Write your copy here")
    image = models.ImageField(upload_to='affiliate_images/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title



class MonetizationSettings(models.Model):
    show_ads_globally = models.BooleanField(default=True)       # For any ads
    show_affiliate_globally = models.BooleanField(default=True) # For affiliate links
    site_owner_email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return "Monetization Settings"
