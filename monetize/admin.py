from django.contrib import admin
from .models import FeaturedPost, AffiliateLink

@admin.register(FeaturedPost)
class FeaturedPostAdmin(admin.ModelAdmin):
    list_display = ('blog_post', 'headline', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('blog_post__title', 'headline')


@admin.register(AffiliateLink)
class AffiliateLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'is_active', 'created_at')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description')
