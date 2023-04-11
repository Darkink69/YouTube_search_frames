import subprocess


def get_frame_types(url):
    command = 'ffprobe -v error -show_entries frame=pict_type -of default=noprint_wrappers=1'.split()
    out = subprocess.check_output(command + [url]).decode()
    frame_types = out.replace('pict_type=', '').split()
    return zip(range(len(frame_types)), frame_types)


def get_i_keyframes(url):
    print('Get i_frames position..')
    frame_types = get_frame_types(url)
    i_frames = [x[0] for x in frame_types if x[1] == 'I']
    # print(i_frames)
    return i_frames
