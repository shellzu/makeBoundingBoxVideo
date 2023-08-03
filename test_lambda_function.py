import unittest
import lambda_function

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

if __name__ == '__main__':
    unittest.main()