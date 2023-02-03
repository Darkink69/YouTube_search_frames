from nsfw_detector import predict
import json
import codecs

model = predict.load_model('./mobilenet_v2_140_224')

# Predict single image
# print(predict.classify(model, '1.png'))

# # Predict multiple images at once
# result = predict.classify(model, ['./out/1.png', './out/2.jpg'])
# # {'2.jpg': {'sexy': 4.3454795e-05, 'neutral': 0.00026579312, 'porn': 0.0007733498, 'hentai': 0.14751942, 'drawings': 0.8513979}, '6.jpg': {'drawings': 0.004214506, 'hentai': 0.013342537, 'neutral': 0.01834045, 'porn': 0.4431829, 'sexy': 0.5209196}}
#
# # Predict for all images in a directory
result = predict.classify(model, 'D:\\w_edu_eng\\OSPanel\\domains\\express_2\\views\\out')

# dict = eval(result)

porn = 0.8
sexy = 0.15
hentai = 0.5
results_nsfw_all = []

for key in result.items():
    if key[1]['porn'] > porn or key[1]['sexy'] > sexy or key[1]['hentai'] > hentai and key[1]['drawings'] < 0.2:
        results_nsfw = {}
        results_nsfw['file'] = key[0].split('\\')[-1]  # Не забыть привести в порядок все пути!
        results_nsfw['porn'] = key[1]['porn']
        results_nsfw['sexy'] = key[1]['sexy']
        results_nsfw['hentai'] = key[1]['hentai']
        results_nsfw['neutral'] = key[1]['neutral']
        results_nsfw_all.append(results_nsfw)


print('Найдено', len(results_nsfw_all))
# results_nsfw_all.sort(key=lambda x: x['porn'], reverse=True)


with codecs.open('D:\\w_edu_eng\\OSPanel\\domains\\express_2\\views\\nsfw.json', 'w', encoding='utf-8') as f:
    json.dump(results_nsfw_all, f, indent=4, ensure_ascii=False)
# print(results_nsfw_all)
