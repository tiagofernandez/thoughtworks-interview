#!/usr/bin/env python3

import ast, logging, os, sys

from trains.models import TrainNetwork
from trains.utils import read_input_data


instructions = '''\
 _____             _             
|_   _|_ __  __ _ (_) _ __   ___
  | | | '__|/ _` || || '_ \ / __|
  | | | |  | (_| || || | | |\__ \\
  |_| |_|   \__,_||_||_| |_||___/

Available commands:
* distance (d)
* trips (t)
* shortest (s)
* quit (q)

Usage examples - named arguments are optional:
* distance A B C
* trips A C exact_stops=<int> max_stops=<int> max_distance=<int>
* shortest B B

Graph:
%s
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
            elif token:
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
    if target in ['distance', 'd']:
        result = getattr(graph, 'total_distance')(command[1])
    elif target in ['trips', 't']:
        result = getattr(graph, 'total_trips')(*command[1], **command[2])
    elif target in ['shortest', 's']:
        result = getattr(graph, 'shortest_route')(*command[1], **command[2])
    return result


if __name__ == '__main__':
    if len(sys.argv) < 2:
        raise ValueError('Error: provide the path to the input data (e.g. make input=data/test.txt run)')
    else:
        data = read_input_data(sys.argv[1])
        train_network, command = (TrainNetwork(data), 'init')

        os.system('clear')
        print(instructions % train_network)

        while command[0] not in ['quit', 'q']:
            command = parse_command(input('$ '))
            try:
                result = execute(command, train_network)
                if result:
                    print('%s\n' % str(result))
            except Exception as ex:
                print('Error %s\n' % ex)
