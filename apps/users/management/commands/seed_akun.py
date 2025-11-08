from django.core.management.base import BaseCommand
from apps.users.models import Akun

class Command(BaseCommand):
    help = 'Seeds the database with a specified number of Akun objects.'

    def add_arguments(self, parser):
        parser.add_argument('count', type=int, help='The number of accounts to create.')

    def handle(self, *args, **options):
        count = options['count']
        for i in range(count):
            email = f'user{i+1}@example.com'
            password = 'password123'
            try:
                Akun.objects.create_user(email=email, password=password)
                self.stdout.write(self.style.SUCCESS(f'Successfully created Akun: {email}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating Akun {email}: {e}'))

        self.stdout.write(self.style.SUCCESS(f'Successfully created {count} Akun objects.'))