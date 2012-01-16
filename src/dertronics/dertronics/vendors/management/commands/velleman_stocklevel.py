from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Velleman Stocklevel Sync'

    def handle(self, *args, **options):
        self.stdout.write('Successfully closed poll')