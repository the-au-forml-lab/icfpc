import json
import sys


def main(in_file):
    with open(in_file) as file_object:
        data = json.load(file_object)
    if data and 'rows' in data:
        for row in data["rows"]:
            if 'values' in row and 'isYou' in row and row['isYou']:
                score, team = row['values']
                print(team, score)
                return
    print('Score not found! sadness.')


if __name__ == '__main__':
    if len(sys.argv) > 1:
        main(sys.argv[1])
    else:
        print('usage: python3 -m util.py file.json')
