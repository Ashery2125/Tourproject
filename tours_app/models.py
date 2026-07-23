from decimal import Decimal

from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
from django.urls import reverse


class SiteAppearance(models.Model):
    """A single editable source for homepage media and the main message."""
    SAMPLE_HERO_VIDEO_URL = 'https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4'
    SAMPLE_HERO_POSTER_URL = '/static/tours_app/images/wildfinder-logo.svg'

    hero_video_url = models.URLField(
        blank=True,
        help_text='Direct MP4 URL used behind the homepage heading. Leave empty to use the sample safari video.'
    )
    hero_poster_url = models.URLField(
        blank=True,
        help_text='Fallback image shown while the video loads or when video is unavailable. Leave empty to use the sample poster.'
    )
    hero_badge = models.CharField(max_length=100, default='Tanzania safari journeys')

    class Meta:
        verbose_name = 'Site appearance'
        verbose_name_plural = 'Site appearance'

    def __str__(self):
        return 'Homepage media & brand copy'

class Destination(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    location = models.CharField(max_length=200)
    image = models.ImageField(upload_to='destinations/', blank=True, null=True)
    image_remote_url = models.URLField(blank=True, null=True)
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    DEFAULT_IMAGE_URL = 'https://images.unsplash.com/photo-1536684182010-56c43846dfa7?auto=format&fit=crop&w=1200&q=80'

    @property
    def image_url(self):
        # Prefer remote URL when present (force remote assets over uploads)
        if self.image_remote_url:
            return self.image_remote_url
        if self.image:
            return self.image.url
        return self.DEFAULT_IMAGE_URL

    def __str__(self):
        return self.name

class Trip(models.Model):
    TRIP_TYPES = [
        ('GROUP', 'Group Trip'),
        ('PRIVATE', 'Private Trip'),
        ('CUSTOM', 'Custom Trip'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    destinations = models.ManyToManyField(Destination, related_name='trips')
    trip_type = models.CharField(max_length=10, choices=TRIP_TYPES, default='GROUP')
    start_date = models.DateField()
    end_date = models.DateField()
    duration_days = models.IntegerField()
    price_per_person = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    price_per_day = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    is_offer = models.BooleanField(default=False)
    discount_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=3, default='USD')
    international_pickup = models.CharField(max_length=200, default='Kilimanjaro International Airport - KIA')
    local_pickup = models.CharField(max_length=200, default='Arusha Town/Central Hotels')
    total_seats = models.IntegerField(default=10, validators=[MinValueValidator(1)])
    available_seats = models.IntegerField(default=10, validators=[MinValueValidator(0)])
    includes_airport_pickup = models.BooleanField(default=True)
    pickup_location = models.CharField(max_length=200, default='KIA Airport, Arusha')
    includes_accommodation = models.BooleanField(default=True)
    includes_meals = models.BooleanField(default=True)
    includes_transport = models.BooleanField(default=True)
    image = models.ImageField(upload_to='trips/', blank=True, null=True)
    image_remote_url = models.URLField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_full = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    DEFAULT_IMAGE_URL = 'https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1200&q=80'

    @property
    def image_url(self):
        # Prefer remote URL when present (force remote assets over uploads)
        if self.image_remote_url:
            return self.image_remote_url
        if self.image:
            return self.image.url
        return self.DEFAULT_IMAGE_URL

    def __str__(self):
        return f"{self.name} - {self.start_date}"

    @property
    def active_price(self):
        if self.is_offer and self.discount_price:
            return self.discount_price
        return self.price_per_day or self.price_per_person

    @property
    def original_price(self):
        return self.price_per_day or self.price_per_person

    def save(self, *args, **kwargs):
        if self.available_seats <= 0:
            self.is_full = True
        else:
            self.is_full = False
        super().save(*args, **kwargs)

    @property
    def is_past(self):
        return self.end_date < timezone.now().date()

class Booking(models.Model):
    TOURIST_TYPE = [
        ('LOCAL', 'Local (Tanzanian)'),
        ('INTERNATIONAL', 'International'),
    ]

    PICKUP_CHOICES = [
        ('KIA Airport - KIA', 'Kilimanjaro International Airport - KIA'),
        ('Arusha Town/Central Hotels', 'Arusha Town/Central Hotels'),
        ('Arusha City/Clocktower', 'Arusha City/Clocktower'),
    ]
    
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('CONFIRMED', 'Confirmed'),
        ('DECLINED', 'Declined'),
        ('CANCELLED', 'Cancelled'),
        ('COMPLETED', 'Completed'),
    ]
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='bookings')
    trip = models.ForeignKey(Trip, on_delete=models.CASCADE, related_name='bookings')
    tourist_type = models.CharField(max_length=20, choices=TOURIST_TYPE, default='INTERNATIONAL')
    pickup_point = models.CharField(max_length=200, choices=PICKUP_CHOICES, blank=True, null=True)
    full_name = models.CharField(max_length=200)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    number_of_seats = models.IntegerField(default=1, validators=[MinValueValidator(1)])
    special_requests = models.TextField(blank=True)
    needs_airport_pickup = models.BooleanField(default=False)
    flight_number = models.CharField(max_length=20, blank=True)
    arrival_time = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='PENDING')
    total_price = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.full_name} - {self.trip.name}"

    @property
    def reserves_seats(self):
        return self.status in {'PENDING', 'CONFIRMED', 'COMPLETED'}

    def clean(self):
        super().clean()
        if not self.trip_id or not self.reserves_seats:
            return

        old_reserved_seats = 0
        if self.pk:
            try:
                old_booking = Booking.objects.get(pk=self.pk)
            except Booking.DoesNotExist:
                old_booking = None
            if old_booking and old_booking.status in {'PENDING', 'CONFIRMED', 'COMPLETED'}:
                old_reserved_seats = old_booking.number_of_seats

        requested_extra_seats = self.number_of_seats - old_reserved_seats
        if requested_extra_seats > self.trip.available_seats:
            raise ValidationError({
                'number_of_seats': f'Only {self.trip.available_seats} seats are available for this trip.'
            })

    def save(self, *args, **kwargs):
        base_price = self.trip.active_price
        duration = max(self.trip.duration_days, 1)
        self.total_price = base_price * duration * self.number_of_seats
        self.full_clean()

        old_reserved_seats = 0
        if self.pk:
            old_booking = Booking.objects.get(pk=self.pk)
            if old_booking.status in {'PENDING', 'CONFIRMED', 'COMPLETED'}:
                old_reserved_seats = old_booking.number_of_seats

        new_reserved_seats = self.number_of_seats if self.reserves_seats else 0
        seat_diff = new_reserved_seats - old_reserved_seats
        if seat_diff:
            self.trip.available_seats -= seat_diff
        self.trip.save()
        super().save(*args, **kwargs)

    def cancel(self):
        if self.status == 'CANCELLED':
            return
        old_status = self.status
        self.status = 'CANCELLED'
        self.save()
        if old_status in {'PENDING', 'CONFIRMED', 'COMPLETED'}:
            self.send_status_email('cancelled')

    def decline(self):
        if self.status == 'DECLINED':
            return
        old_status = self.status
        self.status = 'DECLINED'
        self.save()
        if old_status in {'PENDING', 'CONFIRMED'}:
            self.send_status_email('declined')

    def confirm(self):
        self.status = 'CONFIRMED'
        self.save()
        self.send_confirmation_email()

    def admin_change_url(self, request=None):
        path = reverse('admin:tours_app_booking_change', args=[self.pk])
        if request:
            return request.build_absolute_uri(path)
        return path

    def public_booking_url(self, request=None):
        path = reverse('my_bookings')
        if request:
            return request.build_absolute_uri(path)
        return path

    def admin_notification_recipients(self):
        from django.conf import settings

        configured_emails = getattr(settings, 'ADMIN_NOTIFICATION_EMAILS', [])
        staff_emails = User.objects.filter(
            is_staff=True,
            is_active=True,
            email__isnull=False,
        ).exclude(email='').values_list('email', flat=True)
        return list(dict.fromkeys([*configured_emails, *staff_emails]))

    def send_admin_notification_email(self, request=None):
        from django.core.mail import send_mail
        from django.conf import settings

        recipients = self.admin_notification_recipients()
        if not recipients:
            return 0

        subject = f'New WildVista booking request #{self.id}'
        message = (
            'Hello Safari Admin,\n\n'
            'A new booking request has been submitted and is waiting for review.\n\n'
            f'Booking ID: #{self.id}\n'
            f'Customer: {self.full_name}\n'
            f'Email: {self.email}\n'
            f'Phone: {self.phone_number}\n'
            f'Trip: {self.trip.name}\n'
            f'Tourist type: {self.get_tourist_type_display()}\n'
            f'Seats: {self.number_of_seats}\n\n'
            f'Total: {self.total_price} {self.trip.currency}\n'
            f'Pickup: {self.pickup_point or "Not specified"}\n'
            f'Special requests: {self.special_requests or "None"}\n\n'
            f'Open this request in admin: {self.admin_change_url(request)}\n\n'
            'Please log in and approve or reject the request.'
        )
        return send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            recipients,
            fail_silently=True,
        )

    def send_status_email(self, status_label):
        from django.core.mail import send_mail
        from django.conf import settings

        if status_label == 'declined':
            subject = f'WildVista Safaris booking declined - #{self.id}'
            message = (
                f'Hello {self.full_name},\n\n'
                f'Your booking request for {self.trip.name} was not approved at this time.\n'
                'You can choose another available safari date/trip or contact us for help arranging a custom option.\n\n'
                'Contact: wildvistasafaris@gmail.com | +255 794 872 433\n\n'
                'Thank you for choosing WildVista Safaris.'
            )
        else:
            subject = f'WildVista Safaris booking {status_label} - #{self.id}'
            message = (
                f'Hello {self.full_name},\n\n'
                f'Your booking for {self.trip.name} has been {status_label}.\n'
                f'Seats: {self.number_of_seats}\n\n'
                'For questions, contact wildvistasafaris@gmail.com or +255 794 872 433.\n\n'
                'Thank you for choosing WildVista Safaris.'
            )
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [self.email],
            fail_silently=True,
        )

    def send_confirmation_email(self):
        from django.core.mail import send_mail
        from django.conf import settings

        subject = f'WildVista Safaris booking confirmed - #{self.id}'
        message = (
            f'Hello {self.full_name},\n\n'
            f'Good news, your booking for {self.trip.name} has been approved.\n\n'
            f'Pickup: {self.pickup_point or "Not specified"}\n'
            f'Seats: {self.number_of_seats}\n'
            f'Total: {self.total_price} {self.trip.currency}\n'
            f'Trip dates: {self.trip.start_date} to {self.trip.end_date}\n\n'
            'Next steps:\n'
            '1. Keep this email as your booking confirmation.\n'
            '2. Our team will contact you with payment and arrival instructions.\n'
            '3. Bring your passport/ID and share flight details if you need airport pickup.\n\n'
            'Contact: wildvistasafaris@gmail.com | +255 794 872 433\n\n'
            'Thank you for choosing WildVista Safaris.\n'
            'We look forward to welcoming you on safari!'
        )
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [self.email],
            fail_silently=True,
        )
