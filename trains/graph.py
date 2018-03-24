from queue import Queue


class Graph():

    def __init__(self, edges):
        """
        Initializes the directed graph.

        :param edges: e.g. ['AB5', 'BC4', 'CD8', 'DC8', 'DE6', 'AD5', 'CE2', 'EB3', 'AE7']
        """
        self._graph = {}

        for edge in edges or []:
            origin, destination, distance = (edge[0], edge[1], int(edge[2:]))

            # Init origin if not yet in the graph
            if origin not in self._graph:
                self._graph[origin] = {}

            # Connect origin to destination with its distance
            self._graph[origin][destination] = distance


    @property
    def data(self):
        return self._graph


    def find_paths(self, origin, destination, max_paths=1000):
        """
        Finds all path permutations from an origin to a destination,
        limited by this Graph's max depth.

        :param origin: The start node
        :param destination: The end node
        :param max_paths: The max number of path permutations to generate (optional)
        :return: A list of paths (e.g. [['A', 'B', 'C'], ...])
        """
        queue = Queue()
        with queue.mutex:
            queue.queue.clear()

        # Generate all paths (within the predefined max depth)
        paths = self._generate_paths(queue, origin, destination)

        # Discard invalid permutations (single node paths e.g. ['C'])
        return [p for p in [next(paths) for _ in range(max_paths)] if len(p) > 1]


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


    def __repr__(self):
        return self.__str__()


    def __str__(self):
        return str(self._graph)
