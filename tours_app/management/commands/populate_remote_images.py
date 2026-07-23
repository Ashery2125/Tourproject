from django.core.management.base import BaseCommand
from tours_app.models import Trip, Destination


SAMPLE_TRIP_IMAGES = [
    'https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=1200&q=80',
    'https://images.unsplash.com/photo-1526779259212-5a8f0b89f4a9?auto=format&fit=crop&w=1200&q=80',
    'https://images.unsplash.com/photo-1482192505345-5655af888cc4?auto=format&fit=crop&w=1200&q=80',
    'https://images.unsplash.com/photo-1508672019048-805c876b67e2?auto=format&fit=crop&w=1200&q=80',
]

SAMPLE_DEST_IMAGES = [
    'https://images.unsplash.com/photo-1536684182010-56c43846dfa7?auto=format&fit=crop&w=1200&q=80',
    'https://images.unsplash.com/photo-1542314831-068cd1dbfeeb?auto=format&fit=crop&w=1200&q=80',
    'https://images.unsplash.com/photo-1500534314209-a25ddb2bd429?auto=format&fit=crop&w=1200&q=80',
    'https://images.unsplash.com/photo-1519681393784-d120267933ba?auto=format&fit=crop&w=1200&q=80',
]

class Command(BaseCommand):
    help = 'Populate image_remote_url for Trips and Destinations that have no remote URL set.'

    def handle(self, *args, **options):
        trips = Trip.objects.filter(image_remote_url__isnull=True)
        updated_trips = 0
        for i, trip in enumerate(trips):
            trip.image_remote_url = SAMPLE_TRIP_IMAGES[i % len(SAMPLE_TRIP_IMAGES)]
            trip.save()
            updated_trips += 1

        dests = Destination.objects.filter(image_remote_url__isnull=True)
        updated_dests = 0
        for i, dest in enumerate(dests):
            dest.image_remote_url = SAMPLE_DEST_IMAGES[i % len(SAMPLE_DEST_IMAGES)]
            dest.save()
            updated_dests += 1

        self.stdout.write(self.style.SUCCESS(f'Updated {updated_trips} trips and {updated_dests} destinations with remote images.'))
