import replicate
# export REPLICATE_API_TOKEN = "ef34f7e2bc4cb43fff0f6299bc0a84f5f18d1e7c"


def get_description_interrogator(frame):
    model = replicate.models.get("pharmapsychotic/clip-interrogator")
    version = model.versions.get("a4a8bafd6089e1716b06057c42b19378250d008b80fe87caa5cd36d40c1eda90")

    # https://replicate.com/pharmapsychotic/clip-interrogator/versions/a4a8bafd6089e1716b06057c42b19378250d008b80fe87caa5cd36d40c1eda90#input
    inputs = {
        # Input image
        'image': open(frame, "rb"),

        # Choose ViT-L for Stable Diffusion 1, and ViT-H for Stable Diffusion
        # 2
        'clip_model_name': "ViT-L-14/openai",

        # Prompt mode (best takes 10-20 seconds, fast takes 1-2 seconds).
        'mode': "best",
    }

    # https://replicate.com/pharmapsychotic/clip-interrogator/versions/a4a8bafd6089e1716b06057c42b19378250d008b80fe87caa5cd36d40c1eda90#output-schema
    output = version.predict(**inputs)
    print(output)
    return output
