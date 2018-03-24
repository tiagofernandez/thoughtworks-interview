#!/usr/bin/env python3

import ast, logging, os, sys

from trains.graph import Graph
from trains.utils import read_input_data


instructions = '''
 _____             _             
|_   _|_ __  __ _ (_) _ __   ___
  | | | '__|/ _` || || '_ \ / __|
  | | | |  | (_| || || | | |\__ \\
  |_| |_|   \__,_||_||_| |_||___/

Available commands:
* distance
* nr_trips
* shortest
* quit

Usage examples:
* distance A B C
* nr_trips A C exact_stops=<int> max_stops=<int> max_distance=<int>
* shortest B B

Note: named arguments are optional.
'''

logging.basicConfig(level=logging.INFO)


def parse_command(raw):
    """
    Parses a raw text command.

    :param raw: A string describing the command
    :return: A sequence like (<command_name_str>, <arguments_list>, <optional_arguments_dict>)
    """
    raw = raw.strip()
    if not raw:
        return # nothing to do
    else:
        args, kwargs = ([], {})
        for t in raw.split(' '):
            token = t.strip()
            if '=' in token:
                name, value = [x.strip() for x in token.split('=')]
                kwargs[name] = ast.literal_eval(value)
            else:
                args.append(token)
        return (args[0].lower(), args[1:], kwargs)


def execute(command, graph):
    """
    Executes the given command.

    :param command: A sequence like (<command_name_str>, <arguments_list>, <optional_arguments_dict>)
    :param graph: An initialized Graph object
    :return: The command's result
    """
    target, result = (command[0], None)
    func = getattr(graph, target, None)
    if target == 'distance':
        result = func(command[1])
    elif target in ['nr_trips', 'shortest']:
        result = func(*command[1], **command[2])
    return result


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise ValueError('Error: provide the path to the input data (e.g. make input=data/test.txt run)')
    else:
        data = read_input_data(sys.argv[1])
        graph, command = (Graph(data), 'init')

        os.system('clear')
        print(instructions)
        print('Graph: %s\n' % graph)

        while command[0] != 'quit':
            command = parse_command(input('$ '))
            try:
                result = execute(command, graph)
                if result:
                    print('%s\n' % result)
            except:
                print('Error\n')
