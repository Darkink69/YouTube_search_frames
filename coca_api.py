import requests
import base64


def get_description_coca(frame):
	with open(frame, "rb") as img_file:
		my_string = base64.b64encode(img_file.read())
	# print(str(my_string)[2:-1])

	api_model = 'https://nielsr-comparing-captioning-models.hf.space/run/predict'
	# api_model = 'https://laion-coca.hf.space/run/predict'

	response = requests.post(api_model, json={
		"data": [
			f"data:image/png;base64,{str(my_string)[2:-1]}",
		]
	}).json()

	data = response["data"]
	# print(data)
	return data
