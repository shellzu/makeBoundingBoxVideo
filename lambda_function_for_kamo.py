
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import numpy as np
import cv2

file_name = '19368_640x360'

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

def get_lavels(file_name):
    """lavels取得関数

    Parameters:
    ----------
    file_name : str
        Rekognitionによって生成されるJSONファイル名
    
    Returns:
    ----------
    lavels : dict
        ラベルズ
    """
    # JSONデータ読込
    with open('{}.json'.format(file_name), 'r') as f:
        json_data = json.load(f)

    return json_data['Labels']

def enumerate_lavels(lavels):
    """lavelsを数え上げる関数
       fpsを元にperson['Timestamp']を加工して詰めなおし

    Parameters:
    ----------
    lavels : list
        personリスト
    
    Returns:
    ----------
    target : list
        ターゲットリスト
    """
    target = []
    for i, lavel in enumerate(lavels):
        # ex. 3040 → 76
        lavel['Timestamp'] = int(lavel['Timestamp']*video_fps/1000)
        target.append(lavel)
    return target

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
        if 'BoundingBox' in t['Label']['Instances']:
            box = t['Label']['Instances']['BoundingBox']
            print(box)

            x = round(width * box['Left'])
            y = round(height * box['Top'])
            w = round(width * box['Width'])
            h = round(height * box['Height'])

            cv2.rectangle(frame[i], (x, y), (x + w, y + h), (255, 255, 255), 3)
            # cv2.putText(frame[i], str(t['Label']['Instances']['Index']), (x, y - 9),
            #             cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)
        
        if 'Bird' in t['Label']:
            box = t['Label']['Instances']['BoundingBox']

            # Persons：
            # {'Timestamp' 0, 'Person' {'Index' 0, 'BoundingBox' {'Width' 0.17656250298023224, 'Height'

            # Labels：
            # {'Timestamp': 0, 'Label': {'Name': 'Bird', 'Confidence': 94.80776977539062, 'Instances': [
            # {'BoundingBox': {'Width': 0.14320507645606995, 'Height'

            x = round(width * box['Left'])
            y = round(height * box['Top'])
            w = round(width * box['Width'])
            h = round(height * box['Height'])

            cv2.rectangle(frame[i], (x, y), (x + w, y + h), (255, 0, 0), 3)
            # cv2.putText(frame[i], str('Face {}'.format(t['Person']['Index'])), (x, y - 9),
            #             cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 3)
    return

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

#### 処理開始 ####

# 動画読み込み関数呼び出し
video, video_fps, frame = loading_video(file_name)

# 何してるか不明(加工前後で差分なし)
_, height, width, _ = frame.shape

lavels = get_lavels(file_name)

target = enumerate_lavels(lavels)

write_boundingbox(frame, target)

output_video(video_fps, frame)