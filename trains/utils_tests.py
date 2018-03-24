import unittest

from trains.utils import read_input_data


class TestUtils(unittest.TestCase):

    def test_read_input_data(self):
        self.assertListEqual(
            ['AB5', 'BC4', 'CD8', 'DC8', 'DE6', 'AD5', 'CE2', 'EB3', 'AE7'],
            read_input_data('data/test.txt')
        )
