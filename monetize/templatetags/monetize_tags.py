from django import template
from monetize.models import FeaturedPost, AffiliateLink, MonetizationSettings

register = template.Library()

@register.inclusion_tag("monetize/includes/featured_posts.html")
def show_featured_posts(limit=20):
    return {"featured_posts": FeaturedPost.objects.filter(is_active=True)[:limit]}

@register.inclusion_tag("monetize/includes/affiliate_links.html")
def show_affiliate_links(limit=20):
    return {"affiliate_links": AffiliateLink.objects.filter(is_active=True)[:limit]}

@register.inclusion_tag("monetize/includes/ads.html")
def show_ads():
    # If you have generic ads, create a model or static HTML block
    return {}

@register.inclusion_tag("monetize/ads.html")
def show_ads():
    from monetize.models import Ad  # assuming you have an Ad model
    return {"ads": Ad.objects.filter(is_active=True)}
