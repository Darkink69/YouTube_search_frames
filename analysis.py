import load_mongoDB_to_links
import make_frames
import different
import coca_api
import CLIP_interrogator
import nsfw
import get_from_mongoDB
import yt_dlp_info
import load_mongoDB_to_links
import get_i_frames
import load_subs
import face_analyze
import nudity
import time
import datetime as dt
from pymongo import MongoClient


def time_now():
    return dt.datetime.now().strftime("%H:%M:%S")


def make_time_i_frame(i_frame, fps=30):
    i_frame_seconds = []
    for i in i_frame:
        i_frame_seconds.append(i // fps)
        # print(i // fps)
    return i_frame_seconds


def sub_to_frame(subs, i_frame, fps):
    i_frames_ms = {}
    for i in range(len(i_frame)):
        i_frames_ms[i_frame[i]] = (i_frame[i] // fps) * 1000 + (i_frame[i] % fps) * (1000 // fps)
    print(subs)
    print((i_frames_ms))
    subs_on_frames = {}
    for sub in subs:
        for i in range(len(i_frames_ms) - 1):
            if sub['tStartMs'] >= list(i_frames_ms.values())[i] and sub['tStartMs'] < list(i_frames_ms.values())[i + 1]:
                if not list(i_frames_ms.keys())[i] in subs_on_frames:
                    subs_on_frames[list(i_frames_ms.keys())[i]] = sub['segs']
                elif list(i_frames_ms.keys())[i] in subs_on_frames:
                    # print('уже есть!', sub['segs'])
                    item_sub = subs_on_frames[list(i_frames_ms.keys())[i]] + ' ' + sub['segs']
                    subs_on_frames[list(i_frames_ms.keys())[i]] = item_sub

    print(subs_on_frames)
    return subs_on_frames


def create_data_frame(frames, i_frame, i_frame_seconds, subs_on_frames, unique_frames, desc_frames,
                      keywords_frames, suss_nsfw_all, faces_analize, nsfw_text, nsfw_frames):
    data_frame = {}
    for i in range(len(i_frame)):
        data_frame[str(i_frame[i])] = [
            {'frame_second': i_frame_seconds[i]},
            {'frame': frames[i]},
            {'sub': ''},
            {'unique_frame': False},
            {'desc_frame': []},
            {'keywords': []},
            {'suss_nsfw': False},
            {'frame_faces': []},
            {'nsfw_text': False},
            # {'nsfw': False},
            # {'nsfw_content': ''}
        ]

        for sub in subs_on_frames:
            if i_frame[i] == sub:
                data_frame[str(i_frame[i])][2]['sub'] = subs_on_frames[sub]

        for frame in unique_frames:
            if frames[i] == frame:
                data_frame[str(i_frame[i])][3]['unique_frame'] = True

        for frame, value in desc_frames.items():
            if frames[i] == frame:
                data_frame[str(i_frame[i])][4]['desc_frame'] = value

        for frame, value in keywords_frames.items():
            if frames[i] == frame:
                print(value)
                data_frame[str(i_frame[i])][5]['keywords'] = value

        for frame in suss_nsfw_all:
            if frames[i] == frame:
                data_frame[str(i_frame[i])][6]['suss_nsfw'] = True

        for frame, value in faces_analize.items():
            if frames[i] == frame:
                del value['race']
                del value['emotion']
                data_frame[str(i_frame[i])][7]['frame_faces'] = value

        for frame in nsfw_text:
            if frames[i] == frame:
                data_frame[str(i_frame[i])][8]['nsfw_text'] = True

        # for frame in nsfw_frames:
        #     if frames[i] == frame['file']:
        #         data_frame[str(i_frame[i])][9]['nsfw'] = True
        #         data_frame[str(i_frame[i])][10]['nsfw_content'] = frame['nsfw']

    # print(data_frame)
    return data_frame


def unique_process(frames, path_folder):
    tolerance = 15  # степень похожести кадров от 0 (одинаковые) до 30 (или даже до 64)
    unique_frames = []
    count_frames = {}
    count = 0

    if len(frames) > 400:
        depth_frames = 20
    elif 400 > len(frames) > 100:
        depth_frames = 40
    else:
        depth_frames = 100

    # depth_frames = 1000

    def split_frames(frames, depth_frames):
        for i in range(0, len(frames), depth_frames):
            yield frames[i:i + depth_frames]

    blocks_frames = list(split_frames(frames, depth_frames))

    for block in blocks_frames:
        print(depth_frames, 'depth frames similar. Start of block')

        print('Searching for similar frames...')
        for first_frame in block:
            group_frames = []
            count += 1
            for second_frame in block:
                result = different.process_frame(f'{path_folder}/{first_frame}', f'{path_folder}/{second_frame}')
                # print(first_frame, second_frame, result)
                if result < tolerance:
                    group_frames.append(second_frame)
            count_frames[count] = group_frames
            print(first_frame, 'processed')

        # print(count_frames)

        for key, value in count_frames.items():
            if value[0] not in unique_frames:
                unique_frames.append(value[0])

    # print(unique_frames)
    return unique_frames


def get_analysis_frames(path_folder, unique_frames):
    desc_frames = {}
    interrogator = False
    print('Waiting coca and other api...')

    for index, frame in enumerate(unique_frames):
        print(f'Frame {index + 1} / {len(unique_frames)}')
        try:
            data = coca_api.get_description_coca(f'{path_folder}/{frame}')
        except BaseException:
            print('Problem with connect to CoCa API..')
            data = []

        print(data)
        # if index % 10 == 0 and index > 5:
        #     interrogator = True
        #
        # if interrogator:
        #     print('Waiting CLIP_interrogator api...')
        #     try:
        #         output = CLIP_interrogator.get_description_interrogator(f'{path_folder}/{frame}')
        #         data.append(output)
        #         interrogator = False
        #     except BaseException:
        #         print('Problem with connect to CLIP_interrogator API..')
        #         interrogator = False

        desc_frames[frame] = data

    return desc_frames


def analysis_text(desc_frames):
    keywords_frames = {}
    bad_words = ['a', 'the', 'of', 'and', 'from', 'to', 'that', 'with', 'is', 'by', 'in', 'on', '.', '?', ',', '!',
                 'are', 'at', 'it', 'front', '[', ']', '(', ')', '-', 'an', 'for', 'into', 'am', '', '"', '`', "'",
                 "'s", 'there', 'has', 'who', 'his', 'I']

    nsfw_words = ['bikinisuit', 'bikini', 'bikinis', 'panties', 'bra', 'bodysuit', 'underwear', 'stripped', 'undressed',
                  'unclothed', 'naked', 'nude', 'bare', 'stark-naked', 'disrobed', 'unclad', 'undraped',
                  'unsheathed', 'breasts', 'breast', 'breasty', 'topless', 'boobs', 'nipples', 'nipple', 'butt', 'ass',
                  'sex', 'sexual', 'sexy', 'uncensored', 'lingerie', 'lingersuit']

    nsfw_text = []
    for k, v in desc_frames.items():
        # print(k)
        words = []
        for i in v:
            keys = i.split(' ')
            for key in keys:
                if key not in bad_words:
                    if key[-1] == '.' or key[-1] == ',':
                        key = key[-1]
                    elif key not in words:
                        words.append(key)
        # print(words)
        for word in words:
            if word in nsfw_words and k not in nsfw_text:
                nsfw_text.append(k)

        keywords_frames[k] = words

    # print(keywords_frames)
    count_keywords_frames = {}
    unique_words = []
    all_words = []

    for k, v in keywords_frames.items():

        for i in v:
            if i not in unique_words:
                unique_words.append(i)

        for i in v:
            all_words.append(i)

    print(len(unique_words), 'unique words')
    # print(all_words)
    # print(len(all_words))
    count = 1
    for word in all_words:
        if word not in count_keywords_frames:
            count_keywords_frames[word] = count
        else:
            count = count_keywords_frames[word] + 1
            count_keywords_frames[word] = count

    sorted_words = dict(sorted(count_keywords_frames.items(), key=lambda item: item[1]))
    return unique_words, sorted_words, keywords_frames, nsfw_text


def get_all_faces(path_folder, frames):
    faces_analize = {}
    print('Face detected..')
    for frame in frames:
        face = face_analyze.face_analyze(path_folder, frame)
        print(frame)
        print(face)
        faces_analize[frame] = face

    delete = []
    for k, v in faces_analize.items():
        try:
            x = v['gender']
        except BaseException:
            delete.append(k)
    for key in delete:
        faces_analize.pop(key, None)

    print(faces_analize)
    print(len(faces_analize), 'faces')
    return faces_analize


def get_nsfw_confirm(path_folder, nsfw_text):
    nsfw_frames = []

    for frame in nsfw_text:
        print(frame)
        try:
            result = nudity.get_nude_detect(path_folder, frame)
            print(result)
            if 'status' in result:
                print(result['status'])
                result = {'id': '', 'output': {}, 'file': ''}
        except BaseException:
            print('Problem with nude detect API..')
            result = {'id': '', 'output': {}, 'file': ''}

        item = []
        for k, v in result['output'].items():
            item.append(v)
            if (len(item) > 1 and item[1] > 0.1) or (len(item[0]) > 0):
                if len(item[0]) > 0:
                    # print(item[0][0]['name'])
                    temp = ''
                    for i in range(len(item[0])):
                        # print(item[0][i]['name'])
                        temp += item[0][i]['name'] + ' '
                        result['nsfw'] = temp
                else:
                    result['nsfw'] = ''
                result['file'] = frame

        del result['id']
        del result['output']

        nsfw_frames.append(result)

    # print(nsfw_frames)
    return nsfw_frames


def save_to_db(id, data_frame, type_subs, frequently_words):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['urldb']
    collection = db['mongourls']

    text_info = {}
    text_info['data_frame'] = data_frame
    text_info['type_subs'] = type_subs
    text_info['frequently_words'] = frequently_words
    text_info['screencomix'] = True
    collection.update_one({'id': id}, {'$set': text_info})


def process_links(ids):
    for id in ids:
        print(id)

        description = False
        unique = False
        face = False
        suss_nsfw = False

        field = 'prev_video'
        urls = get_from_mongoDB.load_mongo_data(id, field)

        quality = 'medium'
        # quality = 'hd'
        # quality = '4k'
        if quality == '4k' and '4k_video' in urls[0]:
            url = urls[0]['4k_video'][0]['url']
        elif quality == 'hd' and 'hd_video' in urls[0]:
            url = urls[0]['hd_video'][0]['url']
        elif quality == 'medium':
            url = urls[0]['url_medium']

        frames, path_folder = make_frames.makeFrames(id, url)
        print(frames)
        print(len(frames), 'i_frames.')

        i_frame = get_i_frames.get_i_keyframes(url)
        print(i_frame)

        field = 'fps'
        fps = get_from_mongoDB.load_mongo_data(id, field)[0]
        print(fps, 'fps')

        i_frame_seconds = make_time_i_frame(i_frame, fps)
        # print(i_frame_seconds)

        print('Loading subtitles..')
        field = 'subs'
        raw_subs = get_from_mongoDB.load_mongo_data(id, field)
        lang = 'English'
        subs, type_subs = load_subs.get_subs_from_url(raw_subs, lang)
        print(type_subs)

        subs_on_frames = sub_to_frame(subs, i_frame, fps)
        # print(subs_on_frames)

        if unique:
            unique_frames = unique_process(frames, path_folder)  # фильтрация кадров на "уникальность"
        else:
            unique_frames = frames
        print(len(unique_frames))

        if suss_nsfw:
            suss_nsfw_all = nsfw.get_nsfw_frames(path_folder)
        else:
            suss_nsfw_all = []
        print(suss_nsfw_all)

        if face:
            faces_analize = get_all_faces(path_folder, frames)
        else:
            faces_analize = {}
        print(faces_analize)

        if description:
            desc_frames = get_analysis_frames(path_folder, unique_frames)  # описание каждого кадра из API
        else:
            desc_frames = {}
        print(desc_frames)

        unique_words, sorted_words, keywords_frames, nsfw_text = analysis_text(desc_frames)
        print(keywords_frames)
        print(sorted_words)
        print(nsfw_text)

        # if description:
        #     nsfw_frames = get_nsfw_confirm(path_folder, nsfw_text)
        # else:
        #     nsfw_frames = {}
        # print(nsfw_frames)
        nsfw_frames = []

        tolerance_keys = 20
        frequently_words = list(sorted_words.keys())[-tolerance_keys:][::-1]
        print(frequently_words)

        data_frame = create_data_frame(frames, i_frame, i_frame_seconds, subs_on_frames, unique_frames, desc_frames,
                                       keywords_frames, suss_nsfw_all, faces_analize, nsfw_text, nsfw_frames)
        # print(data_frame)

        save_to_db(id, data_frame, type_subs, frequently_words)

        # Другие анализы какие надо


print(time_now(), '| Start processing')
field = 'screencomix'
ids = load_mongoDB_to_links.load_mongo_data_url(field)
process_links(ids)
print(time_now(), ids, '| processed')





# def create_data_frame(frames, i_frame, i_frame_seconds, subs_on_frames, unique_frames, desc_frames,
#                       keywords_frames, suss_nsfw_all):


# frames = ['keyframe-00001.jpg', 'keyframe-00002.jpg', 'keyframe-00003.jpg', 'keyframe-00004.jpg', 'keyframe-00005.jpg', 'keyframe-00006.jpg', 'keyframe-00007.jpg', 'keyframe-00008.jpg', 'keyframe-00009.jpg', 'keyframe-00010.jpg', 'keyframe-00011.jpg', 'keyframe-00012.jpg', 'keyframe-00013.jpg', 'keyframe-00014.jpg', 'keyframe-00015.jpg', 'keyframe-00016.jpg', 'keyframe-00017.jpg', 'keyframe-00018.jpg', 'keyframe-00019.jpg', 'keyframe-00020.jpg', 'keyframe-00021.jpg', 'keyframe-00022.jpg', 'keyframe-00023.jpg', 'keyframe-00024.jpg', 'keyframe-00025.jpg', 'keyframe-00026.jpg', 'keyframe-00027.jpg', 'keyframe-00028.jpg']
# i_frame = [0, 128, 256, 384, 425, 512, 530, 573, 613, 665, 704, 736, 763, 864, 895, 927, 992, 1049, 1120, 1139, 1196, 1248, 1268, 1301, 1376, 1495, 1578, 1616]
# faces_analize = {'keyframe-00007.jpg': {'age': 33, 'region': {'x': 208, 'y': 54, 'w': 49, 'h': 49}, 'gender': 'Woman', 'race': {'asian': 0.5412340629845858, 'indian': 0.5783332511782646, 'black': 0.06897193961776793, 'white': 74.0094006061554, 'middle eastern': 12.801310420036316, 'latino hispanic': 12.000750750303268}, 'dominant_race': 'white', 'emotion': {'angry': 7.704355766691151e-05, 'disgust': 4.3859555987069143e-07, 'fear': 3.1666897370996594e-05, 'happy': 98.76141548156738, 'sad': 0.00628165653324686, 'surprise': 0.000993965022644261, 'neutral': 1.2311996892094612}, 'dominant_emotion': 'happy'}, 'keyframe-00021.jpg': {'age': 30, 'region': {'x': 356, 'y': 54, 'w': 130, 'h': 130}, 'gender': 'Man', 'race': {'asian': 2.6041267439723015, 'indian': 2.9840676113963127, 'black': 0.43893270194530487, 'white': 45.36783993244171, 'middle eastern': 19.18405592441559, 'latino hispanic': 29.42097783088684}, 'dominant_race': 'white', 'emotion': {'angry': 0.4468207247555256, 'disgust': 6.697639491903828e-05, 'fear': 1.7912335693836212, 'happy': 0.8169467560946941, 'sad': 3.28676775097847, 'surprise': 0.04967416753061116, 'neutral': 93.60849261283875}, 'dominant_emotion': 'neutral'}, 'keyframe-00022.jpg': {'age': 31, 'region': {'x': 380, 'y': 81, 'w': 128, 'h': 128}, 'gender': 'Man', 'race': {'asian': 31.828024983406067, 'indian': 2.032875083386898, 'black': 0.8732333779335022, 'white': 44.8935866355896, 'middle eastern': 8.946999907493591, 'latino hispanic': 11.425279825925827}, 'dominant_race': 'white', 'emotion': {'angry': 4.070758074522018, 'disgust': 0.001154409437731374, 'fear': 0.47593084163963795, 'happy': 2.03335452824831, 'sad': 2.1343789994716644, 'surprise': 0.16907159006223083, 'neutral': 91.11535549163818}, 'dominant_emotion': 'neutral'}, 'keyframe-00025.jpg': {'age': 25, 'region': {'x': 323, 'y': 62, 'w': 107, 'h': 107}, 'gender': 'Man', 'race': {'asian': 2.1182747557759285, 'indian': 1.027565449476242, 'black': 0.1359685673378408, 'white': 69.29574608802795, 'middle eastern': 16.584493219852448, 'latino hispanic': 10.8379565179348}, 'dominant_race': 'white', 'emotion': {'angry': 0.8022463880479336, 'disgust': 0.0017378881238983013, 'fear': 12.73806244134903, 'happy': 0.08577692788094282, 'sad': 84.92135405540466, 'surprise': 3.237812151724029e-06, 'neutral': 1.450817845761776}, 'dominant_emotion': 'sad'}}
# nsfw_frames = [{'nsfw': 'Female Breast - Covered Female Breast - Covered ', 'file': 'keyframe-00003.jpg'}]
#
# data_frame = {}
# for i in range(len(i_frame)):
#     data_frame[str(i_frame[i])] = [
#         # {'frame_second': i_frame_seconds[i]},
#         {'frame': frames[i]},
#         # {'sub': ''},
#         # {'unique_frame': False},
#         # {'desc_frame': []},
#         # {'keywords': []},
#         # {'suss_nsfw': False},
#         # {'frame_faces': []},
#         {'nsfw': False},
#         {'nsfw_content': ''}
#     ]
#
#     for frame in nsfw_frames:
#         # print(frame['file'])
#         if frames[i] == frame['file']:
#             print(frame)
#             data_frame[str(i_frame[i])][1]['nsfw'] = True  # index!!!!!
#             data_frame[str(i_frame[i])][2]['nsfw_content'] = frame['nsfw']  # index!!!!!
#
# print(data_frame)


