import requests
from PIL import Image

# Пока не работает, нужно разобраться
image_data = open("izu_strip49064.png","rb").read()
image = Image.open("izu_strip49064.png").convert("RGB")

response = requests.post("http://localhost:80/v1/vision/face",files={"image":image_data}).json()
i = 0
for face in response["predictions"]:

    y_max = int(face["y_max"])
    y_min = int(face["y_min"])
    x_max = int(face["x_max"])
    x_min = int(face["x_min"])
    cropped = image.crop((x_min,y_min,x_max,y_max))
    cropped.save("image{}.jpg".format(i))

    i += 1