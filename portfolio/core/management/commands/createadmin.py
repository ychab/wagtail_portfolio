from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

User = get_user_model()


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('--username', required=True)
        parser.add_argument('--password', required=True)
        parser.add_argument('--email', default='admin@example.com')

    def handle(self, *args, **options):
        User.objects.create_superuser(
            username=options['username'],
            email=options['email'],
            password=options['password'],
        )
        self.stdout.write(self.style.SUCCESS('Superuser created successfully.'))
