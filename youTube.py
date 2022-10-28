from pytube import YouTube
from pytube import Search
import ffmpeg
import json
import codecs
from ffpyplayer.player import MediaPlayer
import subprocess
import sys
import os


link = 'https://youtu.be/rYS8edMRgBg'
itag = 18  # номер потока, 137 с разрешением 1080p, 22 - 720p, 43 или 18 - 360p
myFps = 1 / 15  # каждые 15 секунд
mySearch = 'Squarepusher'
allResults = []


def searchVideo(mySearch):
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


def descVideo(link):
    video_info = {}
    yt = YouTube(link)
    # yt.bypass_age_gate()
    # print(yt.vid_info)
    video_info['link'] = link
    video_info['title'] = yt.title
    video_info['description'] = yt.description
    video_info['keywords'] = yt.keywords
    video_info['thumbnail_url'] = yt.thumbnail_url
    video_info['length'] = yt.length
    video_info['channel_url'] = yt.channel_url
    video_info['author'] = yt.author
    video_info['age_restricted'] = yt.age_restricted
    # video_info['streams'] = str(yt.streams)
    # print(yt.streams.filter(progressive=True)[0])
    print(f'Продолжительность - {yt.length // 60 // 60}:{yt.length // 60 % 60}:{yt.length % 60}')
    # yt.bypass_age_gate()
    # with open('1.json', 'w', encoding='utf-8', ) as outfile:
    #     json.dump(video_info, outfile)
    with codecs.open('1.json', 'w', encoding='utf-8') as fout:
        json.dump(video_info, fout, ensure_ascii=False)


def makeFrames(link, itag, myFps):
    try:
        url = YouTube(link).streams.get_by_itag(itag).url
    except:
        print('Неверная ссылка')
        yt = YouTube(link)
        print() if yt.age_restricted == 'true' else print('Фильм с возрастным ограничением, невозможно обработать')

    # url = '1.mp4'
    # print(url)
    (ffmpeg
        .input(url)
        # .trim(start_frame=10, end_frame=200)
        .filter('fps', fps=myFps)
        # .filter('scale', 1512, -1, flags='lanczos')
        # .filter('select', 'eq(pict_type,I)')
        # .filter('select', 'not(mod(n,100))')
        # .filter('scale', 200, 100)
        # .filter('tile', 8, 6)
        .output('out/keyframe-%02d.png', vsync=2, format='image2')
        # .output('out/key.png',)
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


descVideo(link)

# makeFrames(link, itag, myFps)

# searchVideo(mySearch)
# resultsSearch(allResults)

# downloadVideo(link)



#  ffmpeg -i 1.mp4 -vf select='eq(pict_type\,I)' -vsync 2 -f image2 out/keyframe-%02d.png
#  ffmpeg -i 1.mp4 -ss 00:01:00 -to 00:02:00 -vf select='eq(pict_type\,I)' -vsync 2 -f image2 out/keyframe-%02d.png
# ffprobe -v quiet -print_format json -show_format -show_streams 1.mp4 > 1.json
# ffmpeg -i 1.mp4 -ss 00:00:00 -vframes 1 output.png
# ffmpeg -i 1.mp4 -vf select='gt(scene\,0.2)',scale=200:120,tile=8x6 -frames:v 1 preview.png