import requests

# frame = '1.jpg'

def get_nude_detect(path_folder, frame):
    print('Waitting nude detect API...')
    res = requests.post(
        "https://api.deepai.org/api/nsfw-detector",
        files={
            'image': open(f'{path_folder}/{frame}', 'rb'),
        },
        headers={'api-key': 'quickstart-QUdJIGlzIGNvbWluZy4uLi4K'}
        # headers = {'api-key': 'b2f1bc7c-65b7-4323-8509-810078010168'}

    )

    return res.json()



# res = get_nude_detect(frame)
#
# print(res)
