from django.contrib.auth.models import User
from django.core import mail
from django.test import TestCase, override_settings

from .models import Booking, Destination, Trip


class EmailWorkflowTests(TestCase):
    @override_settings(
        EMAIL_BACKEND='django.core.mail.backends.locmem.EmailBackend',
        ADMIN_NOTIFICATION_EMAILS=['configured@example.com'],
    )
    def test_admin_notification_and_confirmation_emails_are_sent_for_booking_workflow(self):
        admin_user = User.objects.create_user(
            username='admin1',
            email='admin1@example.com',
            password='testpass123',
            is_staff=True,
        )
        another_admin = User.objects.create_user(
            username='admin2',
            email='admin2@example.com',
            password='testpass123',
            is_staff=True,
        )
        guest_user = User.objects.create_user(
            username='guest',
            email='guest@example.com',
            password='testpass123',
        )

        destination = Destination.objects.create(
            name='Arusha',
            description='A place to test.',
            location='Arusha',
        )
        trip = Trip.objects.create(
            name='Test Safari',
            description='A test trip',
            start_date='2026-01-01',
            end_date='2026-01-03',
            duration_days=2,
            price_per_person=300,
            price_per_day=300,
            total_seats=10,
            available_seats=10,
        )
        trip.destinations.add(destination)

        booking = Booking.objects.create(
            user=guest_user,
            trip=trip,
            full_name='Guest User',
            email='guest@example.com',
            phone_number='255700000000',
            number_of_seats=1,
            total_price=600,
        )

        recipients = booking.admin_notification_recipients()
        self.assertIn('configured@example.com', recipients)
        self.assertIn(admin_user.email, recipients)
        self.assertIn(another_admin.email, recipients)

        sent_count = booking.send_admin_notification_email()
        self.assertGreaterEqual(sent_count, 1)

        booking.status = 'PENDING'
        booking.confirm()

        self.assertEqual(len(mail.outbox), 2)
        self.assertIn('New WildVista booking request', mail.outbox[0].subject)
        self.assertIn('booking confirmed', mail.outbox[1].subject.lower())
