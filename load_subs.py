import urllib.request
import json


def get_subs_from_url(raw_subs, lang):
    subs = []

    # print(raw_subs)

    if 'sub_auto' in raw_subs[0]:
        type_subs = 'Субтитры созданы автоматически'
        print('Automatic captions')
        for i in raw_subs[0]['sub_auto']:
            if lang == i[0]['name']:
                url = i[0]['url']

    elif 'sub_prof' in raw_subs[0]:
        type_subs = 'Полные субтитры'
        print('Prof subtitles')
        for i in raw_subs[0]['sub_prof']:
            if lang == i[0]['name']:
                url = i[0]['url']

    else:
        print('No subtitles')
        type_subs = 'Нет субтитров'
        return subs, type_subs



    try:
        with urllib.request.urlopen(url) as url:
            data = json.load(url)
            # print(data)
    except BaseException:
        print('Не удалось загрузить субтитры')
        type_subs = 'Не удалось загрузить субтитры'
        return subs, type_subs

    for i in data['events']:
        if 'segs' in i:
            if 'dDurationMs' in i:
                item = {}
                item['tStartMs'] = i['tStartMs']
                item['dDurationMs'] = i['dDurationMs']

                item_sub = ''
                for j in i['segs']:
                    item_sub += str(j['utf8'])
                if len(item_sub) > 1:
                    item['segs'] = item_sub

                    subs.append(item)
    print(len(subs), 'subs.')

    return subs, type_subs










# dict_keys(['id', 'uploader', 'uploader_id', 'upload_date', 'title', 'thumbnail', 'duration', 'like_count', 'dislike_count', 'comment_count', 'formats', 'age_limit', 'tags', 'categories', 'cast', 'subtitles', 'thumbnails', 'timestamp', 'view_count', 'webpage_url', 'original_url', 'webpage_url_basename', 'webpage_url_domain', 'extractor', 'extractor_key', 'playlist', 'playlist_index', 'display_id', 'fulltitle', 'duration_string', 'requested_subtitles', '_has_drm', 'format_id', 'format_index', 'url', 'manifest_url', 'tbr', 'ext', 'fps', 'protocol', 'preference', 'quality', 'width', 'height', 'vcodec', 'acodec', 'dynamic_range', 'video_ext', 'audio_ext', 'vbr', 'abr', 'format', 'resolution', 'aspect_ratio', 'filesize_approx', 'http_headers'])
