
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

#### 処理開始 ####

# 動画読み込み関数呼び出し
video, video_fps, frame = loading_video(file_name)

# 何してるか不明(加工前後で差分なし)
_, height, width, _ = frame.shape

lavels = get_lavels(file_name)

target = enumerate_lavels(lavels)