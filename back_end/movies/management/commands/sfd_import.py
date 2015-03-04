from django.core.management.base import BaseCommand, CommandError
from movies.utilities.importer import SFD_Importer

class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        importer = SFD_Importer()
        importer.runner()