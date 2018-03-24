def read_input_data(path):
    """
    Reads input data from the provided path.

    :param path: Absolute or relative path
    :return: The graph's edges
    """
    result = []
    with open(path, 'r') as f:
        for line in f.read().splitlines():
            result += [token.strip() for token in line.split(',') if token]
    return result
