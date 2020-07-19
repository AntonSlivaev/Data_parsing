import requests
from pprint import pprint
import json

token = '10796cf210796cf210796cf2b9100a74631107910796cf24f6a15c243a53fbe860107c9'
version = 5.92
domain = 'aquataz'

response = requests.get('https://api.vk.com/method/wall.get',
                        params={
                            'access_token' : token,
                            'v' : version,
                            'domain' : domain,
                            'count' : 5
                        })
data_vk = response.json()['response']['items']
pprint(data_vk)

with open('data_vk.json', 'w') as f:
    json.dump(response.json(), f)