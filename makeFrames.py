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

# link = 'https://youtu.be/Qd1uC7K3KaE'

def load_mongo_data_url():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['urldb']
    collection = db['mongourls']
    items = collection.find()
    links = []
    for item in items:
        if not item['screencomix']:
            links.append(item['url'])
    return links


def makeFrames(link, path_folder):
    yt = YouTube(link)
    itag = 18
    # itag = list((yt.streams.order_by('resolution').desc().itag_index).keys())[0]  # Самый большой поток по разрешению
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

    # url = filename
    process_call_str = f'ffmpeg -i "{url}" -vf select="eq(pict_type\,PICT_TYPE_I)" -vsync 2 -f image2 {path_folder}/keyframe-%05d.jpg'
    status = subprocess.check_call(process_call_str, shell=True)


def save_to_db(links):

    client = MongoClient('mongodb://localhost:27017/')
    db = client['urldb']
    collection = db['mongourls']

    for link in links:
        yt = YouTube(link)
        path_folder = f"views/{yt.video_id}"

        if not os.path.exists(path_folder):
            os.mkdir(path_folder)
        else:
            print(f'{path_folder} folder already exists.')

        makeFrames(link, path_folder)

        content = os.listdir(path_folder)

        video_info = {}
        video_info['screencomix'] = True
        video_info['path_folder'] = path_folder
        video_info['frame'] = content
        collection.update_one({'id': yt.video_id}, {'$set': video_info})


links = load_mongo_data_url()
save_to_db(links)

