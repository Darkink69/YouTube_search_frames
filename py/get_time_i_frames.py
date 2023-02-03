from pytube import YouTube
import subprocess

# link = 'https://youtu.be/grMPi9PTCaA'
fps = 25


def get_frame_types(url):
    command = 'ffprobe -v error -show_entries frame=pict_type -of default=noprint_wrappers=1'.split()
    out = subprocess.check_output(command + [url]).decode()
    frame_types = out.replace('pict_type=', '').split()
    return zip(range(len(frame_types)), frame_types)


def get_i_keyframes(link):
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


i_frame = get_i_keyframes(link)
i_frame_seconds = make_time_i_frame(i_frame, fps)
# print(i_frame_seconds)

