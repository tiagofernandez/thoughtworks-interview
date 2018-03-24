import unittest

from trains.graph import Graph
from trains.utils import read_input_data


graph = Graph(read_input_data('data/test.txt'))


class TestGraph(unittest.TestCase):

    def test_init(self):
        self.assertDictEqual(
            {'A': {'B': 5, 'D': 5, 'E': 7}, 'B': {'C': 4}, 'C': {'D': 8, 'E': 2}, 'D': {'C': 8, 'E': 6}, 'E': {'B': 3}},
            graph.data
        )


    def test_generate_paths(self):
        self.assertEqual(18, len(graph.find_paths('A', 'C')[-1]))
        self.assertEqual(7, len(graph.find_paths('A', 'C', max_paths=10)[-1]))
