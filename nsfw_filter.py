import replicate
REPLICATE_API_TOKEN = 'ef34f7e2bc4cb43fff0f6299bc0a84f5f18d1e7c'

model = replicate.models.get("m1guelpf/nsfw-filter")
version = model.versions.get("88c3624a13d60bb5ecd0cb215e49e39d2a2135c211bcb94fc801d3def46803c4")

# https://replicate.com/m1guelpf/nsfw-filter/versions/88c3624a13d60bb5ecd0cb215e49e39d2a2135c211bcb94fc801d3def46803c4#input
inputs = {
    # Image to run through the NSFW filter
    'image': open("nu.png", "rb"),
}

# https://replicate.com/m1guelpf/nsfw-filter/versions/88c3624a13d60bb5ecd0cb215e49e39d2a2135c211bcb94fc801d3def46803c4#output-schema
output = version.predict(**inputs)
print(output)
