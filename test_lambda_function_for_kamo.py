import unittest
import lambda_function
import pathlib
import datetime
import os

class TestFunc(unittest.TestCase):
    def test_loading_video(self):
        file_name = '19368_640x360'
        expected1, expected2, expected3 = 'VideoCapture', 29.97002997002997, 'ndarray'
        actual1, actual2, actual3 = lambda_function.loading_video(file_name)
        self.assertEqual(expected1, type(actual1).__name__) # 返却値1はクラス名で比較
        self.assertEqual(expected2, actual2)
        self.assertEqual(expected3, type(actual3).__name__) # 返却値3はクラス名で比較

if __name__ == '__main__':
    unittest.main()