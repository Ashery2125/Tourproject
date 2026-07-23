from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone
from django.contrib.auth import get_user_model

from tours_app.models import Destination, Trip, SiteAppearance


class Command(BaseCommand):
    help = 'Seed the database with sample WildVista Safaris destinations, trips, and homepage media.'

    def handle(self, *args, **options):
        today = timezone.now().date()

        appearance_defaults = {
            'hero_video_url': 'https://interactive-examples.mdn.mozilla.net/media/cc0-videos/flower.mp4',
            'hero_poster_url': '/static/tours_app/images/wildfinder-logo.svg',
            'hero_badge': 'Arusha safari journeys',
        }
        appearance, created = SiteAppearance.objects.get_or_create(pk=1, defaults=appearance_defaults)
        if not created:
            for field, value in appearance_defaults.items():
                setattr(appearance, field, value)
            appearance.save()
        self.stdout.write(self.style.SUCCESS('Homepage appearance seeded.'))

        destinations = [
            {
                'name': 'Arusha National Park',
                'location': 'Arusha, Tanzania',
                'description': 'A compact wildlife gem with giraffes, zebras, black-and-white colobus monkeys and stunning views of Mount Meru.',
                'image_remote_url': 'https://images.unsplash.com/photo-1516426122078-c23e76319801?auto=format&fit=crop&w=1200&q=85',
            },
            {
                'name': 'Lake Duluti',
                'location': 'Arusha, Tanzania',
                'description': 'A quiet lakefront escape near Arusha, perfect for canoeing, birdwatching and peaceful resort stays.',
                'image_remote_url': 'https://images.unsplash.com/photo-1547970810-dc1eac37d174?auto=format&fit=crop&w=1200&q=85',
            },
            {
                'name': 'Mount Meru',
                'location': 'Arusha, Tanzania',
                'description': 'An iconic volcano climb and scenic adventure ideal for travelers seeking a premium outdoor experience.',
                'image_remote_url': 'https://images.unsplash.com/photo-1519167758481-83f29c2a7f78?auto=format&fit=crop&w=1200&q=85',
            },
            {
                'name': 'Arusha City Hotels & Lodges',
                'location': 'Arusha Town',
                'description': 'Curated boutique stays, serviced apartments and welcoming lodges near the city centre.',
                'image_remote_url': 'https://images.unsplash.com/photo-1523805009345-7448845a9e53?auto=format&fit=crop&w=1200&q=85',
            },
            {
                'name': 'Coffee Farm Experience',
                'location': 'Arusha Region',
                'description': 'A local cultural highlight featuring coffee tasting tours and authentic community hospitality.',
                'image_remote_url': 'https://images.unsplash.com/photo-1504432842672-1a79f78e4084?auto=format&fit=crop&w=1200&q=85',
            },
            {
                'name': 'Cultural Heritage Trails',
                'location': 'Arusha, Tanzania',
                'description': 'Explore Maasai-inspired heritage, local markets and authentic village experiences close to town.',
                'image_remote_url': 'https://images.unsplash.com/photo-1586861635167-e5223aadc9fe?auto=format&fit=crop&w=1200&q=85',
            },
        ]

        created_destinations = []
        for dest_data in destinations:
            dest, _ = Destination.objects.update_or_create(
                name=dest_data['name'],
                defaults={
                    'location': dest_data['location'],
                    'description': dest_data['description'],
                    'image_remote_url': dest_data['image_remote_url'],
                    'is_featured': len(created_destinations) < 4,
                }
            )
            created_destinations.append(dest)
        self.stdout.write(self.style.SUCCESS(f'Created {len(created_destinations)} destinations.'))

        trips = [
            {
                'name': 'Arusha City Safari Escape',
                'description': 'Begin your Arusha adventure with a city welcome, lodge check-in and a quick wildlife circuit around the national park.',
                'trip_type': 'GROUP',
                'start_date': today + timedelta(days=14),
                'end_date': today + timedelta(days=18),
                'duration_days': 5,
                'price_per_day': 310.00,
                'price_per_person': 310.00,
                'is_offer': True,
                'discount_price': 280.00,
                'currency': 'USD',
                'total_seats': 14,
                'available_seats': 12,
                'pickup_location': 'KIA Airport, Arusha',
                'image_remote_url': 'https://images.unsplash.com/photo-1516426122078-c23e76319801?auto=format&fit=crop&w=1200&q=85',
            },
            {
                'name': 'Lake Duluti Retreat',
                'description': 'A relaxed Arusha getaway centered on lakeside serenity, birding and a premium lodge stay.',
                'trip_type': 'GROUP',
                'start_date': today + timedelta(days=21),
                'end_date': today + timedelta(days=24),
                'duration_days': 4,
                'price_per_day': 260.00,
                'price_per_person': 260.00,
                'is_offer': False,
                'discount_price': None,
                'currency': 'USD',
                'total_seats': 12,
                'available_seats': 10,
                'pickup_location': 'Arusha Town/Central Hotels',
                'image_remote_url': 'https://images.unsplash.com/photo-1547970810-dc1eac37d174?auto=format&fit=crop&w=1200&q=85',
            },
            {
                'name': 'Mount Meru Trek & Lodge',
                'description': 'A premium guided trek with lodge accommodation and unforgettable views over Arusha.',
                'trip_type': 'PRIVATE',
                'start_date': today + timedelta(days=30),
                'end_date': today + timedelta(days=35),
                'duration_days': 6,
                'price_per_day': 430.00,
                'price_per_person': 430.00,
                'is_offer': True,
                'discount_price': 390.00,
                'currency': 'USD',
                'total_seats': 12,
                'available_seats': 8,
                'pickup_location': 'KIA Airport, Arusha',
                'image_remote_url': 'https://images.unsplash.com/photo-1519167758481-83f29c2a7f78?auto=format&fit=crop&w=1200&q=85',
            },
            {
                'name': 'Arusha National Park Day Tour',
                'description': 'See wildlife, scenic viewpoints and a smooth day safari route from Arusha city.',
                'trip_type': 'GROUP',
                'start_date': today + timedelta(days=10),
                'end_date': today + timedelta(days=11),
                'duration_days': 2,
                'price_per_day': 180.00,
                'price_per_person': 180.00,
                'is_offer': False,
                'discount_price': None,
                'currency': 'USD',
                'total_seats': 10,
                'available_seats': 7,
                'pickup_location': 'Arusha City/Clocktower',
                'image_remote_url': 'https://images.unsplash.com/photo-1523805009345-7448845a9e53?auto=format&fit=crop&w=1200&q=85',
            },
            {
                'name': 'Coffee & Culture Arusha Stay',
                'description': 'Blend coffee farm visits, local market browsing and elegant lodge stays in Arusha.',
                'trip_type': 'CUSTOM',
                'start_date': today + timedelta(days=38),
                'end_date': today + timedelta(days=42),
                'duration_days': 5,
                'price_per_day': 280.00,
                'price_per_person': 280.00,
                'is_offer': False,
                'discount_price': None,
                'currency': 'USD',
                'total_seats': 8,
                'available_seats': 8,
                'pickup_location': 'Arusha Town/Central Hotels',
                'image_remote_url': 'https://images.unsplash.com/photo-1504432842672-1a79f78e4084?auto=format&fit=crop&w=1200&q=85',
            },
            {
                'name': 'Arusha Heritage & Hotel Experience',
                'description': 'A curated city break with hotel comfort, heritage visits and a premium safari mood around Arusha.',
                'trip_type': 'PRIVATE',
                'start_date': today + timedelta(days=45),
                'end_date': today + timedelta(days=49),
                'duration_days': 5,
                'price_per_day': 340.00,
                'price_per_person': 340.00,
                'is_offer': True,
                'discount_price': 305.00,
                'currency': 'USD',
                'total_seats': 10,
                'available_seats': 9,
                'pickup_location': 'KIA Airport, Arusha',
                'image_remote_url': 'https://images.unsplash.com/photo-1586861635167-e5223aadc9fe?auto=format&fit=crop&w=1200&q=85',
            },
        ]

        created_trips = []
        for trip_data in trips:
            trip, _ = Trip.objects.update_or_create(
                name=trip_data['name'],
                defaults={
                    'description': trip_data['description'],
                    'trip_type': trip_data['trip_type'],
                    'start_date': trip_data['start_date'],
                    'end_date': trip_data['end_date'],
                    'duration_days': trip_data['duration_days'],
                    'price_per_day': trip_data['price_per_day'],
                    'price_per_person': trip_data['price_per_person'],
                    'is_offer': trip_data['is_offer'],
                    'discount_price': trip_data['discount_price'],
                    'currency': trip_data['currency'],
                    'total_seats': trip_data['total_seats'],
                    'available_seats': trip_data['available_seats'],
                    'pickup_location': trip_data['pickup_location'],
                    'image_remote_url': trip_data['image_remote_url'],
                    'includes_accommodation': True,
                    'includes_meals': True,
                    'includes_transport': True,
                    'includes_airport_pickup': True,
                    'is_active': True,
                }
            )
            created_trips.append(trip)

        if len(created_destinations) >= 4:
            created_trips[0].destinations.set([created_destinations[0], created_destinations[1]])
            created_trips[1].destinations.set([created_destinations[1], created_destinations[3]])
            created_trips[2].destinations.set([created_destinations[2], created_destinations[0]])
            created_trips[3].destinations.set([created_destinations[3], created_destinations[0]])
        if len(created_destinations) >= 6 and len(created_trips) >= 6:
            created_trips[4].destinations.set([created_destinations[4]])
            created_trips[5].destinations.set([created_destinations[0], created_destinations[5]])

        self.stdout.write(self.style.SUCCESS(f'Created {len(created_trips)} trips.'))

        self.stdout.write(self.style.SUCCESS('Sample data seeded successfully.'))
        self.stdout.write('Run "python manage.py seed_sample_data" again to refresh this data.')
