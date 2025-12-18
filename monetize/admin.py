from django.contrib import admin
from django.utils.html import format_html
from .models import FeaturedPost, AffiliateLink, Ad

@admin.register(FeaturedPost)
class FeaturedPostAdmin(admin.ModelAdmin):
    list_display = ('blog_post', 'headline', 'is_active', 'created_at', 'thumbnail')
    list_filter = ('is_active', 'created_at')
    search_fields = ('blog_post__Title', 'headline')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

    def thumbnail(self, obj):
        if obj.blog_post.Image:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit:cover;border-radius:4px;" />',
                obj.blog_post.Image.url
            )
        return "-"
    thumbnail.short_description = "Image"


@admin.register(AffiliateLink)
class AffiliateLinkAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'is_active', 'created_at', 'thumbnail')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title', 'description')
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

    def thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit:cover;border-radius:4px;" />',
                obj.image.url
            )
        return "-"
    thumbnail.short_description = "Image"


@admin.register(Ad)
class AdAdmin(admin.ModelAdmin):
    list_display = ('title', 'url', 'is_active', 'created_at', 'thumbnail')
    list_filter = ('is_active', 'created_at')
    search_fields = ('title',)
    readonly_fields = ('created_at',)
    ordering = ('-created_at',)

    def thumbnail(self, obj):
        if obj.image:
            return format_html(
                '<img src="{}" width="50" height="50" style="object-fit:cover;border-radius:4px;" />',
                obj.image.url
            )
        return "-"
    thumbnail.short_description = "Image"
