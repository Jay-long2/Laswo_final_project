"""Create the first admin account on a fresh deployment.

Render's free tier has no shell, so `createsuperuser` cannot be run by hand.
This reads the standard DJANGO_SUPERUSER_* variables and does nothing if the
account already exists, which keeps it safe to run on every deploy.
"""

import os

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = 'Create a superuser from DJANGO_SUPERUSER_* env vars, if one is absent.'

    def handle(self, *args, **options):
        username = os.environ.get('DJANGO_SUPERUSER_USERNAME')
        password = os.environ.get('DJANGO_SUPERUSER_PASSWORD')
        email = os.environ.get('DJANGO_SUPERUSER_EMAIL', '')

        if not username or not password:
            self.stdout.write('No DJANGO_SUPERUSER_USERNAME/PASSWORD set - skipping.')
            return

        User = get_user_model()

        if User.objects.filter(is_superuser=True).exists():
            self.stdout.write('A superuser already exists - leaving it alone.')
            return

        User.objects.create_superuser(username=username, email=email, password=password)
        self.stdout.write(self.style.SUCCESS(f'Created superuser "{username}".'))
        self.stdout.write(self.style.WARNING(
            'Now sign in, change this password, and delete the '
            'DJANGO_SUPERUSER_* variables from the Render dashboard.'
        ))
