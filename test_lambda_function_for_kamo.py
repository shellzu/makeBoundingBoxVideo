import unittest
import lambda_function_for_kamo
import pathlib
import datetime
import os

file_name = 'data/19368_640x360'

class TestFunc(unittest.TestCase):
    def test_loading_video(self):
        expected1, expected2, expected3 = 'VideoCapture', 29.97002997002997, 'ndarray'
        actual1, actual2, actual3 = lambda_function_for_kamo.loading_video(file_name)
        self.assertEqual(expected1, type(actual1).__name__) # 返却値1はクラス名で比較
        self.assertEqual(expected2, actual2)
        self.assertEqual(expected3, type(actual3).__name__) # 返却値3はクラス名で比較

    def test_get_lavels(self):
        expected = {'Timestamp': 0, 'Label': {'Name': 'Adult', 'Confidence': 93.61540222167969, 'Instances': [{'BoundingBox': {'Width': 0.1031993180513382, 'Height': 0.31720104813575745, 'Left': 0.21056178212165833, 'Top': 0.0007387797231785953}, 'Confidence': 98.90129852294922}], 'Parents': [{'Name': 'Person'}], 'Aliases': [], 'Categories': [{'Name': 'Person Description'}]}}
        actual = lambda_function_for_kamo.get_lavels(file_name)
        self.assertEqual(expected, actual[0])

    def test_enumerate_lavels(self):
        lavels = lambda_function_for_kamo.get_lavels(file_name)
        expected = {'Timestamp': 0, 'Label': {'Name': 'Adult', 'Confidence': 93.61540222167969, 'Instances': [{'BoundingBox': {'Width': 0.1031993180513382, 'Height': 0.31720104813575745, 'Left': 0.21056178212165833, 'Top': 0.0007387797231785953}, 'Confidence': 98.90129852294922}], 'Parents': [{'Name': 'Person'}], 'Aliases': [], 'Categories': [{'Name': 'Person Description'}]}}
        actual = lambda_function_for_kamo.enumerate_lavels(lavels)
        self.assertEqual(expected, actual[0])

    # 結合テスト
    def test_write_boundingbox(self):
        lavels = lambda_function_for_kamo.get_lavels(file_name)
        video, video_fps, frame = lambda_function_for_kamo.loading_video(file_name)
        target = lambda_function_for_kamo.enumerate_lavels(lavels)
        expected = None
        actual = lambda_function_for_kamo.write_boundingbox(frame, target)
        self.assertEqual(expected, actual)

    # 結合テスト
    def test_output_video(self):
        expected = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")
        video, video_fps, frame = lambda_function_for_kamo.loading_video(file_name)
        lambda_function_for_kamo.output_video(video_fps, frame)
        
        output_file_name = pathlib.Path('{}.mp4'.format(file_name))
        update_time = os.path.getatime(output_file_name)
        actual = datetime.datetime.fromtimestamp(update_time).strftime("%Y/%m/%d %H:%M")
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()