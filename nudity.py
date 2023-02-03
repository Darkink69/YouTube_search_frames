import requests
from PIL import Image, ImageFilter, ImageDraw
import os

itemImg = 'nude.jpg'

print('Waitting API...')
r = requests.post(
    "https://api.deepai.org/api/nsfw-detector",
    files={
        'image': open(itemImg, 'rb'),
    },
    headers={'api-key': 'b2f1bc7c-65b7-4323-8509-810078010168'}
)

print(r.json())
result = r.json()
# result = {'id': 'e0dd97de-c6a7-4c2e-8c12-b131041002bf', 'output': {'detections': [{'confidence': '0.91', 'bounding_box': [375, 245, 91, 67], 'name': 'Buttocks - Exposed'}, {'confidence': '0.92', 'bounding_box': [546, 259, 82, 70], 'name': 'Buttocks - Exposed'}], 'nsfw_score': 0.7162511348724365}}


countDetection = len(result['output']['detections'])


img = Image.open(itemImg)
img1 = ImageDraw.Draw(img)
fill = ["#06fefe", '#ff00ff', '#ffff00', '#00ff00', '#ffffff', '#fc99b8']

for detect in range(countDetection):
    x = result['output']['detections'][detect]['bounding_box'][0]
    y = result['output']['detections'][detect]['bounding_box'][1]
    w = result['output']['detections'][detect]['bounding_box'][2]
    h = result['output']['detections'][detect]['bounding_box'][3]
    nameDetections = result['output']['detections'][detect]['name']
    confidenceDetections = result['output']['detections'][detect]['confidence']

    shape = [(x, y), (x + w, y + h)]
    img1.rectangle(shape, outline=fill[detect], width=3)
    img1.text((x, y + h + 5), nameDetections, fill=fill[detect], align='left')
    img1.text((x, y + h + 15), confidenceDetections, fill=fill[detect], align='left')

nsfwScore = str(result['output']['nsfw_score'])
img1.text((10, 10), nsfwScore, fill="red", align='left')

# img.show()
img.save('nsfw_out.png')



