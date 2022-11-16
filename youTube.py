from pytube import YouTube
from pytube import Search
from pytube import Playlist
from pytube import Channel
import ffmpeg
import json
import codecs
from ffpyplayer.player import MediaPlayer
import subprocess
import sys
import os


link = 'https://youtu.be/v8IHMhrTzMM'
# itag = 18  # номер потока, 137 с разрешением 1080p, 22 - 720p, 43 или 18 - 360p
myFps = 1 / 15  # каждые 15 секунд
mySearch = 'альманах вокруг света'


def searchVideo(mySearch):
    allResults = []
    s = Search(mySearch)
    # print(s.completion_suggestions)
    print(f'Найдено - {len(s.results)} видео')
    for i in s.results:
        result = 'https://youtu.be/' + str(i)[41:-1]
        allResults.append(result)
    return allResults


def resultsSearch(allResults):
    for i in allResults:
        print(i)
        descVideo(i)
        print('========================================================================')


def descVideo(result, allResults):
    video_info_all = []

    for i in allResults:
        video_info = {}
        yt = YouTube(i)
        # yt.bypass_age_gate()
        # print(yt.vid_info)
        video_info['link'] = i
        video_info['title'] = yt.title
        video_info['description'] = yt.description
        video_info['keywords'] = yt.keywords
        video_info['thumbnail_url'] = yt.thumbnail_url
        video_info['length'] = yt.length
        video_info['channel_url'] = yt.channel_url
        video_info['author'] = yt.author
        video_info['age_restricted'] = yt.age_restricted
        video_info['fmt_streams'] = yt.fmt_streams
        # video_info['streams'] = str(yt.streams)
        # print(yt.streams.filter(progressive=True)[0])
        print(f'Продолжительность - {yt.length // 60 // 60}:{yt.length // 60 % 60}:{yt.length % 60}')
        video_info_all.append(video_info)

        with codecs.open('1.json', 'w', encoding='utf-8') as f:
            json.dump(video_info_all, f, indent=4, ensure_ascii=False)


def makeFrames(link, itag, myFps):
    try:
        url = YouTube(link).streams.get_by_itag(itag).url
    except:
        print('Неверная ссылка')
        yt = YouTube(link)
        print() if yt.age_restricted == 'true' else print('Фильм с возрастным ограничением, невозможно обработать')

    # url = '1.mp4'
    # print(url)
    yt = YouTube(link)
    duration = yt.length
    myFps = 15
    ss, mm, hh = 0, 0, 0

    (ffmpeg
        .input(url)
        # .trim(start_frame=10, end_frame=200)
        # .filter('fps', fps=myFps)
        # .filter('scale', 1512, -1, flags='lanczos')
        # .filter('select', 'eq(pict_type,I)')
        # .filter('select', 'not(mod(n,100))')
        # .filter('scale', 200, 100)
        # .filter('tile', 8, 6)
        # .output('out/keyframe-%02d.png', vsync=2, format='image2')
        .output('out/keyframe.png', vframes=1, ss=ss)
        .run(overwrite_output=True)
     )
    # scale = 200:120, tile = 8x6 -frames: v 1
    # ss = '00:00:00'
    # t = '00:00:10'
    # url = '1.mp4'
    # os.system(f"ffmpeg -i {url} -vf select='gt(scene\,0.2)',scale=200:120,tile -frames:v 1 preview.png")
    # process_call_str = f'ffmpeg -i {url} -ss {ss} out.png'
    # status = subprocess.check_call(process_call_str, shell=True)
    # print(url)


def make_screenshots(link):
    yt = YouTube(link)
    # itag = list((yt.streams.order_by('resolution').desc().itag_index).keys())[0]  # Самый большой поток по разрешению
    url = YouTube(link).streams.get_by_itag(18).url
    out_name_file = str(YouTube(link).video_id)

    process_call_str = f'ffmpeg -i "{url}" -vf select="gt(scene\,0.2)",scale=200:120,tile=8x6 -frames:v 1 out/{out_name_file}.png'
    status = subprocess.check_call(process_call_str, shell=True)


def downloadVideo(link):
    yt = YouTube(link)
    streams = yt.streams
    video_best = streams.order_by('resolution').desc().first()
    # video_2160 = streams.filter(res='2160p').desc().first()
    # video_1080 = streams.filter(res='1080p').desc().first()
    audio_best = streams.filter(only_audio=True).desc().first()
    video = streams.filter(progressive=True).desc().first()

    # video_1080.download()
    video.download()
    audio_best.download()


def txt_to_list():
    with open('list.txt', 'r', encoding='utf-8') as f:
        text = f.readlines()
        list_url_time = [x.strip().split() for x in text]
        return list_url_time


def download_fragment(link, ss, to, item_video):
    # url = '1.mp4'
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





# descVideo(link)

# makeFrames(link, itag, myFps)

# searchVideo(mySearch)
# resultsSearch(allResults)

# downloadVideo(link)
# download_fragment(link, itag)
# descVideo(link)


list_url_time = txt_to_list()
download_serial(list_url_time)
# make_screenshots(link)

#  ffmpeg -i 1.mp4 -vf select='eq(pict_type\,I)' -vsync 2 -f image2 out/keyframe-%02d.png
#  ffmpeg -i 1.mp4 -ss 00:01:00 -to 00:02:00 -vf select='eq(pict_type\,I)' -vsync 2 -f image2 out/keyframe-%02d.png
# ffprobe -v quiet -print_format json -show_format -show_streams 1.mp4 > 1.json
# ffmpeg -i 1.mp4 -ss 00:00:00 -vframes 1 output.png
# ffmpeg -i 1.mp4 -vf select='gt(scene\,0.2)',scale=200:120,tile=8x6 -frames:v 1 preview.png
# к ссылке добавляем в секундах:   ?t=1430

# process_call_str = 'ffmpeg -ss {1} -to {2} -i "{0}"'/
#                             '-acodec aac -b:a 192k -avoid_negative_ts make_zero "{3}"'
#                             .format(str(url), str(ss), str(t), download_file_path)

# f'ffmpeg -ss {ss} -to {to} -i "{url}" -ss {ss} -to {to} -i "{aurl}" -acodec aac -b:a 192k -avoid_negative_ts make_zero -map 0:v:0 -map 1:a:0 out.mp4'

# f'ffmpeg -ss {ss} -to {to} -i "{url}" -acodec aac -b:a 192k -avoid_negative_ts make_zero out.mp4'

# ffmpeg -i 1.mp4 -ss 00:01:00 -to 00:02:00 -c copy cut.mp4

