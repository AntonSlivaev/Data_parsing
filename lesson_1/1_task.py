import requests
import json

username = 'AntonSlivaev'
main_link = 'https://api.github.com'

response = requests.get(f'{main_link}/users/{username}/repos')

with open('data.json', 'w') as f:
    json.dump(response.json(), f)

for i in response.json():
    print(i['name'])