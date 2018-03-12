import sys

from queue import Queue


class Graph():

    def __init__(self, edges, max_depth=100):
        """
        Initializes the directed graph.

        :param edges: e.g. ['AB5', 'BC4', 'CD8', 'DC8', 'DE6', 'AD5', 'CE2', 'EB3', 'AE7']
        :param max_depth: The max depth for the path permutations
        """
        self._graph = {}
        self._max_depth = max_depth

        for edge in edges or []:
            origin, destination, distance = (edge[0], edge[1], int(edge[2:]))

            # Init origin if not yet in the graph
            if origin not in self._graph:
                self._graph[origin] = {}

            # Connect origin to destination with its distance
            self._graph[origin][destination] = distance


    def _generate_paths(self, queue, origin, destination, path=None):
        """
        Generates all possible paths using BFS strategy for traversing the graph.
        It starts at some arbitrary node and explores the neighbor nodes first,
        before moving to the next level neighbours. The Queue's FIFO concept ensures
        that what is discovered first will be explored first, before exploring those
        discovered subsequently.

        :param queue: The Queue to be used
        :param origin: The start node
        :param destination: The end node
        :return: A generator
        """
        path = path or []
        queue.put((self._graph, origin, destination, path))

        while not queue.empty():
            self._graph, current, destination, path = queue.get()

            # Return path if the destination was reached
            if current == destination:
                yield path + [current]

            # Append neighbors so they get expanded
            if current in self._graph:
                for neighbor in self._graph[current]:
                    queue.put((self._graph, neighbor, destination, path + [current]))


    def _find_paths(self, origin, destination):
        """
        Finds all path permutations from an origin to a destination,
        limited by this Graph's max depth.

        :param origin: The start node
        :param destination: The end node
        :return: A list of paths (e.g. [['A', 'B', 'C'], ...])
        """
        queue = Queue()
        with queue.mutex:
            queue.queue.clear()

        # Generate all paths (within the predefined max depth)
        paths = self._generate_paths(queue, origin, destination)

        # Discard invalid permutations (single node paths e.g. ['C'])
        return [p for p in [next(paths) for _ in range(self._max_depth)] if len(p) > 1]


    def calc_distance(self, path):
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
            paths = self._graph[origin]

            if destination in paths:
                distance = paths[destination]
                total += distance # compute the distance
            else:
                total = 'NO SUCH ROUTE'
                break # abort!

        return total


    def calc_trips(self, origin, destination, exact_stops=None, max_stops=None, max_distance=None):
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
        for path in self._find_paths(origin, destination):
            if exact_stops or max_stops or max_distance:
                stops = len(path) - 1
                if (exact_stops and stops == exact_stops) or (max_stops and stops <= max_stops):
                    total += 1 # one of the stop constraints matched
                elif max_distance and self.calc_distance(path) < max_distance:
                    total += 1 # the distance is within its constraint
            else:
                total += 1 # no constraints to apply
        return total


    def calc_shortest(self, origin, destination):
        """
        Calculates the shortest route from an origin to a destination.

        :param origin: The start node
        :param destination: The end node
        :return: The distance of the shortest route
        """
        shortest = sys.maxsize
        for path in self._find_paths(origin, destination):
            distance = self.calc_distance(path)
            if distance < shortest:
                shortest = distance
        return shortest
