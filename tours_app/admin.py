from django.contrib import admin
from .models import Destination, Trip, Booking, SiteAppearance


# Brand the built-in Django admin without changing its URLs or permissions.
admin.site.site_header = 'WILDVISTA SAFARI COMMAND CENTRE'
admin.site.site_title = 'WildVista Admin'
admin.site.index_title = 'Safari operations overview'
admin.site.index_template = 'admin/index.html'


class ActivityLogAdmin(admin.ModelAdmin):
    """Read-only audit trail used from the command-centre navigation."""

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(SiteAppearance)
class SiteAppearanceAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'hero_badge')
    fields = ('hero_video_url', 'hero_poster_url', 'hero_badge')

    def has_add_permission(self, request):
        return not SiteAppearance.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('name', 'location', 'is_featured', 'image_remote_url', 'created_at')
    search_fields = ('name', 'location')
    list_filter = ('is_featured',)
    fields = ('name', 'location', 'description', 'is_featured', 'image', 'image_remote_url')

@admin.register(Trip)
class TripAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date', 'end_date', 'price_per_person', 'price_per_day', 'is_offer', 'discount_price', 'total_seats', 'available_seats', 'image_remote_url', 'is_active', 'is_full')
    search_fields = ('name', 'description')
    list_filter = ('is_active', 'is_full', 'is_offer', 'trip_type', 'start_date')
    filter_horizontal = ('destinations',)
    fieldsets = (
        ('Trip details', {
            'fields': ('name', 'description', 'destinations', 'trip_type', 'start_date', 'end_date', 'duration_days')
        }),
        ('Pricing and seats', {
            'fields': ('currency', 'price_per_person', 'price_per_day', 'is_offer', 'discount_price', 'total_seats', 'available_seats')
        }),
        ('Pickup and inclusions', {
            'fields': ('international_pickup', 'local_pickup', 'pickup_location', 'includes_airport_pickup', 'includes_accommodation', 'includes_meals', 'includes_transport')
        }),
        ('Media and visibility', {
            'fields': ('image', 'image_remote_url', 'is_active', 'is_full')
        }),
    )

@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'trip', 'tourist_type', 'pickup_point', 'number_of_seats', 'total_price', 'status', 'created_at')
    search_fields = ('full_name', 'email', 'phone_number')
    list_filter = ('status', 'tourist_type', 'created_at')
    readonly_fields = ('total_price', 'created_at', 'updated_at')
    actions = ('approve_bookings', 'decline_bookings')

    def save_model(self, request, obj, form, change):
        old_status = None
        if change and obj.pk:
            old_status = Booking.objects.get(pk=obj.pk).status
        super().save_model(request, obj, form, change)
        if old_status and old_status != obj.status:
            if obj.status == 'CONFIRMED':
                obj.send_confirmation_email()
            elif obj.status == 'DECLINED':
                obj.send_status_email('declined')

    def approve_bookings(self, request, queryset):
        updated = 0
        for booking in queryset.filter(status='PENDING'):
            booking.confirm()
            updated += 1
        self.message_user(request, f'{updated} booking request(s) confirmed.')
    approve_bookings.short_description = 'Approve selected booking requests'

    def decline_bookings(self, request, queryset):
        declined = 0
        for booking in queryset.filter(status='PENDING'):
            booking.decline()
            declined += 1
        self.message_user(request, f'{declined} booking request(s) declined.')
    decline_bookings.short_description = 'Decline selected booking requests'
