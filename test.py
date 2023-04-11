

# s = 'а'
# s = '\U0001f449'
# print(s.encode('utf-8'))

frames = ['keyframe-00001.jpg', 'keyframe-00002.jpg', 'keyframe-00003.jpg', 'keyframe-00004.jpg', 'keyframe-00005.jpg', 'keyframe-00006.jpg', 'keyframe-00007.jpg', 'keyframe-00008.jpg', 'keyframe-00009.jpg', 'keyframe-00010.jpg', 'keyframe-00011.jpg', 'keyframe-00012.jpg', 'keyframe-00013.jpg', 'keyframe-00014.jpg', 'keyframe-00015.jpg', 'keyframe-00016.jpg', 'keyframe-00017.jpg', 'keyframe-00018.jpg', 'keyframe-00019.jpg', 'keyframe-00020.jpg', 'keyframe-00021.jpg']

depth_frames = 5

def fnc(frames, depth_frames):
    for i in range(0, len(frames), depth_frames):
        yield frames[i:i + depth_frames]


blocks_frames = list(fnc(frames, depth_frames))

for i in blocks_frames:
    print(i)

# print(blocks_frames)
