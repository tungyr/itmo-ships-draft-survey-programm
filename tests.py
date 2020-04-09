import storage
import unittest

print(storage.aft_dist_find(1.1))

class TestStorage(unittest.TestCase):

    def test_aft_dist_find(self):
        A_mean = [1.1, 1.56, 3.97, 5.13, 5.4, 6.1239085, 6.99, 7.04999, 7.37]
        correct_value = [4.64, 3.84, -0.39, -1.9, -1.95, -2.07, -2.33, -2.4, -2.4]
        i = 0
        for value in A_mean:
            result = storage.aft_dist_find(value)
            print(value, '-', result)
            self.assertEqual(round(result, 2), correct_value[i])
            i += 1

    # def test_hydrostatic_find(self):
    #     MOMC = 2
    #     item = 4
    #     result = storage.hydrostatic_find(MOMC, item)
    #     self.assertEqual(result, 106.77)

