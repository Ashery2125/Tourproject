from django import template
from django.contrib.auth import get_user_model

from tours_app.models import Booking, Destination, Trip

register = template.Library()


@register.simple_tag
def admin_count(model_name):
    """Small, safe counters used by the branded admin dashboard."""
    models = {
        'booking': Booking,
        'destination': Destination,
        'trip': Trip,
        'pending_booking': Booking,
        'user': get_user_model(),
    }
    model = models.get(model_name.lower())
    if not model:
        return 0
    if model_name.lower() == 'pending_booking':
        return Booking.objects.filter(status='PENDING').count()
    return model.objects.count()


@register.simple_tag
def recent_bookings(limit=4):
    return Booking.objects.select_related('trip').order_by('-created_at')[:limit]


@register.simple_tag
def recent_destinations(limit=3):
    return Destination.objects.order_by('-created_at')[:limit]
