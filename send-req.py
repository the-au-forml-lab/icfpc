import requests
import json
from sys import argv

from index import *

url = "https://boundvariable.space/communicate"
headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer cbf221e9-6d64-484c-b378-20198bf98757'
}

if __name__ == '__main__':
    input_str = input('type message to send:\n> ') if len(argv) == 0 else ' '.join(argv[1:])
    payload = 'S' + encode_str(input_str)
    response = requests.request("POST", url, headers=headers, data=payload).text[1:]
    print(decode_str(response))
