
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


#### 処理開始 ####

# 動画読み込み関数呼び出し
video, video_fps, frame = loading_video(file_name)
