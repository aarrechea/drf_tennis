"""
Django command to wait for the database to be available.
"""
from django.core.management.base import BaseCommand
import time
from psycopg2 import OperationalError as Psycopg2Error
from django.db.utils import OperationalError


class Command(BaseCommand):
    """
    Django command to wait for the database to be available.
    """

    def handle(self, *args, **options):
        """
        Entry point for command
        """
        self.stdout.write('Waiting for database...')

        db_up = False
        while not db_up:
            try:
                # Try to connect to the database. Check is a method of
                # BaseCommand.
                self.check(databases=['default'])
                db_up = True
            except (Psycopg2Error, OperationalError):
                self.stdout.write('Database unavailable, waiting 1 second...')
                time.sleep(1)

        # When the database is available it shows a success message.
        self.stdout.write(self.style.SUCCESS('Database available!'))
