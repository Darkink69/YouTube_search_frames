# from youtube_search import YoutubeSearch
# from youtubesearchpython import VideosSearch
import yt_dlp
import subprocess

# search_request = 'stark-naked women'
# max_res = 3
#
# ydl_opts = {}
# # ydl_opts = {'format_id': '18'}
#
# with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#     # info = ydl.extract_info(link, download=False)
#     video = ydl.extract_info(f"ytsearch{max_res}:{search_request}", download=False)
#
# # print(video)
# # Разберем на части всё info
# for i in dict.keys(video):
#     # print(i, video[i])
#     print()

# process_call_str = 'yt-dlp "ytsearch3:angelina joly" --get-id --get-title'
process_call_str = 'yt-dlp --dateafter 20221201 "ytsearch3:angelina joly" --get-id --get-title'
output = subprocess.check_output(process_call_str, shell=True)
print(output)



# YDL_OPTIONS = {
#     'format': 'bestaudio*',
#     'yesplaylist': True,
#     'cookies-from-browser chrome': True,
#     # 'age-limit': 18
# }
#
# with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
#     info = ydl.extract_info(url, download=False)

# url = 'https://www.youtube.com/playlist?list=PLS45Qmdl8VLNr2lZ5FheQvJYyvHamqcVL'
# # process_call_str = f'yt-dlp --cookies-from-browser chrome --yes-playlist {url}'
# process_call_str = f'yt-dlp --no-flat-playlist {url}'
# output = subprocess.check_output(process_call_str, shell=True)
# print(str(output).split(' '))
# print(info)
