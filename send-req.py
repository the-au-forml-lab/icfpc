import requests
import json

url = "https://boundvariable.space/communicate"

payload = "S'%4}).$%8"
headers = {
  'Content-Type': 'application/json',
  'Authorization': 'Bearer cbf221e9-6d64-484c-b378-20198bf98757'
}

response = requests.request("POST", url, headers=headers, data=payload)

print(response.text)
