import opennsfw2 as n2

# To get the NSFW probability of a single image.
image_path = "1.jpg"

nsfw_probability = n2.predict_image(image_path)

# To get the NSFW probabilities of a list of images.
# This is better than looping with `predict_image` as the model will only be instantiated once
# and batching is used during inference.
# image_paths = [
#   "path/to/your/image1.jpg",
#   "path/to/your/image2.jpg",
#   # ...
# ]

nsfw_probabilities = n2.predict_images(image_paths)
print(nsfw_probabilities)
