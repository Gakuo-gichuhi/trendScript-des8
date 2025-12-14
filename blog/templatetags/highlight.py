# blog/templatetags/highlight.py

from django import template
from django.utils.html import strip_tags
from django.utils.safestring import mark_safe
import re

register = template.Library()

@register.filter(name='highlight')
def highlight(text, search_query):
    if not search_query or not text:
        return text

    plain = strip_tags(str(text))
    words = [w.strip() for w in search_query.split() if w.strip()]
    if not words:
        return plain

    words_sorted = sorted(words, key=len, reverse=True)
    highlighted = plain

    colors = ['#FFEAA7', '#FAB1A0', '#A29BFE', '#74B9FF', '#81ECEC', '#FF7675']
    for i, word in enumerate(words_sorted):
        pattern = re.compile(f"({re.escape(word)})", re.IGNORECASE)
        color = colors[i % len(colors)]
        highlighted = pattern.sub(
            f'<mark style="background:{color}; padding:0 5px; border-radius:5px;">\\1</mark>',
            highlighted
        )

    return mark_safe(highlighted)