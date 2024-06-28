import json
from sys import argv
from types import SimpleNamespace as Sn


def main(in_file):
    with open(in_file) as fp:
        data = json.load(fp, object_hook=lambda d: Sn(**d))
    rank, team, pts = next(
        ((row.values + [0])[:3] for row in data.rows
         if row.isYou), ('Team unknown', 999, 0))
    print(f'{team} is #{rank} with score {pts}')


if __name__ == '__main__':
    main(argv[1]) if len(argv) > 1 else \
        print('usage: python3 score.py input.json')