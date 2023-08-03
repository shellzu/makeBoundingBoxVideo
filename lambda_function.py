
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import numpy as np
import cv2

file_name = 'IMG_3656_lambda'

def loading_video(file_name):
    """動画読み込み関数

    Parameters:
    ----------
    file_name : str
        動画ファイル名
    
    Returns:
    ----------
    video : class
        VideoCaptureクラス
    video_fps : int
        単位時間あたりに処理させるコマ数
    frame : list
        フレームリスト
    """
    video = cv2.VideoCapture('{}.mp4'.format(file_name))
    video_fps = video.get(cv2.CAP_PROP_FPS)
    
    frame = []
    while True:
        is_good, f = video.read()
        if not is_good:
            break
        frame.append(f)
    # print(np.array(frame))
    frame = np.array(frame)
    return video, video_fps, frame

# 動画読み込み関数呼び出し
video, video_fps, frame = loading_video(file_name)

# 何してるか不明(加工前後で差分なし)
_, height, width, _ = frame.shape

def get_persons(file_name):
    """persons取得関数

    Parameters:
    ----------
    file_name : str
        Rekognitionによって生成されるJSONファイル名
    
    Returns:
    ----------
    persons : dict
        persons(人を認識した場合に出力される階層)
    """
    # JSONデータ読込
    with open('{}.json'.format(file_name), 'r') as f:
        json_data = json.load(f)

    ####### json_data['Labels']に変更 #######
    return json_data['Persons']

persons = get_persons(file_name)

def enumerate_persons(persons):
    """personsを数え上げる関数
       fpsを元にperson['Timestamp']を加工して詰めなおし

    Parameters:
    ----------
    persons : list
        personリスト
    
    Returns:
    ----------
    target : list
        ターゲットリスト
    """
    target = []
    for i, person in enumerate(persons):
        # ex. 3040 → 76
        person['Timestamp'] = int(person['Timestamp']*video_fps/1000)
        target.append(person)
    return target

target = enumerate_persons(persons)

def write_boundingbox(frame, target):
    """バウンディングボックス描画関数


    Parameters:
    ----------
    frame : list
        フレームリスト
    target : list
        ターゲットリスト
    
    Returns:
    ----------
    None
    """

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
            cv2.putText(frame[i], str('Face {}'.format(t['Person']['Index'])), (x, y - 9),
                        cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 3)
        return

write_boundingbox(frame, target)

def output_video(video_fps, frame):
    """解析結果動画出力関数

    Parameters:
    ----------
    video_fps : int
        コマ数
    frame : list
        フレームリスト
    
    Returns:
    ----------
    None
    """

    # 解析結果動画出力
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    video = cv2.VideoWriter('{}_rect.mp4'.format(file_name), fourcc, video_fps, (width, height))

    for d in frame:
        video.write(d)
    video.release()

output_video(video_fps, frame)