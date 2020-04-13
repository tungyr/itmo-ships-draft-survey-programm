import storage
import unittest

print(storage.aft_dist_find(1.1))

class TestStorage(unittest.TestCase):

    def test_aft_dist_find(self):
        a_mean = [1.1, 1.56, 3.97, 5.13, 5.4, 6.1239085, 6.99, 7.04999, 7.37]
        correct_values = [4.64, 3.84, -0.39, -1.9, -1.95, -2.07, -2.33, -2.4, -2.4]
        i = 0
        for value in a_mean:
            result = storage.aft_dist_find(value)
            print(value, '-', result)
            self.assertEqual(round(result, 2), correct_values[i])
            i += 1

    def test_hydrostatic_find(self):
        # momc = [1.5, 1.635, 2.0899, 3.99, 4.4444, 5.45999, 6.3111, 7.789999, 7.9]
        momc = [1.5, 1.635123, 2.0899, 3.999999, 4.4444, 5.45999, 6.3111, 7.789999, 7.9]
        db_column = [2, 3, 4, 6]
        correct_values = [2117.99, 2337.5471, 3070.8245]
        i = 0
        for column in db_column:
            for momc_value in momc:
                result = storage.hydrostatic_find(momc_value, column)
                print(f'column: {column} - momc: {momc_value} -> '
                      f'result: {result} - correct: {correct_values[i]}')
                self.assertEqual(round(result, 4), correct_values[i])
                i += 1

ex = TestStorage()
ex.test_hydrostatic_find()