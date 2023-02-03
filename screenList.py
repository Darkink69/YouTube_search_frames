from pytube import YouTube
from pytube import Search
from pytube import Playlist
from pytube import Channel
import ffmpeg
import ffprobe
import json
import codecs
from ffpyplayer.player import MediaPlayer
import subprocess
import sys
import os
from ffprobe import FFProbe
import cv2
from pymongo import MongoClient
import load_mongoDB_to_links


fps = 25
# links = ['https://youtu.be/OKgtA3h8WB8']


# def load_mongo_data_url():
#     client = MongoClient('mongodb://localhost:27017/')
#     db = client['urldb']
#     collection = db['mongourls']
#     items = collection.find()
#     links = []
#     for item in items:
#         if not item['screenlist']:
#             links.append(item['url'])
#     return links


def make_screenlist(link, i_frame_seconds, width, height):
    url = YouTube(link).streams.get_by_itag(18).url
    out_name_file = str(YouTube(link).video_id)
    # print(len(i_frames))

    w_tile = 5 if len(i_frame_seconds) < 50 else 10
    h_tile = len(i_frame_seconds) // w_tile + 1

    w = 170
    h = w * height / width
    # process_call_str = f'ffmpeg -i "{url}" -vf select="gt(scene\,0.2)",scale=200:120,tile=8x6 -frames:v 1 -y views/out/{out_name_file}.png'
    process_call_str = f'ffmpeg -i "{url}" -vf select="eq(pict_type\,I)",scale={w}:{h},tile={w_tile}x{h_tile} -frames:v 1 -y views/out/{out_name_file}.jpg'

    status = subprocess.check_call(process_call_str, shell=True)


def get_frame_types(video_fn):
    command = 'ffprobe -v error -show_entries frame=pict_type -of default=noprint_wrappers=1'.split()
    out = subprocess.check_output(command + [video_fn]).decode()
    frame_types = out.replace('pict_type=', '').split()
    return zip(range(len(frame_types)), frame_types)


def get_i_keyframes(link):
    # yt = YouTube(link)
    # itag = list((yt.streams.order_by('resolution').desc().itag_index).keys())[0]  # Самый большой поток по разрешению
    url = YouTube(link).streams.get_by_itag(18).url
    # aurl = YouTube(link).streams.get_by_itag(18).url
    frame_types = get_frame_types(url)
    i_frames = [x[0] for x in frame_types if x[1] == 'I']
    # print(i_frames)
    return i_frames


def make_time_i_frame(i_frame, fps):
    i_frame_seconds = []
    for i in i_frame:
        i_frame_seconds.append(i // fps)
        # print(i // fps)
    return i_frame_seconds


def process_links(links):
    client = MongoClient('mongodb://localhost:27017/')
    db = client['urldb']
    collection = db['mongourls']

    for link in links:
        video_info = {}
        yt = YouTube(link)
        i_frame = get_i_keyframes(link)
        i_frame_seconds = make_time_i_frame(i_frame, fps)
        print(i_frame_seconds)

        width = collection.find_one({'id': yt.video_id})['width']
        height = collection.find_one({'id': yt.video_id})['height']
        make_screenlist(link, i_frame_seconds, width, height)

        video_info['screenlist_url'] = f'out/{yt.video_id}.jpg'
        video_info['i_frame_seconds'] = i_frame_seconds
        video_info['screenlist'] = True
        collection.update_one({'id': yt.video_id}, {'$set': video_info})


field = 'screenlist'
links = load_mongoDB_to_links.load_mongo_data_url(field)
process_links(links)
print(links, 'processed')


