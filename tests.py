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
        momc = [1.5, 1.625123, 2.0899, 5.45999, 7.789999, 7.9, 7.96199]
        db_column = [2, 3, 4, 6]
        correct_values = [[2117.99, 2321.322, 3070.999, 8728.083, 12943.598, 13149.28, 13264.918],
                          [15.82, 15.873, 16.1, 17.49, 18.76, 18.801],
                          [102.85, 103.673, 137.950, 163.225, 164.63, 165.457],
                          [64.958, 64.912, 64.101, 57.480, 57.479, 57.461]]
        i = 0
        for column in db_column:
            j = 0
            for momc_value in momc:
                result = storage.hydrostatic_find(momc_value, column)
                result = round(result, 3)
                print(f'column: {column} - momc: {momc_value} -> '
                      f'result: {result} - correct: {correct_values[i][j]}')
                self.assertEqual(result, correct_values[i][j])
                j += 1
            i += 1

ex = TestStorage()
ex.test_hydrostatic_find()