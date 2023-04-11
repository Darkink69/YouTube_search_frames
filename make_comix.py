from pytube import YouTube
from pytube import Search
from pytube import Playlist
from pytube import Channel
import ffmpeg
import ffprobe
import json
import codecs
import subprocess
import sys
import os
from ffprobe import FFProbe
import cv2
from pymongo import MongoClient
import yt_dlp_info
import load_mongoDB_to_links
import get_from_mongoDB
import get_i_frames
import make_frames
import load_subs


def make_time_i_frame(i_frame, fps=30):
    i_frame_seconds = []
    for i in i_frame:
        i_frame_seconds.append(i // fps)
        # print(i // fps)
    return i_frame_seconds


def save_to_db(data_frame, id, type_subs):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['urldb']
    collection = db['mongourls']

    video_info = {}
    video_info['data_frame'] = data_frame
    video_info['type_subs'] = type_subs
    video_info['screencomix'] = True
    collection.update_one({'id': id}, {'$set': video_info})


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


def create_data_frame(frames, i_frame, i_frame_seconds, subs_on_frames):
    data_frame = {}
    for i in range(len(i_frame)):
        data_frame[str(i_frame[i])] = [
            {'frame_second': i_frame_seconds[i]},
            {'frame': frames[i]},
            {'sub': ''}
        ]
        # print(i_frame[i])
        for sub in subs_on_frames:
            if i_frame[i] == sub:
                data_frame[str(i_frame[i])][2]['sub'] = subs_on_frames[sub]

    # print(data_frame)
    return data_frame


def process_ids(ids):
    for id in ids:

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
        print(len(frames), 'i_frames.')

        i_frame = get_i_frames.get_i_keyframes(url)
        print(i_frame)

        field = 'fps'
        fps = get_from_mongoDB.load_mongo_data(id, field)[0]
        print(fps)

        i_frame_seconds = make_time_i_frame(i_frame, fps)
        print(i_frame_seconds)

        print('Loading subtitles..')
        field = 'subs'
        raw_subs = get_from_mongoDB.load_mongo_data(id, field)
        lang = 'Russian'
        subs, type_subs = load_subs.get_subs_from_url(raw_subs, lang)
        print(type_subs)

        subs_on_frames = sub_to_frame(subs, i_frame, fps)
        print(subs_on_frames)

        data_frame = create_data_frame(frames, i_frame, i_frame_seconds, subs_on_frames)
        save_to_db(data_frame, id, type_subs)


field = 'screencomix'
ids = load_mongoDB_to_links.load_mongo_data_url(field)
process_ids(ids)
print(ids, 'processed')

