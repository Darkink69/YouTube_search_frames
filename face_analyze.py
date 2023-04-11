from deepface import DeepFace
import json


# img = '2.jpg'


def face_analyze(path_folder, frame):
    try:
        result_dict = DeepFace.analyze(img_path=f'{path_folder}/{frame}', actions=['age', 'gender', 'race', 'emotion'])

        # print(f'[+] Age: {result_dict.get("age")}')
        # print(f'[+] Gender: {result_dict.get("gender")}')
        # print('[+] Race:')
        #
        # for k, v in result_dict.get('race').items():
        #     print(f'{k} - {round(v, 2)}%')
        #
        # print('[+] Emotions:')
        #
        # for k, v in result_dict.get('emotion').items():
        #     print(f'{k} - {round(v, 2)}%')

        # print(result_dict)
        return result_dict

    except Exception as _ex:
        return _ex


# face_analyze(img)
