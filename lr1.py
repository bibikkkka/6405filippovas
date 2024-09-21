import argparse
import math


def calculate_y(x, a, b, c):
    return a * ((2 * x + (math.sin(b * x + c)) ** 2) / (3 + x))


def calc(params):
    n0 = params['n0']
    h = params['h']
    nk = params['nk']
    a = params['a']
    b = params['b']
    c = params['c']

    with open('results.txt', 'w') as f:
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


def create_parser():
    parser = argparse.ArgumentParser()

    parser.add_argument('--n0', type=float)
    parser.add_argument('--h', type=float)
    parser.add_argument('--nk', type=float)
    parser.add_argument('--a', type=float)
    parser.add_argument('--b', type=float)
    parser.add_argument('--c', type=float)

    return parser


def is_not_bash_args():
    updated = False

    args_mapping = {
        'n0': args.n0,
        'h': args.h,
        'nk': args.nk,
        'a': args.a,
        'b': args.b,
        'c': args.c
    }

    for key, value in args_mapping.items():
        if value is not None:
            params[key] = value
            updated = True

    return not updated


if __name__ == "__main__":
    params = {}
    parser = create_parser()
    args = parser.parse_args()
    if is_not_bash_args():
        params = parse_config('config.txt')
    calc(params)
