import unittest
import lambda_function

class TestFunc(unittest.TestCase):
    def test_func(self):
        file_name = 'IMG_3656_lambda'
        expected1, expected2 = 'VideoCapture', 25.0
        actual1, actual2 = lambda_function.loading_video(file_name)
        self.assertEqual(expected1, type(actual1).__name__) # 返却値1はクラス名で比較
        self.assertEqual(expected2, actual2)

if __name__ == '__main__':
    unittest.main()