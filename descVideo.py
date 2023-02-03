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


# def load_mongo_data_url():
#     client = MongoClient('mongodb://localhost:27017/')
#     db = client['urldb']
#     collection = db['mongourls']
#     items = collection.find()
#     links = []
#     for item in items:
#         if not item['discription']:
#             links.append(item['url'])
#     return links


def disc_video(links):
    video_info_all = []
    client = MongoClient('mongodb://localhost:27017/')
    db = client['urldb']
    collection = db['mongourls']

    for i in links:
        video_info = {}
        yt = YouTube(i)
        info = yt_dlp_info.get_info_dlp(i)

        ids = info['formats']
        for id in ids:
            if 'format_id' in id:
                if id['format_id'] == '18':
                    print(id['url'])
                    url_video = id['url']

        if yt.age_restricted:
            print('18+')

            video_info['url'] = i
            video_info['title'] = info['title']
            # video_info['description'] = yt.description
            # video_info['keywords'] = yt.keywords
            # video_info['thumbnail_url'] = yt.thumbnail_url
            # video_info['length'] = yt.length
            # video_info['channel_url'] = yt.channel_url
            # video_info['author'] = yt.author
            # video_info['age_restricted'] = True
            # video_info['width'] = yt.vid_info['streamingData']['formats'][1]['width']
            # video_info['height'] = yt.vid_info['streamingData']['formats'][1]['height']
            # video_info['fps'] = yt.vid_info['streamingData']['formats'][1]['fps']
            video_info['screenlist_url_small'] = info['formats'][0]['url']

            video_info['discription'] = True
            collection.update_one({'id': yt.video_id}, {'$set': video_info})

        else:
            video_info['id'] = yt.video_id
            video_info['url'] = i
            video_info['title'] = yt.title
            video_info['description'] = yt.description
            video_info['keywords'] = yt.keywords
            video_info['thumbnail_url'] = yt.thumbnail_url
            video_info['length'] = yt.length
            video_info['channel_url'] = yt.channel_url
            video_info['author'] = yt.author
            video_info['age_restricted'] = yt.age_restricted
            video_info['width'] = yt.vid_info['streamingData']['formats'][1]['width']
            video_info['height'] = yt.vid_info['streamingData']['formats'][1]['height']
            video_info['fps'] = yt.vid_info['streamingData']['formats'][1]['fps']
            video_info['screenlist_url_small'] = info['formats'][0]['url']
            video_info['url_video'] = url_video


            video_info['discription'] = True
            collection.update_one({'id': yt.video_id}, {'$set': video_info})

field = 'discription'
links = load_mongoDB_to_links.load_mongo_data_url(field)
disc_video(links)

print(links, 'processed')

