import math
import sys
import  json
from typing import Callable, Tuple
from xml.etree.ElementTree import indent

import numpy as np
# type annotations


def target(x: float, a: float, b: float, c: float) -> float:
    return a * ((2 * x + (math.sin(b * x + c)) ** 2) / (3 + x))


def eval_target(function: Callable[[float, float, float, float], float],
                n0: float, h: float, nk: float, a: float, b: float, c: float) -> np.ndarray:
    # return np.column_stack((np.arange(n0, nk + h, h), [function(x, a, b, c) for x in np.arange(n0, nk + h, h)]))
    return np.array(tuple((x, function(x, a, b, c)) for x in np.arange(n0, nk + h, h)))

def save_values_as_txt(file_path: str, values: np.ndarray) -> None:
    with open(file_path, 'wt') as output_file:
        print('\n'.join(f"x = {x:>9.3f} y = {y:>9.3f}" for x, y in values), file=output_file)

def save_values_as_csv(file_path: str, values: np.ndarray) -> None:
    with open(file_path, 'wt') as output_file:
        print('x;y', file=output_file)
        print('\n'.join(f"{x:<9.3f};{y:<9.3f}" for x, y in values), file=output_file)
    #через ; каждое значение

def save_function_values(file_path: str, values: np.ndarray) -> None:
    ext = file_path.split('.')[-1]
    match ext:
        case 'txt':
            save_values_as_txt(file_path, values)
            # np.savetxt(file_path, values, fmt=' '.join(['x = %.4f'] + ['y = %.4f']))
        case 'json':
            import json
            with open(file_path, 'w') as f:
                #json.dump(values.tolist(), f, separators=(', ', ': '), indent=('\t'))
                json.dump(values.tolist(), f, indent=4)
        case 'csv':
            save_values_as_csv(file_path, values)

    #np.savetxt(file_path, values, fmt=' '.join(['x = %.4f'] + ['y = %.4f']))
        case _:
            raise ValueError("Unknown function values file format, sucker!")


def load_args(file_path: str) -> tuple[str, ...]:
    ext = file_path.split('.')[-1]
    match ext:
        case 'txt':
            return parse_config(file_path)
        case 'json':
            return parse_config(file_path)
        case 'csv':
            return parse_config(file_path)
        case _:
            raise ValueError("Unknown args file format, sucker!")

# def calc(params):
#     n0 = params['n0']
#     h = params['h']
#     nk = params['nk']
#     a = params['a']
#     b = params['b']
#     c = params['c']
#
#     with open('../results.txt', 'w') as f:
#         x = n0
#         while x <= nk:
#             y = target(x, a, b, c)
#             f.write(f"x={x}, y={y}\n")
#             x += h

def parse_config(file_path):
    params = {'n0': 0.0, 'h': 0.0, 'nk': 0, 'a': 0.0, 'b': 0.0, 'c': 0.0}

    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()

            if '=' not in line:
                continue
            try:
                key, value = line.split('=')
                params[key] = float(value)
            except KeyError as er:
                print(er)

    return tuple(params.values())


def parse_command_line_args():
    params = {'n0': 0.0, 'h': 0.0, 'nk': 0, 'a': 0.0, 'b': 0.0, 'c': 0.0}
    for arg in sys.argv[1:]:
        if '=' not in arg:
            continue
        try:
            key, value = arg.split('=')
            params[key.lstrip('--')] = float(value)
        except KeyError as er:
            print(er)
    return tuple(params.values())


def main(args_file: str = "", result_file: str = "") -> None:
    # args = None
    try:
        args = load_args(args_file)
    except ValueError as _:
        args = parse_command_line_args() # from command line
    if not args:
        raise ValueError("No args found, a-hole!")
    values = eval_target(target, *args)
    save_function_values(result_file, values)


if __name__ == "__main__":
    main("config.txt", "result.csv")
    # params = parse_command_line_args()
    #
    # if not params:
    #     params = parse_config('config.txt')
    #
    # calc(params)
