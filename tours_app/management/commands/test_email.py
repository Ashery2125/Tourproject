from django.conf import settings
from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    help = 'Send a test email using the configured SMTP settings.'

    def add_arguments(self, parser):
        parser.add_argument('recipient', help='Email address that should receive the test message.')

    def handle(self, *args, **options):
        recipient = options['recipient']
        if not settings.EMAIL_HOST_USER or not settings.EMAIL_HOST_PASSWORD:
            raise CommandError('EMAIL_HOST_USER and EMAIL_HOST_PASSWORD must be set in .env first.')

        sent = send_mail(
            'WildVista Safaris email test',
            (
                'Hello,\n\n'
                'This is a successful test from the WildVista Safaris booking system.\n\n'
                'If you received this, real email notifications are configured correctly.'
            ),
            settings.DEFAULT_FROM_EMAIL,
            [recipient],
            fail_silently=False,
        )
        self.stdout.write(self.style.SUCCESS(f'Sent {sent} test email to {recipient}.'))
