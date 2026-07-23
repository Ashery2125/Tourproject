from django.contrib.admin.models import LogEntry
from django.contrib import admin
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Count, Sum
from django.shortcuts import render

from .models import Booking, Destination, Trip


staff_required = user_passes_test(lambda user: user.is_active and user.is_staff)


def admin_context(request, extra_context):
    context = admin.site.each_context(request)
    context.update(extra_context)
    return context


@staff_required
def reports(request):
    bookings_by_status = list(
        Booking.objects.values('status').annotate(total=Count('id')).order_by('status')
    )
    total_revenue = Booking.objects.exclude(status__in=['CANCELLED', 'DECLINED']).aggregate(
        total=Sum('total_price')
    )['total'] or 0
    context = admin_context(request, {
        'page_title': 'Reports',
        'page_subtitle': 'A live snapshot of your safari operations.',
        'booking_count': Booking.objects.count(),
        'trip_count': Trip.objects.count(),
        'destination_count': Destination.objects.count(),
        'total_revenue': total_revenue,
        'bookings_by_status': bookings_by_status,
        'top_trips': Trip.objects.annotate(booking_total=Count('bookings')).order_by('-booking_total', 'name')[:5],
    })
    return render(request, 'admin/reports.html', context)


@staff_required
def activity_logs(request):
    context = admin_context(request, {
        'page_title': 'Activity logs',
        'page_subtitle': 'Recent administrative activity in the command centre.',
        'entries': LogEntry.objects.select_related('user', 'content_type').order_by('-action_time')[:50],
    })
    return render(request, 'admin/activity_logs.html', context)


@staff_required
def help_support(request):
    return render(request, 'admin/help_support.html', admin_context(request, {
        'page_title': 'Help & support',
        'page_subtitle': 'A quick guide to managing WildVista Safari operations.',
    }))
