import unittest

from draft_survey import storage

# class TestConnection(unittest.TestCase):
#     @unittest.mock('storage.connect.sqlite3.connect')
#     def test_connection(self, mockconnect):
#         # storage.connect()
#         # mockconnect.assert_called()
#
#         connection = storage.connect()
#         self.assertIsNotNone(connection)
#         mockconnect.assert_called()

data = [[(5.5, -1.97), (5.4, -1.95)], 5.46, 1]
result = storage.interpolation(*data)
print(result)

class TestInterpolation(unittest.TestCase):

    def integers(self):
        data = [[(5.5, -1.97), (5.4, -1.95)], 5.46, 1]
        result = storage.interpolation(*data)
        print("result:", result)
        self.assertEqual(result, -1.962)


if __name__ == '__main__':
    unittest.main()