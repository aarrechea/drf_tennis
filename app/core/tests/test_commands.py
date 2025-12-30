"""
Test custom Django management commands
"""
from unittest.mock import patch
from psycopg2 import OperationalError as Psycopg2Error
from django.db.utils import OperationalError
from django.core.management import call_command
from django.test import SimpleTestCase


@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    """
    Tests for custom Django management commands
    """

    def test_wait_for_db_ready(self, patched_check):
        """
        Test waiting for database if database is ready
        """
        patched_check.return_value = True
        call_command('wait_for_db')
        patched_check.assert_called_once()

    # To speed up the test avoiding actual sleep.
    @patch('time.sleep', return_value=True)
    def test_wait_for_db_delay(self, patched_sleep, patched_check):
        """
        Test waiting for database when getting OperationalError
        """
        # Simulate OperationalError being raised 5 times before succeeding
        patched_check.side_effect = [Psycopg2Error]*2 + [OperationalError]*3 \
            + [True]

        # Call the command
        call_command('wait_for_db')

        # Verify that the check method was called 6 times
        self.assertEqual(patched_check.call_count, 6)

        # Verify that the check method was called with the correct database
        patched_check.assert_called_with(databases=['default'])
