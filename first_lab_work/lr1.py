import math
import sys


def calculate_y(x, a, b, c):
    return a * ((2 * x + (math.sin(b * x + c)) ** 2) / (3 + x))


def calc(params):
    n0 = params['n0']
    h = params['h']
    nk = params['nk']
    a = params['a']
    b = params['b']
    c = params['c']

    with open('../results.txt', 'w') as f:
        x = n0
        while x <= nk:
            y = calculate_y(x, a, b, c)
            f.write(f"x={x}, y={y}\n")
            x += h


def parse_config(file_path):
    params = {}

    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line:
                key, value = line.split('=')
                params[key] = float(value)

    return params


def parse_command_line_args():
    params = {}

    for arg in sys.argv[1:]:
        if '=' in arg:
            key, value = arg.split('=')
            params[key.lstrip('--')] = float(value)

    return params


if __name__ == "__main__":
    params = parse_command_line_args()

    if not params:
        params = parse_config('config.txt')

    calc(params)
