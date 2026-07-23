from django import template
from django.utils import timezone

register = template.Library()

@register.filter
def days_until(value):
    if not value:
        return ''
    delta = value - timezone.now().date()
    days = delta.days
    if days < 0:
        return 'Past'
    elif days == 0:
        return 'Today'
    elif days == 1:
        return 'Tomorrow'
    else:
        return f'{days} days'

@register.filter
def status_badge(value):
    badges = {
        'PENDING': 'warning',
        'CONFIRMED': 'success',
        'CANCELLED': 'danger',
        'COMPLETED': 'secondary',
    }
    return badges.get(value, 'secondary')