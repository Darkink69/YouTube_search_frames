import ffmpeg
import subprocess
import os


def makeFrames(id, url):

    path_folder = f"views/{id}"
    if not os.path.exists(path_folder):
        os.mkdir(path_folder)
    else:
        print(f'{path_folder} folder already exists.')

        if len(os.listdir(path_folder)) == 0:
            print('Folder is empty. Creating images...')

            process_call_str = f'ffmpeg -i "{url}" -vf select="eq(pict_type\,PICT_TYPE_I)" -vsync 2 -f image2 {path_folder}/keyframe-%05d.jpg'
            output = subprocess.check_output(process_call_str, shell=True)
        else:
            print('Images have already been created')

    frames = os.listdir(path_folder)
    return frames, path_folder


# makeFrames(link, itag)