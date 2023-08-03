
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import numpy as np
import cv2

file_name = 'IMG_3656_lambda'

# 動画読込
video = cv2.VideoCapture('{}.mp4'.format(file_name))
video_fps = video.get(cv2.CAP_PROP_FPS)

frame = []
while True:
    is_good, f = video.read()
    if not is_good:
        break
    frame.append(f)
print(np.array(frame))
frame = np.array(frame)

_, height, width, _ = frame.shape

# JSONデータ読込
with open('{}.json'.format(file_name), 'r') as f:
    json_data = json.load(f)

####### json_data['Labels']に変更 #######
persons = json_data['Persons']
target = []

for i, person in enumerate(persons):
    person['Timestamp'] = int(person['Timestamp']*video_fps/1000)
    print(person)
    target.append(person)

# 動画にJSONの情報を書き込む
for t in target:
    i = t['Timestamp']
    ####### t['Person']をt['Labels']['Instances']に変更 #######
    if 'BoundingBox' in t['Person']:
        box = t['Person']['BoundingBox']

        x = round(width * box['Left'])
        y = round(height * box['Top'])
        w = round(width * box['Width'])
        h = round(height * box['Height'])

        cv2.rectangle(frame[i], (x, y), (x + w, y + h), (255, 255, 255), 3)
        cv2.putText(frame[i], str(t['Person']['Index']), (x, y - 9),
                    cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)
    ####### t['Labels']['Name']が"Duck"の場合 #######
    if 'Face' in t['Person']:
        
        ####### t['Labels']['Instances']['BoundingBox'] #######
        box = t['Person']['Face']['BoundingBox']

        x = round(width * box['Left'])
        y = round(height * box['Top'])
        w = round(width * box['Width'])
        h = round(height * box['Height'])

        cv2.rectangle(frame[i], (x, y), (x + w, y + h), (255, 0, 0), 3)
        # cv2.putText(frame[i], str('Face {}'.format(t['Person']['Index'])), (x, y - 9),
        #             cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 3)

# 解析結果動画出力
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
video = cv2.VideoWriter('{}_rect.mp4'.format(file_name), fourcc, video_fps, (width, height))

for d in frame:
    video.write(d)
video.release()
