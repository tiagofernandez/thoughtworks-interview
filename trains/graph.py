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
