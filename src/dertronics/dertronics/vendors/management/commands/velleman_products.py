from django.core.management.base import BaseCommand

from suds.client import Client
from suds.transport.http import HttpAuthenticated

from dertronics.vendors.velleman.client import Client

class Command(BaseCommand):
    help = 'Velleman Product Sync'

    def handle(self, *args, **options):

        velleman = Client()

        for popular_product in velleman.get_popular_products():
            product = velleman.get_product(popular_product.value)
            print '---'
            print product
            print '---'