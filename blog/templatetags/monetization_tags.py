from django import template
from monetize.models import MonetizationSettings
from blog.models import AffiliateLink, FeaturedPost

register = template.Library()

# Map content types to models
CONTENT_MODELS = {
    'affiliate': AffiliateLink,
    'featured': FeaturedPost,
}

@register.inclusion_tag('monetize/_render_ads.html', takes_context=True)
def render_ads(context, position, content_type='affiliate'):
    """
    Render content (ads, affiliate links, featured posts) by position.
    
    Usage in templates:
        {% render_ads "sidebar" "affiliate" %}
        {% render_ads "footer" "featured" %}
    """
    # Global settings
    settings = MonetizationSettings.objects.first()
    if not settings or not settings.show_ads_globally:
        return {"items": []}

    # Optional: check if current blog disables ads
    blog = context.get('blog')
    if blog and hasattr(blog, 'show_ads') and not blog.show_ads:
        return {"items": []}

    # Determine model to use
    model = CONTENT_MODELS.get(content_type)
    if not model:
        return {"items": []}

    # Load active items filtered by position
    items = model.objects.filter(active=True, position=position)

    return {"items": items}
