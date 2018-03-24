import logging, sys

from trains.graph import Graph


logger = logging.getLogger(__name__)


class TrainNetwork():

    def __init__(self, paths):
        """
        Initializes the network based on the provided paths.

        :param paths: e.g. ['AB5', 'BC4', 'CD8', 'DC8', 'DE6', 'AD5', 'CE2', 'EB3', 'AE7']
        """
        self._graph = Graph(paths)
        logger.info('Graph initialized: %s' % self._graph)


    def total_distance(self, path):
        """
        Calculates the distance for an exact path.

        :param path: e.g. ['A', 'B', 'C']
        :return: e.g. 9 for AB=5 and BC=4
        """
        total = 0

        # Loop from the first node until the second last
        for idx, current in enumerate(path[:-1]):
            origin, destination = (current, path[idx + 1])

            # Check the paths from the origin
            paths = self._graph.data[origin]

            if destination in paths:
                distance = paths[destination]
                total += distance # compute the distance
            else:
                total = 'NO SUCH ROUTE'
                break # abort!

        return total


    def total_trips(self, origin, destination, exact_stops=None, max_stops=None, max_distance=None):
        """
        Calculates the number of trips from an origin to a destination.

        :param origin: The start node
        :param destination: The end node
        :param exact_stops: The exact number of stops (optional)
        :param max_stops: The maximum number of stops (optional)
        :param max_distance: The maximum distance for the route (optional)
        :return: The number of different routes
        """
        total = 0
        for path in self._graph.find_paths(origin, destination):
            if exact_stops or max_stops or max_distance:
                stops = len(path) - 1
                if (exact_stops and stops == exact_stops) or (max_stops and stops <= max_stops):
                    total += 1 # one of the stop constraints matched
                elif max_distance and self.total_distance(path) < max_distance:
                    total += 1 # the distance is within its constraint
            else:
                total += 1 # no constraints to apply
        return total


    def shortest_route(self, origin, destination):
        """
        Calculates the shortest route from an origin to a destination.

        :param origin: The start node
        :param destination: The end node
        :return: The distance of the shortest route
        """
        route, distance = ([], sys.maxsize)
        for path in self._graph.find_paths(origin, destination):
            d = self.total_distance(path)
            if d < distance:
                route, distance = (path, d)
        return (route, distance)


    def __repr__(self):
        return self.__str__()


    def __str__(self):
        return str(self._graph)
