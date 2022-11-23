from django.core.management.base import BaseCommand

from apps.cocktails.parsers.inshaker import InshakerParser


class Command(BaseCommand):
    help = 'Runs the Inshaker parser'

    def handle(self, *args, **options):
        parser = InshakerParser()
        parser.run()
