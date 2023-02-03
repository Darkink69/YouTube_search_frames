import json
import requests


client_id = 'b0H0TlN57SzctqJkUNHmltZd'
client_secret = 'LQIoP4W34GyIFecjlcPlZtgAv056VxbIC4XZ9qFCgp4q14Pl'
# params = {'url': 'views/G333Is7VPOg/keyframe-00101.jpg', 'num_keywords': 5}
# keywords = requests.get('https://api.everypixel.com/v1/keywords', params=params, auth=(client_id, client_secret)).json()
# print(keywords)

with open('views/G333Is7VPOg/keyframe-00999.jpg','rb') as image:
    data = {'data': image}
    keywords = requests.post('https://api.everypixel.com/v1/keywords', files=data, auth=(client_id, client_secret)).json()
    print(keywords)

# keywords = {'keywords': [{'keyword': 'one person', 'score': 0.8196252209768284}, {'keyword': 'adult', 'score': 0.8063291549538628}, {'keyword': 'outdoors', 'score': 0.7027960174043226}, {'keyword': 'women', 'score': 0.5283648376173674}, {'keyword': 'travel', 'score': 0.48833746439202}, {'keyword': 'lifestyles', 'score': 0.42566295476372507}, {'keyword': 'men', 'score': 0.35290727349508433}, {'keyword': 'adults only', 'score': 0.30754476964971666}, {'keyword': 'caucasian ethnicity', 'score': 0.28926513578689217}, {'keyword': 'tourist', 'score': 0.28175086296182705}, {'keyword': 'looking', 'score': 0.2649282876831887}, {'keyword': 'one', 'score': 0.26264680233987164}, {'keyword': 'woman', 'score': 0.26264680233987164}], 'status': 'ok'}
tags = []

for key in range(5):
    tags.append(keywords['keywords'][key]['keyword'])

print(tags)

