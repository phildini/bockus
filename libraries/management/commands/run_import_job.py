from django.conf import settings
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "get import job and run it"

    def handle(self, *args, **options):
        pass