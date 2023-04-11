from pytube import YouTube
import ffmpeg
import ffprobe
import json
import codecs
import subprocess
import sys
import os
import urllib.request
import cv2
from pymongo import MongoClient
import yt_dlp_info
import load_mongoDB_to_links
import get_from_mongoDB


def desc_text(id_desc):
    # fields = ['categories', 'title', 'description', 'keywords']
    # id_desc = []
    #
    # for field in fields:
    #     result = get_from_mongoDB.load_mongo_data(id, field)[0]
    #     id_desc.append(result)

    print(id_desc)
    bad_words = ['a', 'the', 'of', 'and', 'from', 'to', 'that', 'with', 'is', 'by', 'in', 'on', '.', '?', ',', '!',
                 'are', 'at', 'it', 'front', '[', ']', '(', ')', '-', '—', '–', 'an', 'for', 'into', 'am', '', '"', '`',
                 "'", "'s", 'there', 'has', 'who', 'his', 'I', '&', '|', '/', '//', ':', ';', '#', '➝', '•', '→',
                 'я', 'и', 'в', 'на', 'под', 'над', 'с', 'а', 'не', 'до', 'это', 'по', 'или', 'еще', 'из', 'этих',
                 'как', 'что', 'все', 'эти', 'этом', 'мы', 'они', 'его', 'чем', 'был', 'он', 'всей', 'от', 'для',
                 'нет', 'Нет', 'были', 'к', 'о', 'можно', 'об', 'самом', 'какие', 'них', 'вы', 'точно', 'вам',
                 'какой', 'за', 'ты', 'свой', 'свои', 'так', 'чтобы', 'вообще', 'так', 'между', 'которые', 'меня',
                 'когда', 'сам', 'свое', 'этой', 'кто', 'где', 'теперь', 'но', 'то', 'моем', 'про', 'всегда', 'кого',
                 'кем', 'меня', 'какое', 'этого', 'мой', 'том', 'тебе', 'уже', 'ещё', 'нас', 'будет', 'через',
                 'откуда', 'которыми', 'ничего', 'если', 'бы', 'там', 'сейчас', 'при', 'ради', 'моего', 'есть', 'тд.',
                 'тут', 'здесь', 'будут', 'какую', 'чего', 'себя', 'своей', 'твои', 'со', 'наши', 'ли', 'у', 'своего',
                 'почему', 'своими', 'кому', 'перед', 'нами', 'можем', 'может', 'какого-то', 'такое', 'зачем', 'такие',
                 'которых', 'нужно', 'же', 'всё', 'самое', 'самых', 'конечно', 'каких', 'бывает', 'свою', 'нашу',
                 'сможет', 'надо', 'каком', 'чаще', 'чаще', 'всего', 'без', 'нашего', 'во', 'также', 'нашей', 'такая',
                 'вас', 'быть', 'другая', 'чтоб', 'всю', 'очень', 'какого-нибудь', 'который', 'когда-нибудь', 'опять',
                 'вне', 'их', 'которая', 'всем', 'можете', 'после', 'tiktok', 'telegram', 'него', 'наш', 'которое',
                 'итак', 'instagram', 'такое', 'такого', 'как']

    signs = ['.', ',', '&', '!', '?', '/', '@', '#', '$', '%', '*', '(', ')', ':', ';', '"', '«', '»', '[', ']', '+']

    # '\U0001f449' '\xe9' \U0001f31f

    count_tags = {}
    unique_tags = []
    all_words = []

    for i in id_desc:
        if type(i) == list:
            words = ' '.join(map(str, i)).lower().replace("\n", " ").split(' ')
        else:
            words = i.lower().replace("\n", " ").split(' ')

        for key in words:
            if key not in bad_words and 'https://' not in key and 'http://' not in key:
                if key[-1] in signs:
                    key = key[:-1]
                if key[0] in signs:
                    key = key[1:]
                all_words.append(key)

        for key in all_words:
            if key not in unique_tags:
                unique_tags.append(key)

    # print(all_words)
    print(unique_tags)
    print(len(unique_tags))

    count = 1
    for word in all_words:
        if word not in count_tags:
            count_tags[word] = count
        else:
            count = count_tags[word] + 1
            count_tags[word] = count

    sorted_words = dict(sorted(count_tags.items(), key=lambda item: item[1]))

    tolerance_keys = 20
    id_desc_tags = list(sorted_words.keys())[-tolerance_keys:][::-1]

    print(id_desc_tags)
    return id_desc_tags, unique_tags


def disc_video(ids):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['urldb']
    collection = db['mongourls']

    for id in ids:
        print(f'https://youtu.be/{id}')
        video_info = {}
        # try:
        #     yt = YouTube(f'https://youtu.be/{id}')
        # except BaseException:
        #     print('Pytube не работает :(')
        try:
            info = yt_dlp_info.get_info_dlp(f'https://youtu.be/{id}')
        except BaseException:
            print('yt_dlp не сработал :( Надо попробовать позже..')


        # Разберем на части всё info
        # for i in dict.keys(info):
        #     print(i, info[i])

        prev_img = []
        prev_video = {}

        for i in info['thumbnails']:
            if i['id'] == '14':
                prev_img.append(i['url'])

        for i in info['formats']:
            if 'fragments' in i:
                for j in i['fragments']:
                    prev_img.append(j['url'])

        for i in info['formats']:
            if i['format_id'] == '18':
                prev_video['url_medium'] = i['url']
                prev_video['filesize'] = i['filesize']
                prev_video['format_note'] = i['format_note']
                prev_video['fps'] = i['fps']
                prev_video['audio_channels'] = i['audio_channels']
                prev_video['height'] = i['height']
                prev_video['width'] = i['width']
                prev_video['video_ext'] = i['video_ext']

        hd_video = {}
        k4_video = {}
        url_hd = []
        url_4k = []
        format_id_hd = ['399', '299', '303', '22', '136', '247', '398', '298', '302']
        format_id_4k = ['571', '401', '315', '400', '308', '313', '271']

        for i in info['formats']:
            # print(i)
            if i['format_id'] in format_id_hd:
                hd_video['url'] = i['url']
                hd_video['filesize'] = i['filesize']
                hd_video['format_note'] = i['format_note']
                hd_video['fps'] = i['fps']
                hd_video['audio_channels'] = i['audio_channels']
                hd_video['height'] = i['height']
                hd_video['width'] = i['width']
                hd_video['video_ext'] = i['video_ext']
                url_hd.append(hd_video)
                prev_video['hd_video'] = url_hd

            if i['format_id'] in format_id_4k:
                k4_video['url'] = i['url']
                k4_video['filesize'] = i['filesize']
                k4_video['format_note'] = i['format_note']
                k4_video['fps'] = i['fps']
                k4_video['audio_channels'] = i['audio_channels']
                k4_video['height'] = i['height']
                k4_video['width'] = i['width']
                k4_video['video_ext'] = i['video_ext']
                url_4k.append(k4_video)
                prev_video['4k_video'] = url_4k


        subs = {}
        sub = []
        for i in info['subtitles']:
            if i in ['ru', 'en']:
                sub.append(info['subtitles'][i])
                subs['sub_prof'] = sub

        for i in info['automatic_captions']:
            if i in ['ru', 'en']:
                sub.append(info['automatic_captions'][i])
                subs['sub_auto'] = sub

        # if yt.age_restricted == False:
        #     print('18+')

        video_info['url'] = f'https://youtu.be/{id}'
        video_info['title'] = info['title']
        video_info['description'] = info['description']
        video_info['keywords'] = info['tags']
        video_info['thumbnail_url'] = info['thumbnail']
        video_info['prev_img'] = prev_img
        video_info['length'] = info['duration']
        video_info['channel_url'] = info['uploader_url']
        video_info['author'] = info['uploader']
        # video_info['age_restricted'] = True
        video_info['fps'] = prev_video['fps']
        video_info['screenlist_url_small'] = info['formats'][0]['url']
        video_info['prev_video'] = prev_video
        video_info['url_video'] = prev_video['url_medium']
        video_info['subs'] = subs
        video_info['view_count'] = info['view_count']
        video_info['categories'] = info['categories']
        try:
            video_info['like_count'] = info['like_count']
        except BaseException:
            pass
        video_info['channel_follower_count'] = info['channel_follower_count']
        video_info['upload_date'] = info['upload_date']
        video_info['playlist'] = info['playlist']
        video_info['playlist_index'] = info['playlist_index']
        video_info['duration_string'] = info['duration_string']

        id_desc = [info['categories'], info['title'], info['description'], info['tags']]
        id_desc_tags, unique_tags = desc_text(id_desc)
        video_info['id_desc_tags'] = id_desc_tags
        video_info['unique_tags'] = unique_tags

        video_info['discription'] = True
        collection.update_one({'id': id}, {'$set': video_info})




field = 'discription'
ids = load_mongoDB_to_links.load_mongo_data_url(field)
disc_video(ids)

print(ids, 'processed')




