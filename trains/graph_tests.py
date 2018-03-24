import unittest

from trains.app import read_input_data
from trains.graph import Graph


graph = Graph(read_input_data('data/test.txt'))


class TestGraph(unittest.TestCase):

    def test_distance_of_routes(self):
        self.assertDistance(1, 9, ['A', 'B', 'C'])
        self.assertDistance(2, 5, ['A', 'D'])
        self.assertDistance(3, 13, ['A', 'D', 'C'])
        self.assertDistance(4, 22, ['A', 'E', 'B', 'C', 'D'])
        self.assertDistance(5, 'NO SUCH ROUTE', ['A', 'E', 'D'])


    def test_number_of_trips(self):
        self.assertTotalTrips(6, 2, 'C', 'C', max_stops=3)
        self.assertTotalTrips(7, 3, 'A', 'C', exact_stops=4)


    def test_length_of_shortest_route(self):
        self.assertShortest(8, 9, 'A', 'C')
        self.assertShortest(9, 9, 'B', 'B')


    def test_number_of_different_routes(self):
        self.assertTotalTrips(10, 7, 'C', 'C', max_distance=30)


    def assertDistance(self, out_number, expected, path):
        result = graph.distance(path)
        self.assertResultEqual(expected, result, out_number)


    def assertTotalTrips(self, out_number, expected, origin, destination, **kwargs):
        result = graph.nr_trips(origin, destination, **kwargs)
        self.assertResultEqual(expected, result, out_number)


    def assertShortest(self, out_number, expected, origin, destination):
        result = graph.shortest(origin, destination)
        self.assertResultEqual(expected, result, out_number)


    def assertResultEqual(self, expected, result, out_number):
        print('Output #%d: %s' % (out_number, result))
        self.assertEqual(expected, result)
