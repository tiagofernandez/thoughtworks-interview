import unittest

from trains.app import parse_command


class TestApp(unittest.TestCase):

    def test_parse_command(self):
        self.assertSequenceEqual(
            ('distance', ['A', 'B', 'C'], {}),
            parse_command('distance A B C')
        )

    def test_parse_command_with_optional_args(self):
        self.assertSequenceEqual(
            ('nr_trips', ['A', 'C'], {'exact_stops': 4}),
            parse_command('nr_trips A C exact_stops=4')
        )
