# monetize/templatetags/monetize_tags.py
from django import template
from monetize.models import FeaturedPost, AffiliateLink

register = template.Library()

@register.inclusion_tag("monetize/featured_posts.html")
def featured_posts():
    return {
        "featured_posts": FeaturedPost.objects.filter(is_active=True)
    }

@register.inclusion_tag("monetize/affiliate_links.html")
def affiliate_links():
    return {
        "affiliate_links": AffiliateLink.objects.filter(is_active=True)
    }
