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
import get_i_frames


def load_from_db(link):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['urldb']
    collection = db['mongourls']

    yt = YouTube(link)
    fps = collection.find_one({'id': yt.video_id})['fps']
    return fps


def make_time_i_frame(i_frame, fps=30):
    i_frame_seconds = []
    for i in i_frame:
        i_frame_seconds.append(i // fps)
        # print(i // fps)
    return i_frame_seconds


def save_to_db(data_frame, link):
    yt = YouTube(link)

    client = MongoClient('mongodb://localhost:27017/')
    db = client['urldb']
    collection = db['mongourls']

    video_info = {}
    video_info['data_frame'] = data_frame
    collection.update_one({'id': yt.video_id}, {'$set': video_info})


def create_data_frame(frames, i_frame, i_frame_seconds):
    data_frame = {}

    for i in range(len(i_frame)):
        data_frame[str(i_frame[i])] = [{'frame_second': i_frame_seconds[i]}, {'frame': frames[i]}]
    print(data_frame)
    return data_frame


def makeFrames(link):
    yt = YouTube(link)
    itag = 18
    # itag = list((yt.streams.order_by('resolution').desc().itag_index).keys())[0]  # Самый большой поток по разрешению

    path_folder = f"views/{yt.video_id}"

    if not os.path.exists(path_folder):
        os.mkdir(path_folder)
    else:
        print(f'{path_folder} folder already exists.')

    if yt.age_restricted:
        print('18+')
        info = yt_dlp_info.get_info_dlp(link)
        for i in info['formats']:
            if 'format_id' in i:
                if i['format_id'] == str(itag):
                    url = i['url']
                    # print(i['url'])

    else:
        url = YouTube(link).streams.get_by_itag(itag).url

    frames = os.listdir(path_folder)

    process_call_str = f'ffmpeg -i "{url}" -vf select="eq(pict_type\,PICT_TYPE_I)" -vsync 2 -f image2 {path_folder}/keyframe-%05d.jpg'
    status = subprocess.check_call(process_call_str, shell=True)
    return frames


def process_links(links):
    for link in links:
        frames = makeFrames(link)
        print(frames)
        i_frame = get_i_frames.get_i_keyframes(link)
        print(i_frame)
        fps = load_from_db(link)
        print(fps)
        i_frame_seconds = make_time_i_frame(i_frame, fps)
        print(i_frame_seconds)
        # i_frame = [0, 43, 89, 116, 173, 210, 253, 255, 284, 339, 388, 415, 457, 492, 511, 568, 604, 640, 663, 700, 733, 761]
        # i_frame_seconds = [0, 1, 3, 4, 6, 8, 10, 10, 11, 13, 15, 16, 18, 19, 20, 22, 24, 25, 26, 28, 29, 30]
        # frames = ['keyframe-00001.jpg', 'keyframe-00002.jpg', 'keyframe-00003.jpg', 'keyframe-00004.jpg', 'keyframe-00005.jpg', 'keyframe-00006.jpg', 'keyframe-00007.jpg', 'keyframe-00008.jpg', 'keyframe-00009.jpg', 'keyframe-00010.jpg', 'keyframe-00011.jpg', 'keyframe-00012.jpg', 'keyframe-00013.jpg', 'keyframe-00014.jpg', 'keyframe-00015.jpg', 'keyframe-00016.jpg', 'keyframe-00017.jpg', 'keyframe-00018.jpg', 'keyframe-00019.jpg', 'keyframe-00020.jpg', 'keyframe-00021.jpg', 'keyframe-00022.jpg']

        data_frame = create_data_frame(frames, i_frame, i_frame_seconds)
        save_to_db(data_frame, link)


        # video_info = {}
        # width = collection.find_one({'id': yt.video_id})['width']
        # height = collection.find_one({'id': yt.video_id})['height']
        # make_screenlist(link, i_frame_seconds, width, height)
        #
        # video_info['screenlist_url'] = f'out/{yt.video_id}.jpg'
        # video_info['i_frame_seconds'] = i_frame_seconds
        # video_info['screenlist'] = True
        # collection.update_one({'id': yt.video_id}, {'$set': video_info})


field = 'screenlist'
links = load_mongoDB_to_links.load_mongo_data_url(field)
process_links(links)
print(links, 'processed')



