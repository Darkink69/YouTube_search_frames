import json
import yt_dlp


def get_info_dlp(link):

    ydl_opts = {}
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(link, download=False)
        # print(dict.keys(info))
        # print(info['formats'])
        # print(info)
        return info
        # for i in info['formats']:
        #     if 'format_id' in i:
        #         if i['format_id'] == '18':
        #             print(i['url'])

        #  ydl.sanitize_info makes the info json-serializable
        # print(json.dumps(ydl.sanitize_info(info)))

# get_info_dlp(URL)

