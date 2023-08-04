
#!/usr/bin/env python
# -*- coding: utf-8 -*-
import json
import numpy as np
import cv2

file_name = 'data/19368_640x360' # フリー素材（白鳥）
# file_name = 'IMG_3570' # 撮影した野鳥
# file_name = '18381_640x360' # フリー素材（カモ）
# file_name = 'data/19368_1280x720' # フリー素材（白鳥）

# img = cv2.imread('map_takara_chizu.png')
img = cv2.imread('image.jpg')

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
        cv2.imwrite("image.jpg", f)

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

        if not len(t['Label']['Instances'])==0:

            if 'BoundingBox' in t['Label']['Instances'][0]:
                box = t['Label']['Instances'][0]['BoundingBox']

                x = round(width * box['Left'])
                y = round(height * box['Top'])
                w = round(width * box['Width'])
                h = round(height * box['Height'])

                # 長方形描画(画像, 左上座標 (X, Y), 右下座標 (X, Y), 色 (B, G, R), 線の太さ)
                cv2.rectangle(frame[i], (x, y), (x + w, y + h), (255, 255, 255), 3)
                cv2.putText(frame[i], str(t['Label']['Name']), (x, y - 9),
                            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)

            if 'Bird' in t['Label']['Name']:
                box = t['Label']['Instances'][0]['BoundingBox']

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

    # Writeメソッドに1フレームずつ渡して動画を書き出す
    for d in frame:
        video.write(d)
    video.release()

def output_map(video_fps, frame):
    """地図出力関数

    Parameters:
    ----------
    map : ???
        地図の元となる画像
    frame : list
        描画情報
    
    Returns:
    ----------
    None
    """
    for t in target:
        i = t['Timestamp']

        if not len(t['Label']['Instances'])==0:
            if 'BoundingBox' in t['Label']['Instances'][0]:
                box = t['Label']['Instances'][0]['BoundingBox']

                x = round(width * box['Left'])
                y = round(height * box['Top'])
                w = round(width * box['Width'])
                h = round(height * box['Height'])

                # 長方形描画(画像, 左上座標 (X, Y), 右下座標 (X, Y), 色 (B, G, R), 線の太さ)
                cv2.rectangle(img, (x, y), (x + w, y + h), (255, 255, 255), 3)
                # cv2.putText(frame[i], str(t['Label']['Name']), (x, y - 9),
                #             cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 255, 255), 3)
    return

#### 処理開始 ####

# 動画読み込み関数呼び出し
video, video_fps, frame = loading_video(file_name)
_, height, width, _ = frame.shape

lavels = get_lavels(file_name)

target = enumerate_lavels(lavels)

write_boundingbox(frame, target)

output_map(video_fps, frame)

# 地図出力
cv2.imwrite('sample_after.png', img)