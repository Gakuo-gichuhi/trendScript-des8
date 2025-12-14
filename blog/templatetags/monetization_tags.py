from django import template
from blog.models import Advert
from monetize.models import MonetizationSettings

register = template.Library()

@register.inclusion_tag('monetize/_render_ads.html', takes_context=True)
def render_ads(context, position):
    # Get global ad settings
    settings = MonetizationSettings.objects.first()
    request = context.get('request')

    # If global ads are OFF → return empty
    if not settings or not settings.show_ads_globally:
        return {"ads": []}

    # Check if blog overrides ads (optional)
    blog = context.get('blog')
    if blog and hasattr(blog, 'show_ads') and not blog.show_ads:
        return {"ads": []}

    # Load active ads
    ads = [
        ad for ad in Advert.objects.filter(position=position, active=True)
        if hasattr(ad, "is_current") and ad.is_current()
    ]

    return {"ads": ads}
