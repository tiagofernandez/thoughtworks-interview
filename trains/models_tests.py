from unittest import TestCase

from trains.models import TrainNetwork
from trains.utils import read_input_data


train_network = TrainNetwork(read_input_data('data/test.txt'))


class TestTrainNetwork(TestCase):

    def test_total_distance(self):
        self.assertDistance(1, 9, ['A', 'B', 'C'])
        self.assertDistance(2, 5, ['A', 'D'])
        self.assertDistance(3, 13, ['A', 'D', 'C'])
        self.assertDistance(4, 22, ['A', 'E', 'B', 'C', 'D'])
        self.assertDistance(5, 'NO SUCH ROUTE', ['A', 'E', 'D'])


    def test_total_trips(self):
        self.assertTrips(6, 2, 'C', 'C', max_stops=3)
        self.assertTrips(7, 3, 'A', 'C', exact_stops=4)
        self.assertTrips(10, 7, 'C', 'C', max_distance=30)


    def test_shortest_route(self):
        self.assertShortest(8, 9, 'A', 'C')
        self.assertShortest(9, 9, 'B', 'B')


    def assertDistance(self, out_number, expected, path):
        result = train_network.total_distance(path)
        self.assertResultEqual(expected, result, out_number)


    def assertTrips(self, out_number, expected, origin, destination, **kwargs):
        result = train_network.total_trips(origin, destination, **kwargs)
        self.assertResultEqual(expected, result, out_number)


    def assertShortest(self, out_number, expected, origin, destination):
        result = train_network.shortest_route(origin, destination)
        self.assertResultEqual(expected, result[1], out_number)


    def assertResultEqual(self, expected, result, out_number):
        print('Output #%d: %s' % (out_number, result))
        self.assertEqual(expected, result)
