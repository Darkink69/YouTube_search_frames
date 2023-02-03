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



link = 'https://youtu.be/SJwcIsy4XF4'
itag = 18  # номер потока, 137 с разрешением 1080p, 22 - 720p, 43 или 18 - 360p
myFps = 1 / 15  # каждые 15 секунд
mySearch = 'альманах вокруг света'
filename = '1.webm'

yt = YouTube(link).vid_info['videoDetails']
print(yt)
print(YouTube(link).age_restricted)

# dict_keys(['responseContext', 'playabilityStatus', 'videoDetails', 'trackingParams', 'playerSettingsMenuData'])

def searchVideo(mySearch):
    allResults = []
    s = Search(mySearch)
    # print(s.completion_suggestions)
    print(f'Найдено - {len(s.results)} видео')
    for i in s.results:
        result = 'https://youtu.be/' + str(i)[41:-1]
        allResults.append(result)
    print(allResults)
    return allResults


def resultsSearch(allResults):
    for i in allResults:
        print(i)
        descVideo(i)
        print('========================================================================')


def descVideo(allResults):
    video_info_all = []

    for i in allResults:
        video_info = {}
        yt = YouTube(i)
        # yt.bypass_age_gate()
        # print(yt.vid_info)
        video_info['id'] = yt.video_id
        video_info['link'] = i
        video_info['title'] = yt.title
        video_info['description'] = yt.description
        video_info['keywords'] = yt.keywords
        video_info['thumbnail_url'] = yt.thumbnail_url
        video_info['length'] = yt.length
        video_info['channel_url'] = yt.channel_url
        video_info['author'] = yt.author
        video_info['age_restricted'] = yt.age_restricted

        # video_info['metadata'] = yt.metadata
        # video_info['vid_info'] = str(yt.vid_info)

        print(f'Продолжительность - {yt.length // 60 // 60}:{yt.length // 60 % 60}:{yt.length % 60}')
        video_info_all.append(video_info)

        with codecs.open('1.json', 'w', encoding='utf-8') as f:
            json.dump(video_info_all, f, indent=4, ensure_ascii=False)


def makeFrames(link, filename):
    yt = YouTube(link)
    try:
        # itag = list((yt.streams.order_by('resolution').desc().itag_index).keys())[0]  # Самый большой поток по разрешению
        itag = 18
    except:
        print('Неверная ссылка')
        print() if yt.age_restricted == 'true' else print('Фильм с возрастным ограничением, невозможно обработать')


    # print(url)

    url = YouTube(link).streams.get_by_itag(itag).url
    url = filename

    process_call_str = f'ffmpeg -i "{url}" -vf select="eq(pict_type\,PICT_TYPE_I)" -vsync 2 -f image2 D:\\w_edu_eng\\OSPanel\\domains\\express_2\\views\\out\\keyframe-%05d.png'
    status = subprocess.check_call(process_call_str, shell=True)


def make_screenshots(link, filename, i_frames):
    yt = YouTube(link)
    # itag = list((yt.streams.order_by('resolution').desc().itag_index).keys())[0]  # Самый большой поток по разрешению
    url = YouTube(link).streams.get_by_itag(18).url
    # url = filename
    out_name_file = str(YouTube(link).video_id)
    print(len(i_frames))

    w = 5 if len(i_frames) < 50 else 10
    h = len(i_frames) // w + 1
    # process_call_str = f'ffmpeg -i "{url}" -vf select="gt(scene\,0.2)",scale=200:120,tile={w}x{h} -frames:v 1 -y out/{out_name_file}.png'
    process_call_str = f'ffmpeg -i "{url}" -vf select="eq(pict_type\,I)",scale=200:120,tile={w}x{h} -frames:v 1 -y out/{out_name_file}.png'

    status = subprocess.check_call(process_call_str, shell=True)


def downloadVideoQuick(link):
    yt = YouTube(link)
    streams = yt.streams
    # video_best = streams.order_by('resolution').desc().first()
    # audio_best = streams.filter(only_audio=True).desc().first()
    video = streams.filter(progressive=True).desc().first()
    video.download()
    # audio_best.download()



def txt_to_list():
    with open('mults_4.txt', 'r', encoding='utf-8') as f:
        text = f.readlines()
        list_url_time = [x.strip().split() for x in text]
        return list_url_time


def download_fragment(link, ss='00:00:00', to='00:02:25', item_video='123'):

    yt = YouTube(link)
    itag = list((yt.streams.order_by('resolution').desc().itag_index).keys())[0]  # Самый большой поток по разрешению
    url = YouTube(link).streams.get_by_itag(itag).url
    aurl = YouTube(link).streams.get_by_itag(18).url
    out_name_file = str(YouTube(link).video_id)

    # ss = '00:00:40'
    # to = '00:01:00'
    # process_call_str = f'ffmpeg -ss {ss} -to {to} -i "{url}" -acodec aac -b:a 192k -avoid_negative_ts make_zero out.mp4'
    process_call_str = f'ffmpeg -ss {ss} -to {to} -i "{url}" -ss {ss} -to {to} -i "{aurl}" -acodec aac -b:a 192k -avoid_negative_ts make_zero -map 0:v:0 -map 1:a:0 out/{item_video}{out_name_file}.mp4'
    status = subprocess.check_call(process_call_str, shell=True)


def download_serial(list_url_time):
    for video in list_url_time:
        link = video[0]
        ss = video[1]
        to = video[2]
        print(f'Загрузка видео {list_url_time.index(video) + 1} / {len(list_url_time)}')
        try:
            item_video = str(list_url_time.index(video) + 1) + '__'
            download_fragment(link, ss, to, item_video)
        except:
            print('Ошибка загрузки видео -', list_url_time.index(video) + 1, video)


def get_file_info(filename):

    # Local file
    metadata = FFProbe(filename)

    # Video stream
    # metadata=FFProbe('http://some-streaming-url.com:8080/stream')

    print(metadata)
    for stream in metadata.streams:
        if stream.is_video():
            print(f'Stream contains {stream.frames()} frames.')
        print('fps -', str(metadata.video).split(',')[1])
        fps = int(str(metadata.video).split(',')[1])
    return fps


def get_frame_types(video_fn):
    command = 'ffprobe -v error -show_entries frame=pict_type -of default=noprint_wrappers=1'.split()
    out = subprocess.check_output(command + [video_fn]).decode()
    frame_types = out.replace('pict_type=', '').split()
    return zip(range(len(frame_types)), frame_types)


def get_i_keyframes(link):
    yt = YouTube(link)
    # itag = list((yt.streams.order_by('resolution').desc().itag_index).keys())[0]  # Самый большой поток по разрешению
    url = YouTube(link).streams.get_by_itag(18).url
    # aurl = YouTube(link).streams.get_by_itag(18).url
    frame_types = get_frame_types(url)
    i_frames = [x[0] for x in frame_types if x[1] == 'I']
    print(i_frames)
    return i_frames


def timecode_to_json(i_frames, fps):
    start_second = []
    print(i_frames)
    for i_frame in i_frames:
        start_second.append(i_frame // fps)
        # print(i_frame)
        with codecs.open('timecode.json', 'w', encoding='utf-8') as f:
            json.dump(start_second, f, indent=4, ensure_ascii=False)

    print(start_second)


def save_subtitle_txt(link):
    yt = YouTube(link)
    if len(yt.captions) == 0:
        print('Нет субтитров')
    else:
        print(len(yt.captions))
    if len(yt.captions) == 1:
        caption_lang = 'a.ru'
    else:
        caption_lang = 'ru'

    caption = yt.captions[caption_lang].xml_captions
    # print(caption)
    p_blocks = caption.split('<p')
    for p_block in p_blocks:
        if '<s' in p_block:
            time_sub_start = int(p_block.split()[0].split('"')[1])
            time_sub_dur = int(p_block.split()[1].split('"')[1])
            s = p_block.split('>')
            one_str = []
            for i in s:
                if '</s' in i:
                    one_str.append(i[:-3])
            print(time_sub_start, time_sub_dur, "".join(one_str))
        else:
            s = p_block.split('>')
            one_str = []
            for i in s:
                if '</p' in i:
                    one_str.append(i[:-3])
                    time_sub_start = int(p_block.split()[0].split('"')[1])
                    time_sub_dur = int(p_block.split()[1].split('"')[1])

                    print(time_sub_start, time_sub_dur, "".join(one_str))
    # with codecs.open(f'{yt.video_id}.txt', 'w', encoding='utf-8') as f:
    #     f.write(caption)


def load_mongo_data_url():
    client = MongoClient('mongodb://localhost:27017/')
    db = client['urldb']
    collection = db['mongourls']
    items = collection.find()
    links = []
    for item in items:
        links.append('https://' + item['url'])
    return links


# links = load_mongo_data_url()
# print(links)
# descVideo(links)

# fps = get_file_info(filename)
# i_frames = get_i_keyframes(link)
#
# timecode_to_json(i_frames, fps)

# makeFrames(link, filename)



# allResults = searchVideo(mySearch)
# descVideo(allResults)

# save_subtitle_txt(link)

# resultsSearch()

# downloadVideoQuick(link)
# download_fragment(link)
# descVideo(link)


# list_url_time = txt_to_list()
# download_serial(list_url_time)
# make_screenshots(link, filename, i_frames)


# грабит видеокарта
# ffmpeg -f gdigrab -framerate 30 -i desktop -c:v h264_nvenc -qp 0 output.mkv
#
# ffmpeg - f gdigrab - rtbufsize 100 M - framerate 30 - probesize 10 M - draw_mouse 1 - i desktop - c: v libx264 - r 30 - preset ultrafast - tune zerolatency - crf 25 - pix_fmt yuv420p out.mp4
# запись экрана со звуком
# ffmpeg -f dshow -i audio="@device_cm_{33D9A762-90C8-11D0-BD43-00A0C911CE86}\wave_{A148FE0E-AF21-4217-899B-6FB4FDD0D616}" -f gdigrab -rtbufsize 100M -framerate 30 -probesize 10M -draw_mouse 1 -i desktop -acodec aac -c:v libx264 -r 30 -preset ultrafast -tune zerolatency -crf 25 -pix_fmt yuv420p out.mp4

#  ffmpeg -i 1.mp4 -vf select='eq(pict_type\,I)' -vsync 2 -f image2 out/keyframe-%02d.png
#  ffmpeg -i 1.mp4 -ss 00:01:00 -to 00:02:00 -vf select='eq(pict_type\,I)' -vsync 2 -f image2 out/keyframe-%02d.png
# ffprobe -v quiet -print_format json -show_format -show_streams 1.mp4 > 1.json
# ffmpeg -i 2.mp4 -ss 00:00:10.000 -vframes 1 output2.png / сохраняем кадр с тысячными долями секунды
# ffmpeg -i 1.mp4 -vf select='gt(scene\,0.2)',scale=200:120,tile=8x6 -frames:v 1 preview.png
# к ссылке добавляем в секундах:   ?t=1430

# process_call_str = 'ffmpeg -ss {1} -to {2} -i "{0}"'/
#                             '-acodec aac -b:a 192k -avoid_negative_ts make_zero "{3}"'
#                             .format(str(url), str(ss), str(t), download_file_path)

# f'ffmpeg -ss {ss} -to {to} -i "{url}" -ss {ss} -to {to} -i "{aurl}" -acodec aac -b:a 192k -avoid_negative_ts make_zero -map 0:v:0 -map 1:a:0 out.mp4'

# f'ffmpeg -ss {ss} -to {to} -i "{url}" -acodec aac -b:a 192k -avoid_negative_ts make_zero out.mp4'

# ffmpeg -i 1.mp4 -ss 00:01:00 -to 00:02:00 -c copy cut.mp4
# ffmpeg -i "1.mp4" -t 15  -vf select="eq(pict_type\,PICT_TYPE_I)" -vsync 2  -s 160x90 -f image2 thumbnails-%02d.jpeg -loglevel debug 2>&1| for /f "tokens=4,8,9 delims=. " %d in ('findstr "pict_type:I"') do echo %d %e.%f>>"keyframe_list.txt"

#  ffprobe -i 1.mp4 -select_streams v -show_frames -show_entries frame=pict_type -of csv > frame_index.txt
# process_call_str = f'ffprobe - i 1.mp4 - select_streams v - show_frames - show_entries frame = pict_type - of csv | findstr "pict_type" | cut - d ":" - f 1 > frame_index.txt'
# ffprobe -i 1.mp4 -show_frames !!!!!!



# yt = YouTube(link).vid_info['videoDetails']['thumbnail']['thumbnails'][1]['width']
# print(yt)
# {'videoId': 'f89UBRSK5wM',
# 'title': 'Серенада Пьеро - Приключения Буратино (1975) 4K',
# 'lengthSeconds': '140',
# 'channelId': 'UCRcxY8C43vV7kj-4zc7fZ8A',
# 'isOwnerViewing': False,
# 'shortDescription': 'Цифровая реставрация',
# 'isCrawlable': True,
# 'thumbnail':
# {'thumbnails':
#   [
#       {'url': 'https://i.ytimg.com/vi/f89UBRSK5wM/default.jpg?sqp=-oaymwEkCHgQWvKriqkDGvABAfgBsgeAAtAFigIMCAAQARhEIEgoZTAP&rs=AOn4CLBLXFDPPEayJnGTyvMUQhVoEwfq5g', 'width': 120, 'height': 90},
#       {'url': 'https://i.ytimg.com/vi/f89UBRSK5wM/mqdefault.jpg?sqp=-oaymwEmCMACELQB8quKqQMa8AEB-AGyB4AC0AWKAgwIABABGEQgSChlMA8=&rs=AOn4CLARLgs4nz1fdfG6o7Kae6GKxC53LA', 'width': 320, 'height': 180},
#       {'url': 'https://i.ytimg.com/vi/f89UBRSK5wM/hqdefault.jpg?sqp=-oaymwEmCOADEOgC8quKqQMa8AEB-AGyB4AC0AWKAgwIABABGEQgSChlMA8=&rs=AOn4CLD2WV4Jg7UkRnL2dAF7vbddMvWRaA', 'width': 480, 'height': 360},
#       {'url': 'https://i.ytimg.com/vi/f89UBRSK5wM/sddefault.jpg?sqp=-oaymwEmCIAFEOAD8quKqQMa8AEB-AGyB4AC0AWKAgwIABABGEQgSChlMA8=&rs=AOn4CLDnKQPPkpZ_j-nIXlbU_lJRxih6KQ', 'width': 640, 'height': 480}
#   ]},
# 'allowRatings': True,
# 'viewCount': '358',
# 'author': 'ReLive HD',
# 'isPrivate': False,
# 'isUnpluggedCorpus': False,
# 'isLiveContent': False}
#


# yt = YouTube(link).vid_info['streamingData']
# print(yt)

# {'expiresInSeconds': '21540',
# 'formats':
# [
# {'itag': 17,
# 'url': 'https://rr1---sn-gvnuxaxjvh-v8cz.googlevideo.com/videoplayback?expire=1671533241&ei=WT6hY_vdFo2zyQWYwqqADw&ip=92.125.255.100&id=o-AOz34mLnQWBtTjMz0e_ST17vpg8qv5zl4LwqsEC4Igum&itag=17&source=youtube&requiressl=yes&mh=Q8&mm=31%2C29&mn=sn-gvnuxaxjvh-v8cz%2Csn-n8v7znsl&ms=au%2Crdu&mv=m&mvi=1&pcm2cms=yes&pl=18&initcwndbps=1813750&vprv=1&mime=video%2F3gpp&gir=yes&clen=1262283&dur=140.155&lmt=1669980674310925&mt=1671511290&fvip=3&fexp=24001373%2C24007246&c=ANDROID&txp=5318224&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cgir%2Cclen%2Cdur%2Clmt&sig=AOq0QJ8wRQIgefdGDyrXh7uJDVNNgC6-EpGhkgYKHGcsRT5AFwGt6NoCIQCESs4epM7qitLEieWrlJ1WjyykvCnHUcEyScJOBxokTw%3D%3D&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpcm2cms%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRgIhAOkBUUXVKYtJ3JrNtOlvy8RcWQHOAb6AqH3zhl2VJfaEAiEA-iAd4QQ3eoTkDLWa5tg0rFcjv2_AX7RbOXB0DnOJ7Zs%3D',
# 'mimeType': 'video/3gpp; codecs="mp4v.20.3, mp4a.40.2"',
# 'bitrate': 72130,
# 'width': 176,
# 'height': 144,
# 'lastModified': '1669980674310925',
# 'contentLength': '1262283',
# 'quality': 'small',
# 'fps': 6,
# 'qualityLabel': '144p',
# 'projectionType': 'RECTANGULAR',
# 'averageBitrate': 72050,
# 'audioQuality': 'AUDIO_QUALITY_LOW',
# 'approxDurationMs': '140155',
# 'audioSampleRate': '22050', 'audioChannels': 1},

# {'itag': 18,
# 'url': 'https://rr1---sn-gvnuxaxjvh-v8cz.googlevideo.com/videoplayback?expire=1671533241&ei=WT6hY_vdFo2zyQWYwqqADw&ip=92.125.255.100&id=o-AOz34mLnQWBtTjMz0e_ST17vpg8qv5zl4LwqsEC4Igum&itag=18&source=youtube&requiressl=yes&mh=Q8&mm=31%2C29&mn=sn-gvnuxaxjvh-v8cz%2Csn-n8v7znsl&ms=au%2Crdu&mv=m&mvi=1&pcm2cms=yes&pl=18&initcwndbps=1813750&vprv=1&mime=video%2Fmp4&gir=yes&clen=6908173&ratebypass=yes&dur=140.109&lmt=1669980627569773&mt=1671511290&fvip=3&fexp=24001373%2C24007246&c=ANDROID&txp=5319224&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cgir%2Cclen%2Cratebypass%2Cdur%2Clmt&sig=AOq0QJ8wRQIgEbxFftLX3Yi8da9yD8gxaQeT2K9626RdQb6pXA7JIVYCIQDtgYP1QpV-kuArN79TEhiP8rudZQZaSqG9YtPBipjYBg%3D%3D&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpcm2cms%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRgIhAOkBUUXVKYtJ3JrNtOlvy8RcWQHOAb6AqH3zhl2VJfaEAiEA-iAd4QQ3eoTkDLWa5tg0rFcjv2_AX7RbOXB0DnOJ7Zs%3D',
#'mimeType': 'video/mp4;
# codecs="avc1.42001E, mp4a.40.2"',
# 'bitrate': 394639,
# 'width': 474,
# 'height': 360,
# 'lastModified': '1669980627569773',
# 'contentLength': '6908173',
# 'quality': 'medium',
# 'fps': 25,
# 'qualityLabel': '360p',
# 'projectionType': 'RECTANGULAR',
# 'averageBitrate': 394445,
# 'audioQuality': 'AUDIO_QUALITY_LOW',
# 'approxDurationMs': '140109',
# 'audioSampleRate': '44100',
# 'audioChannels': 2},
#
# {'itag': 22,
# 'url': 'https://rr1---sn-gvnuxaxjvh-v8cz.googlevideo.com/videoplayback?expire=1671533241&ei=WT6hY_vdFo2zyQWYwqqADw&ip=92.125.255.100&id=o-AOz34mLnQWBtTjMz0e_ST17vpg8qv5zl4LwqsEC4Igum&itag=22&source=youtube&requiressl=yes&mh=Q8&mm=31%2C29&mn=sn-gvnuxaxjvh-v8cz%2Csn-n8v7znsl&ms=au%2Crdu&mv=m&mvi=1&pcm2cms=yes&pl=18&initcwndbps=1813750&vprv=1&mime=video%2Fmp4&cnr=14&ratebypass=yes&dur=140.109&lmt=1669980928549539&mt=1671511290&fvip=3&fexp=24001373%2C24007246&c=ANDROID&txp=5318224&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cvprv%2Cmime%2Ccnr%2Cratebypass%2Cdur%2Clmt&sig=AOq0QJ8wRQIgR4DuvDVUR_dURT6AExqWe3ZzY76JId9IK_sj5ixgQ5gCIQCVSVkhm8OIZAK1awRhR0ZlGmx6qA0zSuXiNpnED5TIyA%3D%3D&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpcm2cms%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRgIhAOkBUUXVKYtJ3JrNtOlvy8RcWQHOAb6AqH3zhl2VJfaEAiEA-iAd4QQ3eoTkDLWa5tg0rFcjv2_AX7RbOXB0DnOJ7Zs%3D',
# 'mimeType': 'video/mp4; codecs="avc1.64001F, mp4a.40.2"',
# 'bitrate': 1427148, 'width': 948, 'height': 720, 'lastModified': '1669980928549539', 'quality': 'hd720', 'fps': 25, 'qualityLabel': '720p', 'projectionType': 'RECTANGULAR', 'audioQuality': 'AUDIO_QUALITY_MEDIUM', 'approxDurationMs': '140109', 'audioSampleRate': '44100', 'audioChannels': 2}
# ],
#
# 'adaptiveFormats':
# [
# {'itag': 313, 'url': 'https://rr1---sn-gvnuxaxjvh-v8cz.googlevideo.com/videoplayback?expire=1671533241&ei=WT6hY_vdFo2zyQWYwqqADw&ip=92.125.255.100&id=o-AOz34mLnQWBtTjMz0e_ST17vpg8qv5zl4LwqsEC4Igum&itag=313&source=youtube&requiressl=yes&mh=Q8&mm=31%2C29&mn=sn-gvnuxaxjvh-v8cz%2Csn-n8v7znsl&ms=au%2Crdu&mv=m&mvi=1&pcm2cms=yes&pl=18&initcwndbps=1813750&vprv=1&mime=video%2Fwebm&gir=yes&clen=160116204&dur=140.040&lmt=1669980959020066&mt=1671511290&fvip=3&keepalive=yes&fexp=24001373%2C24007246&c=ANDROID&txp=5319224&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cgir%2Cclen%2Cdur%2Clmt&sig=AOq0QJ8wRgIhAIu4Mwahss1UK4YnfAKXDAw8RZHNvLPLSpY2sALth85sAiEAp-N9FpzhdCJOYxqlQmJnWHaWNzNNAYvfEGxO4jDNo68%3D&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpcm2cms%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRgIhAOkBUUXVKYtJ3JrNtOlvy8RcWQHOAb6AqH3zhl2VJfaEAiEA-iAd4QQ3eoTkDLWa5tg0rFcjv2_AX7RbOXB0DnOJ7Zs%3D',
# 'mimeType': 'video/webm; codecs="vp9"',
# 'bitrate': 10174754,
# 'width': 2844,
# 'height': 2160,
# 'initRange': {'start': '0', 'end': '219'},
# 'indexRange': {'start': '220', 'end': '711'},
# 'lastModified': '1669980959020066',
# 'contentLength': '160116204',
# 'quality': 'hd2160',
# 'fps': 25,
# 'qualityLabel': '2160p',
# 'projectionType': 'RECTANGULAR',
# 'averageBitrate': 9146883,
# 'colorInfo':
# {'primaries': 'COLOR_PRIMARIES_BT709',
# 'transferCharacteristics': 'COLOR_TRANSFER_CHARACTERISTICS_BT709',
# 'matrixCoefficients': 'COLOR_MATRIX_COEFFICIENTS_BT709'},
# 'approxDurationMs': '140040'},

# {'itag': 271,
# 'url': 'https://rr1---sn-gvnuxaxjvh-v8cz.googlevideo.com/videoplayback?expire=1671533241&ei=WT6hY_vdFo2zyQWYwqqADw&ip=92.125.255.100&id=o-AOz34mLnQWBtTjMz0e_ST17vpg8qv5zl4LwqsEC4Igum&itag=271&source=youtube&requiressl=yes&mh=Q8&mm=31%2C29&mn=sn-gvnuxaxjvh-v8cz%2Csn-n8v7znsl&ms=au%2Crdu&mv=m&mvi=1&pcm2cms=yes&pl=18&initcwndbps=1813750&vprv=1&mime=video%2Fwebm&gir=yes&clen=78945369&dur=140.040&lmt=1669980995481638&mt=1671511290&fvip=3&keepalive=yes&fexp=24001373%2C24007246&c=ANDROID&txp=5319224&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cgir%2Cclen%2Cdur%2Clmt&sig=AOq0QJ8wRQIgSmCoNbdxOHfMjlmepgmjVSclPcYVmGeTCyXZ2rXUPxgCIQChECNOXYTBXClhLwI-_lJ1FPnq8-8Ner43Pf07qvXHgw%3D%3D&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpcm2cms%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRgIhAOkBUUXVKYtJ3JrNtOlvy8RcWQHOAb6AqH3zhl2VJfaEAiEA-iAd4QQ3eoTkDLWa5tg0rFcjv2_AX7RbOXB0DnOJ7Zs%3D',
# 'mimeType': 'video/webm; codecs="vp9"', 'bitrate': 5370257, 'width': 1896, 'height': 1440, 'initRange': {'start': '0', 'end': '219'}, 'indexRange': {'start': '220', 'end': '708'}, 'lastModified': '1669980995481638', 'contentLength': '78945369', 'quality': 'hd1440', 'fps': 25, 'qualityLabel': '1440p', 'projectionType': 'RECTANGULAR', 'averageBitrate': 4509875, 'colorInfo': {'primaries': 'COLOR_PRIMARIES_BT709', 'transferCharacteristics': 'COLOR_TRANSFER_CHARACTERISTICS_BT709', 'matrixCoefficients': 'COLOR_MATRIX_COEFFICIENTS_BT709'}, 'approxDurationMs': '140040'},
# {'itag': 137, 'url': 'https://rr1---sn-gvnuxaxjvh-v8cz.googlevideo.com/videoplayback?expire=1671533241&ei=WT6hY_vdFo2zyQWYwqqADw&ip=92.125.255.100&id=o-AOz34mLnQWBtTjMz0e_ST17vpg8qv5zl4LwqsEC4Igum&itag=137&source=youtube&requiressl=yes&mh=Q8&mm=31%2C29&mn=sn-gvnuxaxjvh-v8cz%2Csn-n8v7znsl&ms=au%2Crdu&mv=m&mvi=1&pcm2cms=yes&pl=18&initcwndbps=1813750&vprv=1&mime=video%2Fmp4&gir=yes&clen=48347503&dur=140.040&lmt=1669980887507801&mt=1671511290&fvip=3&keepalive=yes&fexp=24001373%2C24007246&c=ANDROID&txp=5319224&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cgir%2Cclen%2Cdur%2Clmt&sig=AOq0QJ8wRAIgSIKmjXb6zhaEaiVRSKkYtMq09S5pHzRUrmRKBctWkcsCIFJsOiNww6OVRos08btC9KjG3BhX1AQ9N3VCYlEghBy5&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpcm2cms%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRgIhAOkBUUXVKYtJ3JrNtOlvy8RcWQHOAb6AqH3zhl2VJfaEAiEA-iAd4QQ3eoTkDLWa5tg0rFcjv2_AX7RbOXB0DnOJ7Zs%3D',
# 'mimeType': 'video/mp4; codecs="avc1.640028"', 'bitrate': 3454868, 'width': 1422, 'height': 1080, 'initRange': {'start': '0', 'end': '742'}, 'indexRange': {'start': '743', 'end': '1110'}, 'lastModified': '1669980887507801', 'contentLength': '48347503', 'quality': 'hd1080', 'fps': 25, 'qualityLabel': '1080p', 'projectionType': 'RECTANGULAR', 'averageBitrate': 2761925, 'approxDurationMs': '140040'},
# {'itag': 248, 'url': 'https://rr1---sn-gvnuxaxjvh-v8cz.googlevideo.com/videoplayback?expire=1671533241&ei=WT6hY_vdFo2zyQWYwqqADw&ip=92.125.255.100&id=o-AOz34mLnQWBtTjMz0e_ST17vpg8qv5zl4LwqsEC4Igum&itag=248&source=youtube&requiressl=yes&mh=Q8&mm=31%2C29&mn=sn-gvnuxaxjvh-v8cz%2Csn-n8v7znsl&ms=au%2Crdu&mv=m&mvi=1&pcm2cms=yes&pl=18&initcwndbps=1813750&vprv=1&mime=video%2Fwebm&gir=yes&clen=24299373&dur=140.040&lmt=1669980961247217&mt=1671511290&fvip=3&keepalive=yes&fexp=24001373%2C24007246&c=ANDROID&txp=5319224&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cgir%2Cclen%2Cdur%2Clmt&sig=AOq0QJ8wRQIgDx5MJOwPL5TtiRnfJdagB0VRqxSkIzSakeasgGMSDWYCIQCTj3OSlC3T0Zq_5gm_4l2f5f3wPg0sgjKzFrVdM1CSIA%3D%3D&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpcm2cms%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRgIhAOkBUUXVKYtJ3JrNtOlvy8RcWQHOAb6AqH3zhl2VJfaEAiEA-iAd4QQ3eoTkDLWa5tg0rFcjv2_AX7RbOXB0DnOJ7Zs%3D', 'mimeType': 'video/webm; codecs="vp9"', 'bitrate': 2149234, 'width': 1422, 'height': 1080, 'initRange': {'start': '0', 'end': '219'}, 'indexRange': {'start': '220', 'end': '695'}, 'lastModified': '1669980961247217', 'contentLength': '24299373', 'quality': 'hd1080', 'fps': 25, 'qualityLabel': '1080p', 'projectionType': 'RECTANGULAR', 'averageBitrate': 1388138, 'colorInfo': {'primaries': 'COLOR_PRIMARIES_BT709', 'transferCharacteristics': 'COLOR_TRANSFER_CHARACTERISTICS_BT709', 'matrixCoefficients': 'COLOR_MATRIX_COEFFICIENTS_BT709'}, 'approxDurationMs': '140040'},
# {'itag': 136, 'url': 'https://rr1---sn-gvnuxaxjvh-v8cz.googlevideo.com/videoplayback?expire=1671533241&ei=WT6hY_vdFo2zyQWYwqqADw&ip=92.125.255.100&id=o-AOz34mLnQWBtTjMz0e_ST17vpg8qv5zl4LwqsEC4Igum&itag=136&source=youtube&requiressl=yes&mh=Q8&mm=31%2C29&mn=sn-gvnuxaxjvh-v8cz%2Csn-n8v7znsl&ms=au%2Crdu&mv=m&mvi=1&pcm2cms=yes&pl=18&initcwndbps=1813750&vprv=1&mime=video%2Fmp4&gir=yes&clen=22729080&dur=140.040&lmt=1669980899712714&mt=1671511290&fvip=3&keepalive=yes&fexp=24001373%2C24007246&c=ANDROID&txp=5319224&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cgir%2Cclen%2Cdur%2Clmt&sig=AOq0QJ8wRQIhAJ1YCrUG4lxXMQARAfo8yE4Tq8omNJwMK0c7aQ8x5va_AiBUMImdVXyZ768qx9r2APeek7UIrLuXFqS3uwWDk-cklw%3D%3D&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpcm2cms%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRgIhAOkBUUXVKYtJ3JrNtOlvy8RcWQHOAb6AqH3zhl2VJfaEAiEA-iAd4QQ3eoTkDLWa5tg0rFcjv2_AX7RbOXB0DnOJ7Zs%3D',
# 'mimeType': 'video/mp4; codecs="avc1.64001f"', 'bitrate': 1763842, 'width': 948, 'height': 720, 'initRange': {'start': '0', 'end': '741'}, 'indexRange': {'start': '742', 'end': '1109'}, 'lastModified': '1669980899712714', 'contentLength': '22729080', 'quality': 'hd720', 'fps': 25, 'qualityLabel': '720p', 'projectionType': 'RECTANGULAR', 'averageBitrate': 1298433, 'approxDurationMs': '140040'},
# {'itag': 247, 'url': 'https://rr1---sn-gvnuxaxjvh-v8cz.googlevideo.com/videoplayback?expire=1671533241&ei=WT6hY_vdFo2zyQWYwqqADw&ip=92.125.255.100&id=o-AOz34mLnQWBtTjMz0e_ST17vpg8qv5zl4LwqsEC4Igum&itag=247&source=youtube&requiressl=yes&mh=Q8&mm=31%2C29&mn=sn-gvnuxaxjvh-v8cz%2Csn-n8v7znsl&ms=au%2Crdu&mv=m&mvi=1&pcm2cms=yes&pl=18&initcwndbps=1813750&vprv=1&mime=video%2Fwebm&gir=yes&clen=14237423&dur=140.040&lmt=1669980986714399&mt=1671511290&fvip=3&keepalive=yes&fexp=24001373%2C24007246&c=ANDROID&txp=5319224&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cgir%2Cclen%2Cdur%2Clmt&sig=AOq0QJ8wRQIhAM9qwH1Z8caZpyP0Zic-cBbmQ_TgxDeLFMAC5-TyFIhYAiByegDmFjNauBl5KYH3Mink005JPDPL4Av6qaCp-DcDoA%3D%3D&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpcm2cms%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRgIhAOkBUUXVKYtJ3JrNtOlvy8RcWQHOAb6AqH3zhl2VJfaEAiEA-iAd4QQ3eoTkDLWa5tg0rFcjv2_AX7RbOXB0DnOJ7Zs%3D', 'mimeType': 'video/webm; codecs="vp9"', 'bitrate': 1276823, 'width': 948, 'height': 720, 'initRange': {'start': '0', 'end': '219'}, 'indexRange': {'start': '220', 'end': '686'}, 'lastModified': '1669980986714399', 'contentLength': '14237423', 'quality': 'hd720', 'fps': 25, 'qualityLabel': '720p', 'projectionType': 'RECTANGULAR', 'averageBitrate': 813334, 'colorInfo': {'primaries': 'COLOR_PRIMARIES_BT709', 'transferCharacteristics': 'COLOR_TRANSFER_CHARACTERISTICS_BT709', 'matrixCoefficients': 'COLOR_MATRIX_COEFFICIENTS_BT709'}, 'approxDurationMs': '140040'},
# {'itag': 135, 'url': 'https://rr1---sn-gvnuxaxjvh-v8cz.googlevideo.com/videoplayback?expire=1671533241&ei=WT6hY_vdFo2zyQWYwqqADw&ip=92.125.255.100&id=o-AOz34mLnQWBtTjMz0e_ST17vpg8qv5zl4LwqsEC4Igum&itag=135&source=youtube&requiressl=yes&mh=Q8&mm=31%2C29&mn=sn-gvnuxaxjvh-v8cz%2Csn-n8v7znsl&ms=au%2Crdu&mv=m&mvi=1&pcm2cms=yes&pl=18&initcwndbps=1813750&vprv=1&mime=video%2Fmp4&gir=yes&clen=12039460&dur=140.040&lmt=1669980897820169&mt=1671511290&fvip=3&keepalive=yes&fexp=24001373%2C24007246&c=ANDROID&txp=5319224&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cgir%2Cclen%2Cdur%2Clmt&sig=AOq0QJ8wRAIgBWXFlkT_Fr_SziVUgw9iq1M2Eglk2AT_XipO3-f5YJgCIHX6WK47uLq9UETLlFZ_RlpYlsS0cFvQWoVsWyq0mcFf&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpcm2cms%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRgIhAOkBUUXVKYtJ3JrNtOlvy8RcWQHOAb6AqH3zhl2VJfaEAiEA-iAd4QQ3eoTkDLWa5tg0rFcjv2_AX7RbOXB0DnOJ7Zs%3D', 'mimeType': 'video/mp4; codecs="avc1.4d401e"', 'bitrate': 909368, 'width': 632, 'height': 480, 'initRange': {'start': '0', 'end': '740'}, 'indexRange': {'start': '741', 'end': '1108'}, 'lastModified': '1669980897820169', 'contentLength': '12039460', 'quality': 'large', 'fps': 25, 'qualityLabel': '480p', 'projectionType': 'RECTANGULAR', 'averageBitrate': 687772, 'approxDurationMs': '140040'},
# {'itag': 244, 'url': 'https://rr1---sn-gvnuxaxjvh-v8cz.googlevideo.com/videoplayback?expire=1671533241&ei=WT6hY_vdFo2zyQWYwqqADw&ip=92.125.255.100&id=o-AOz34mLnQWBtTjMz0e_ST17vpg8qv5zl4LwqsEC4Igum&itag=244&source=youtube&requiressl=yes&mh=Q8&mm=31%2C29&mn=sn-gvnuxaxjvh-v8cz%2Csn-n8v7znsl&ms=au%2Crdu&mv=m&mvi=1&pcm2cms=yes&pl=18&initcwndbps=1813750&vprv=1&mime=video%2Fwebm&gir=yes&clen=7621399&dur=140.040&lmt=1669980940843228&mt=1671511290&fvip=3&keepalive=yes&fexp=24001373%2C24007246&c=ANDROID&txp=5319224&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cgir%2Cclen%2Cdur%2Clmt&sig=AOq0QJ8wRAIgV75mbwv3ghcmpH5XsYAGbg8Q_P46AaqFpUCSQJuQ3YkCIDkUtssKPS_d614u7a1vti7wQuSVAHX98Llw8b0qZI0H&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpcm2cms%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRgIhAOkBUUXVKYtJ3JrNtOlvy8RcWQHOAb6AqH3zhl2VJfaEAiEA-iAd4QQ3eoTkDLWa5tg0rFcjv2_AX7RbOXB0DnOJ7Zs%3D', 'mimeType': 'video/webm; codecs="vp9"', 'bitrate': 629993, 'width': 632, 'height': 480, 'initRange': {'start': '0', 'end': '219'}, 'indexRange': {'start': '220', 'end': '686'}, 'lastModified': '1669980940843228', 'contentLength': '7621399', 'quality': 'large', 'fps': 25, 'qualityLabel': '480p', 'projectionType': 'RECTANGULAR', 'averageBitrate': 435384, 'colorInfo': {'primaries': 'COLOR_PRIMARIES_BT709', 'transferCharacteristics': 'COLOR_TRANSFER_CHARACTERISTICS_BT709', 'matrixCoefficients': 'COLOR_MATRIX_COEFFICIENTS_BT709'}, 'approxDurationMs': '140040'},
# {'itag': 134, 'url': 'https://rr1---sn-gvnuxaxjvh-v8cz.googlevideo.com/videoplayback?expire=1671533241&ei=WT6hY_vdFo2zyQWYwqqADw&ip=92.125.255.100&id=o-AOz34mLnQWBtTjMz0e_ST17vpg8qv5zl4LwqsEC4Igum&itag=134&source=youtube&requiressl=yes&mh=Q8&mm=31%2C29&mn=sn-gvnuxaxjvh-v8cz%2Csn-n8v7znsl&ms=au%2Crdu&mv=m&mvi=1&pcm2cms=yes&pl=18&initcwndbps=1813750&vprv=1&mime=video%2Fmp4&gir=yes&clen=5229968&dur=140.040&lmt=1669980892496068&mt=1671511290&fvip=3&keepalive=yes&fexp=24001373%2C24007246&c=ANDROID&txp=5319224&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cgir%2Cclen%2Cdur%2Clmt&sig=AOq0QJ8wRQIhAPYBkp6-9lvz_RlkoMN8wdrArh0VaPZGvbM8USmrZr3-AiBBW7oprfesC1v4OcQGa4-F2Z-yqmWdX5VtOEMlgZ-hXw%3D%3D&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpcm2cms%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRgIhAOkBUUXVKYtJ3JrNtOlvy8RcWQHOAb6AqH3zhl2VJfaEAiEA-iAd4QQ3eoTkDLWa5tg0rFcjv2_AX7RbOXB0DnOJ7Zs%3D', 'mimeType': 'video/mp4; codecs="avc1.4d4015"', 'bitrate': 450226, 'width': 474, 'height': 360, 'initRange': {'start': '0', 'end': '740'}, 'indexRange': {'start': '741', 'end': '1108'}, 'lastModified': '1669980892496068', 'contentLength': '5229968', 'quality': 'medium', 'fps': 25, 'qualityLabel': '360p', 'projectionType': 'RECTANGULAR', 'averageBitrate': 298769, 'highReplication': True, 'approxDurationMs': '140040'},
# {'itag': 243, 'url': 'https://rr1---sn-gvnuxaxjvh-v8cz.googlevideo.com/videoplayback?expire=1671533241&ei=WT6hY_vdFo2zyQWYwqqADw&ip=92.125.255.100&id=o-AOz34mLnQWBtTjMz0e_ST17vpg8qv5zl4LwqsEC4Igum&itag=243&source=youtube&requiressl=yes&mh=Q8&mm=31%2C29&mn=sn-gvnuxaxjvh-v8cz%2Csn-n8v7znsl&ms=au%2Crdu&mv=m&mvi=1&pcm2cms=yes&pl=18&initcwndbps=1813750&vprv=1&mime=video%2Fwebm&gir=yes&clen=4316382&dur=140.040&lmt=1669981014243103&mt=1671511290&fvip=3&keepalive=yes&fexp=24001373%2C24007246&c=ANDROID&txp=5319224&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cgir%2Cclen%2Cdur%2Clmt&sig=AOq0QJ8wRgIhAJlcrarpa3iGIcYf8mgiX4vAanYUutShMC0za_HiMls1AiEA4OdRgtj4Z4c8M7DhoTKCiE-b4B2d4p4sjY_KhV1QWJ4%3D&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpcm2cms%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRgIhAOkBUUXVKYtJ3JrNtOlvy8RcWQHOAb6AqH3zhl2VJfaEAiEA-iAd4QQ3eoTkDLWa5tg0rFcjv2_AX7RbOXB0DnOJ7Zs%3D', 'mimeType': 'video/webm; codecs="vp9"', 'bitrate': 327143, 'width': 474, 'height': 360, 'initRange': {'start': '0', 'end': '219'}, 'indexRange': {'start': '220', 'end': '686'}, 'lastModified': '1669981014243103', 'contentLength': '4316382', 'quality': 'medium', 'fps': 25, 'qualityLabel': '360p', 'projectionType': 'RECTANGULAR', 'averageBitrate': 246579, 'colorInfo': {'primaries': 'COLOR_PRIMARIES_BT709', 'transferCharacteristics': 'COLOR_TRANSFER_CHARACTERISTICS_BT709', 'matrixCoefficients': 'COLOR_MATRIX_COEFFICIENTS_BT709'}, 'approxDurationMs': '140040'},
# {'itag': 133, 'url': 'https://rr1---sn-gvnuxaxjvh-v8cz.googlevideo.com/videoplayback?expire=1671533241&ei=WT6hY_vdFo2zyQWYwqqADw&ip=92.125.255.100&id=o-AOz34mLnQWBtTjMz0e_ST17vpg8qv5zl4LwqsEC4Igum&itag=133&source=youtube&requiressl=yes&mh=Q8&mm=31%2C29&mn=sn-gvnuxaxjvh-v8cz%2Csn-n8v7znsl&ms=au%2Crdu&mv=m&mvi=1&pcm2cms=yes&pl=18&initcwndbps=1813750&vprv=1&mime=video%2Fmp4&gir=yes&clen=2617774&dur=140.040&lmt=1669980875428107&mt=1671511290&fvip=3&keepalive=yes&fexp=24001373%2C24007246&c=ANDROID&txp=5319224&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cgir%2Cclen%2Cdur%2Clmt&sig=AOq0QJ8wRQIgSNvzVDVuBpMOAxiFEaHwFdFLVXVbgNysbbWaW7fVh3oCIQDzDo9dVsMaZVlVxJMM96sBFlabL7I7TA9PqDbypi5gYQ%3D%3D&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpcm2cms%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRgIhAOkBUUXVKYtJ3JrNtOlvy8RcWQHOAb6AqH3zhl2VJfaEAiEA-iAd4QQ3eoTkDLWa5tg0rFcjv2_AX7RbOXB0DnOJ7Zs%3D', 'mimeType': 'video/mp4; codecs="avc1.4d400d"', 'bitrate': 208964, 'width': 316, 'height': 240, 'initRange': {'start': '0', 'end': '739'}, 'indexRange': {'start': '740', 'end': '1107'}, 'lastModified': '1669980875428107', 'contentLength': '2617774', 'quality': 'small', 'fps': 25, 'qualityLabel': '240p', 'projectionType': 'RECTANGULAR', 'averageBitrate': 149544, 'approxDurationMs': '140040'},
# {'itag': 242, 'url': 'https://rr1---sn-gvnuxaxjvh-v8cz.googlevideo.com/videoplayback?expire=1671533241&ei=WT6hY_vdFo2zyQWYwqqADw&ip=92.125.255.100&id=o-AOz34mLnQWBtTjMz0e_ST17vpg8qv5zl4LwqsEC4Igum&itag=242&source=youtube&requiressl=yes&mh=Q8&mm=31%2C29&mn=sn-gvnuxaxjvh-v8cz%2Csn-n8v7znsl&ms=au%2Crdu&mv=m&mvi=1&pcm2cms=yes&pl=18&initcwndbps=1813750&vprv=1&mime=video%2Fwebm&gir=yes&clen=2434775&dur=140.040&lmt=1669980951842710&mt=1671511290&fvip=3&keepalive=yes&fexp=24001373%2C24007246&c=ANDROID&txp=5319224&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cgir%2Cclen%2Cdur%2Clmt&sig=AOq0QJ8wRgIhAOPK6lBAIBwVJf_vfsK9zBcdl4eKnMshhrt8A4ADk0GHAiEAxjpnkwReWHlt-fAJvUt-Jp1qIumNcb5PO0MXzIsxHN8%3D&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpcm2cms%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRgIhAOkBUUXVKYtJ3JrNtOlvy8RcWQHOAb6AqH3zhl2VJfaEAiEA-iAd4QQ3eoTkDLWa5tg0rFcjv2_AX7RbOXB0DnOJ7Zs%3D', 'mimeType': 'video/webm; codecs="vp9"', 'bitrate': 179425, 'width': 316, 'height': 240, 'initRange': {'start': '0', 'end': '218'}, 'indexRange': {'start': '219', 'end': '685'}, 'lastModified': '1669980951842710', 'contentLength': '2434775', 'quality': 'small', 'fps': 25, 'qualityLabel': '240p', 'projectionType': 'RECTANGULAR', 'averageBitrate': 139090, 'colorInfo': {'primaries': 'COLOR_PRIMARIES_BT709', 'transferCharacteristics': 'COLOR_TRANSFER_CHARACTERISTICS_BT709', 'matrixCoefficients': 'COLOR_MATRIX_COEFFICIENTS_BT709'}, 'approxDurationMs': '140040'},
# {'itag': 160, 'url': 'https://rr1---sn-gvnuxaxjvh-v8cz.googlevideo.com/videoplayback?expire=1671533241&ei=WT6hY_vdFo2zyQWYwqqADw&ip=92.125.255.100&id=o-AOz34mLnQWBtTjMz0e_ST17vpg8qv5zl4LwqsEC4Igum&itag=160&source=youtube&requiressl=yes&mh=Q8&mm=31%2C29&mn=sn-gvnuxaxjvh-v8cz%2Csn-n8v7znsl&ms=au%2Crdu&mv=m&mvi=1&pcm2cms=yes&pl=18&initcwndbps=1813750&vprv=1&mime=video%2Fmp4&gir=yes&clen=1171472&dur=140.040&lmt=1669980895005756&mt=1671511290&fvip=3&keepalive=yes&fexp=24001373%2C24007246&c=ANDROID&txp=5319224&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cgir%2Cclen%2Cdur%2Clmt&sig=AOq0QJ8wRQIgKcZfPJAxLlriuPLhBMNfP4qM8whd-rUTvgl5FJ4sBH0CIQDyC-neoDJKPkESZZ3RjgcXg58S88oUhybL5qLN_4Grlg%3D%3D&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpcm2cms%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRgIhAOkBUUXVKYtJ3JrNtOlvy8RcWQHOAb6AqH3zhl2VJfaEAiEA-iAd4QQ3eoTkDLWa5tg0rFcjv2_AX7RbOXB0DnOJ7Zs%3D', 'mimeType': 'video/mp4; codecs="avc1.4d400b"', 'bitrate': 101467, 'width': 190, 'height': 144, 'initRange': {'start': '0', 'end': '739'}, 'indexRange': {'start': '740', 'end': '1107'}, 'lastModified': '1669980895005756', 'contentLength': '1171472', 'quality': 'tiny', 'fps': 25, 'qualityLabel': '144p', 'projectionType': 'RECTANGULAR', 'averageBitrate': 66922, 'approxDurationMs': '140040'},
# {'itag': 278, 'url': 'https://rr1---sn-gvnuxaxjvh-v8cz.googlevideo.com/videoplayback?expire=1671533241&ei=WT6hY_vdFo2zyQWYwqqADw&ip=92.125.255.100&id=o-AOz34mLnQWBtTjMz0e_ST17vpg8qv5zl4LwqsEC4Igum&itag=278&source=youtube&requiressl=yes&mh=Q8&mm=31%2C29&mn=sn-gvnuxaxjvh-v8cz%2Csn-n8v7znsl&ms=au%2Crdu&mv=m&mvi=1&pcm2cms=yes&pl=18&initcwndbps=1813750&vprv=1&mime=video%2Fwebm&gir=yes&clen=1194439&dur=140.040&lmt=1669980964193031&mt=1671511290&fvip=3&keepalive=yes&fexp=24001373%2C24007246&c=ANDROID&txp=5319224&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cgir%2Cclen%2Cdur%2Clmt&sig=AOq0QJ8wRQIhAPtqLhHyBEdnuH6HVw7NMttqmfRrQTq_l7vN0TtYoY_7AiA7LJbXQ_bjWvWSaHPzLOYzqipe5nO95aVe0gPMmwGD3Q%3D%3D&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpcm2cms%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRgIhAOkBUUXVKYtJ3JrNtOlvy8RcWQHOAb6AqH3zhl2VJfaEAiEA-iAd4QQ3eoTkDLWa5tg0rFcjv2_AX7RbOXB0DnOJ7Zs%3D', 'mimeType': 'video/webm; codecs="vp9"', 'bitrate': 81942, 'width': 190, 'height': 144, 'initRange': {'start': '0', 'end': '216'}, 'indexRange': {'start': '217', 'end': '682'}, 'lastModified': '1669980964193031', 'contentLength': '1194439', 'quality': 'tiny', 'fps': 25, 'qualityLabel': '144p', 'projectionType': 'RECTANGULAR', 'averageBitrate': 68234, 'colorInfo': {'primaries': 'COLOR_PRIMARIES_BT709', 'transferCharacteristics': 'COLOR_TRANSFER_CHARACTERISTICS_BT709', 'matrixCoefficients': 'COLOR_MATRIX_COEFFICIENTS_BT709'}, 'approxDurationMs': '140040'},
# {'itag': 139, 'url': 'https://rr1---sn-gvnuxaxjvh-v8cz.googlevideo.com/videoplayback?expire=1671533241&ei=WT6hY_vdFo2zyQWYwqqADw&ip=92.125.255.100&id=o-AOz34mLnQWBtTjMz0e_ST17vpg8qv5zl4LwqsEC4Igum&itag=139&source=youtube&requiressl=yes&mh=Q8&mm=31%2C29&mn=sn-gvnuxaxjvh-v8cz%2Csn-n8v7znsl&ms=au%2Crdu&mv=m&mvi=1&pcm2cms=yes&pl=18&initcwndbps=1813750&vprv=1&mime=audio%2Fmp4&gir=yes&clen=855624&dur=140.155&lmt=1669980892813759&mt=1671511290&fvip=3&keepalive=yes&fexp=24001373%2C24007246&c=ANDROID&txp=5318224&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cgir%2Cclen%2Cdur%2Clmt&sig=AOq0QJ8wRQIgWgAOaos0jXde05R43C4yz80ErvycdVjvG5MP2gzMmQYCIQCDhMtCvqJmodtwgjntUEeyVuXZ4TOfPLzAsyEk5Tw6xA%3D%3D&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpcm2cms%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRgIhAOkBUUXVKYtJ3JrNtOlvy8RcWQHOAb6AqH3zhl2VJfaEAiEA-iAd4QQ3eoTkDLWa5tg0rFcjv2_AX7RbOXB0DnOJ7Zs%3D', 'mimeType': 'audio/mp4; codecs="mp4a.40.5"', 'bitrate': 49894, 'initRange': {'start': '0', 'end': '640'}, 'indexRange': {'start': '641', 'end': '852'}, 'lastModified': '1669980892813759', 'contentLength': '855624', 'quality': 'tiny', 'projectionType': 'RECTANGULAR', 'averageBitrate': 48838, 'audioQuality': 'AUDIO_QUALITY_LOW', 'approxDurationMs': '140155', 'audioSampleRate': '22050', 'audioChannels': 2},
# {'itag': 140, 'url': 'https://rr1---sn-gvnuxaxjvh-v8cz.googlevideo.com/videoplayback?expire=1671533241&ei=WT6hY_vdFo2zyQWYwqqADw&ip=92.125.255.100&id=o-AOz34mLnQWBtTjMz0e_ST17vpg8qv5zl4LwqsEC4Igum&itag=140&source=youtube&requiressl=yes&mh=Q8&mm=31%2C29&mn=sn-gvnuxaxjvh-v8cz%2Csn-n8v7znsl&ms=au%2Crdu&mv=m&mvi=1&pcm2cms=yes&pl=18&initcwndbps=1813750&vprv=1&mime=audio%2Fmp4&gir=yes&clen=2268287&dur=140.109&lmt=1669980892939232&mt=1671511290&fvip=3&keepalive=yes&fexp=24001373%2C24007246&c=ANDROID&txp=5318224&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cgir%2Cclen%2Cdur%2Clmt&sig=AOq0QJ8wRgIhAJKVtnVQTvJNnGFZLh1pZSkpyMzBtevR16ZHysppU8FjAiEA_c53dTsAm3T3Gc_fzhpqmkwCl_kwezP_w6UB3e1Da4w%3D&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpcm2cms%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRgIhAOkBUUXVKYtJ3JrNtOlvy8RcWQHOAb6AqH3zhl2VJfaEAiEA-iAd4QQ3eoTkDLWa5tg0rFcjv2_AX7RbOXB0DnOJ7Zs%3D', 'mimeType': 'audio/mp4; codecs="mp4a.40.2"', 'bitrate': 130152, 'initRange': {'start': '0', 'end': '631'}, 'indexRange': {'start': '632', 'end': '843'}, 'lastModified': '1669980892939232', 'contentLength': '2268287', 'quality': 'tiny', 'projectionType': 'RECTANGULAR', 'averageBitrate': 129515, 'highReplication': True, 'audioQuality': 'AUDIO_QUALITY_MEDIUM', 'approxDurationMs': '140109', 'audioSampleRate': '44100', 'audioChannels': 2},
# {'itag': 249, 'url': 'https://rr1---sn-gvnuxaxjvh-v8cz.googlevideo.com/videoplayback?expire=1671533241&ei=WT6hY_vdFo2zyQWYwqqADw&ip=92.125.255.100&id=o-AOz34mLnQWBtTjMz0e_ST17vpg8qv5zl4LwqsEC4Igum&itag=249&source=youtube&requiressl=yes&mh=Q8&mm=31%2C29&mn=sn-gvnuxaxjvh-v8cz%2Csn-n8v7znsl&ms=au%2Crdu&mv=m&mvi=1&pcm2cms=yes&pl=18&initcwndbps=1813750&vprv=1&mime=audio%2Fwebm&gir=yes&clen=931701&dur=140.061&lmt=1669980918584053&mt=1671511290&fvip=3&keepalive=yes&fexp=24001373%2C24007246&c=ANDROID&txp=5318224&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cgir%2Cclen%2Cdur%2Clmt&sig=AOq0QJ8wRgIhALM6k0oDHXzCX1uh5Fg1jfBv_IoXoWa3dn8-zckKgJwgAiEAhDprFqRzmbkfyCpcol2lABU6qbFXrb6o8kQGOZWsvAY%3D&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpcm2cms%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRgIhAOkBUUXVKYtJ3JrNtOlvy8RcWQHOAb6AqH3zhl2VJfaEAiEA-iAd4QQ3eoTkDLWa5tg0rFcjv2_AX7RbOXB0DnOJ7Zs%3D', 'mimeType': 'audio/webm; codecs="opus"', 'bitrate': 74400, 'initRange': {'start': '0', 'end': '258'}, 'indexRange': {'start': '259', 'end': '509'}, 'lastModified': '1669980918584053', 'contentLength': '931701', 'quality': 'tiny', 'projectionType': 'RECTANGULAR', 'averageBitrate': 53216, 'audioQuality': 'AUDIO_QUALITY_LOW', 'approxDurationMs': '140061', 'audioSampleRate': '48000', 'audioChannels': 2},
# {'itag': 250, 'url': 'https://rr1---sn-gvnuxaxjvh-v8cz.googlevideo.com/videoplayback?expire=1671533241&ei=WT6hY_vdFo2zyQWYwqqADw&ip=92.125.255.100&id=o-AOz34mLnQWBtTjMz0e_ST17vpg8qv5zl4LwqsEC4Igum&itag=250&source=youtube&requiressl=yes&mh=Q8&mm=31%2C29&mn=sn-gvnuxaxjvh-v8cz%2Csn-n8v7znsl&ms=au%2Crdu&mv=m&mvi=1&pcm2cms=yes&pl=18&initcwndbps=1813750&vprv=1&mime=audio%2Fwebm&gir=yes&clen=1121956&dur=140.061&lmt=1669980909207033&mt=1671511290&fvip=3&keepalive=yes&fexp=24001373%2C24007246&c=ANDROID&txp=5318224&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cgir%2Cclen%2Cdur%2Clmt&sig=AOq0QJ8wRgIhALtQ0A889H_Fzaw6oQBLqZ8bWWKRyCdL68CqzgjUpl3OAiEA7xSSIM2POhdRssq3awFNeu5kyjGhAaHFWndY3fWiFWc%3D&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpcm2cms%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRgIhAOkBUUXVKYtJ3JrNtOlvy8RcWQHOAb6AqH3zhl2VJfaEAiEA-iAd4QQ3eoTkDLWa5tg0rFcjv2_AX7RbOXB0DnOJ7Zs%3D', 'mimeType': 'audio/webm; codecs="opus"', 'bitrate': 88533, 'initRange': {'start': '0', 'end': '258'}, 'indexRange': {'start': '259', 'end': '510'}, 'lastModified': '1669980909207033', 'contentLength': '1121956', 'quality': 'tiny', 'projectionType': 'RECTANGULAR', 'averageBitrate': 64083, 'audioQuality': 'AUDIO_QUALITY_LOW', 'approxDurationMs': '140061', 'audioSampleRate': '48000', 'audioChannels': 2},
# {'itag': 251, 'url': 'https://rr1---sn-gvnuxaxjvh-v8cz.googlevideo.com/videoplayback?expire=1671533241&ei=WT6hY_vdFo2zyQWYwqqADw&ip=92.125.255.100&id=o-AOz34mLnQWBtTjMz0e_ST17vpg8qv5zl4LwqsEC4Igum&itag=251&source=youtube&requiressl=yes&mh=Q8&mm=31%2C29&mn=sn-gvnuxaxjvh-v8cz%2Csn-n8v7znsl&ms=au%2Crdu&mv=m&mvi=1&pcm2cms=yes&pl=18&initcwndbps=1813750&vprv=1&mime=audio%2Fwebm&gir=yes&clen=1912781&dur=140.061&lmt=1669980908746795&mt=1671511290&fvip=3&keepalive=yes&fexp=24001373%2C24007246&c=ANDROID&txp=5318224&sparams=expire%2Cei%2Cip%2Cid%2Citag%2Csource%2Crequiressl%2Cvprv%2Cmime%2Cgir%2Cclen%2Cdur%2Clmt&sig=AOq0QJ8wRQIhAOIkUzRsx6cJAo2B-SdXTcTSOxad7KKQyZshj5Y63ff_AiAI1SfjvfsQnSaHLTewmRCSMnJwXPoLEDJb3Fqcdq8aIg%3D%3D&lsparams=mh%2Cmm%2Cmn%2Cms%2Cmv%2Cmvi%2Cpcm2cms%2Cpl%2Cinitcwndbps&lsig=AG3C_xAwRgIhAOkBUUXVKYtJ3JrNtOlvy8RcWQHOAb6AqH3zhl2VJfaEAiEA-iAd4QQ3eoTkDLWa5tg0rFcjv2_AX7RbOXB0DnOJ7Zs%3D', 'mimeType': 'audio/webm; codecs="opus"', 'bitrate': 160400, 'initRange': {'start': '0', 'end': '258'}, 'indexRange': {'start': '259', 'end': '510'}, 'lastModified': '1669980908746795', 'contentLength': '1912781', 'quality': 'tiny', 'projectionType': 'RECTANGULAR', 'averageBitrate': 109254, 'audioQuality': 'AUDIO_QUALITY_MEDIUM', 'approxDurationMs': '140061', 'audioSampleRate': '48000', 'audioChannels': 2}
# ]
# }

# yt-dlp --format 'mp4' --list-formats  --skip-download https://youtu.be/ibbjk7-yvPI
# --write-info-json

