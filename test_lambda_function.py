import unittest
import lambda_function
import pathlib
import datetime
import os

class TestFunc(unittest.TestCase):
    def test_loading_video(self):
        file_name = 'IMG_3656_lambda'
        expected1, expected2, expected3 = 'VideoCapture', 25.0, 'ndarray'
        actual1, actual2, actual3 = lambda_function.loading_video(file_name)
        self.assertEqual(expected1, type(actual1).__name__) # 返却値1はクラス名で比較
        self.assertEqual(expected2, actual2)
        self.assertEqual(expected3, type(actual3).__name__) # 返却値3はクラス名で比較

    def test_get_persons(self):
        file_name = 'IMG_3656_lambda'
        expected = {'Timestamp': 0, 'Person': {'Index': 0, 'BoundingBox': {'Width': 0.17656250298023224, 'Height': 0.7138888835906982, 'Left': 0.16562500596046448, 'Top': 0.11388888955116272}}}
        actual = lambda_function.get_persons(file_name)
        self.assertEqual(expected, actual[0])
    
    def test_enumerate_persons(self):
        file_name = 'IMG_3656_lambda'
        persons = lambda_function.get_persons(file_name)
        expected = {'Timestamp': 0, 'Person': {'Index': 0, 'BoundingBox': {'Width': 0.17656250298023224, 'Height': 0.7138888835906982, 'Left': 0.16562500596046448, 'Top': 0.11388888955116272}}}
        actual = lambda_function.enumerate_persons(persons)
        self.assertEqual(expected, actual[0])
    
    # 結合テスト
    def test_write_boundingbox(self):
        file_name = 'IMG_3656_lambda'
        persons = lambda_function.get_persons(file_name)
        video, video_fps, frame = lambda_function.loading_video(file_name)
        target = lambda_function.enumerate_persons(persons)
        expected = None
        actual = lambda_function.write_boundingbox(frame, target)
        self.assertEqual(expected, actual)

    # 結合テスト
    def test_output_video(self):
        file_name = 'IMG_3656_lambda'
        expected = datetime.datetime.now().strftime("%Y/%m/%d %H:%M")
        video, video_fps, frame = lambda_function.loading_video(file_name)
        lambda_function.output_video(video_fps, frame)
        
        output_file_name = pathlib.Path('{}.mp4'.format(file_name))
        update_time = os.path.getatime(output_file_name)
        actual = datetime.datetime.fromtimestamp(update_time).strftime("%Y/%m/%d %H:%M")
        self.assertEqual(expected, actual)

if __name__ == '__main__':
    unittest.main()