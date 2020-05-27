import unittest

import storage

class TestStorage(unittest.TestCase):

    def test_aft_dist_data(self):
        a_mean = [1.1, 1.56, 3.97, 5.13, 5.4, 6.1239085, 6.99, 7.04999, 7.37]
        correct_values = [4.64, 3.84, -0.39, -1.9, -1.95, -2.07, -2.33, -2.4, -2.4]
        i = 0
        print("\n", "id:", self.id())
        for value in a_mean:
            result = storage.aft_dist_data(value)
            self.assertEqual(round(result, 2), correct_values[i])
            i += 1

    def test_hydrostatic_data(self):
        momc = [1.5, 1.625123, 2.0899, 5.45999, 7.789999, 7.9, 7.96199]
        db_column = [2, 3, 4, 6]
        correct_values = [[2117.99, 2321.322, 3070.999, 8728.083, 12943.598, 13149.28, 13264.918],
                          [15.82, 15.873, 16.1, 17.49, 18.72, 18.76, 18.801],
                          [102.85, 103.673, 107.619, 134.2, 163.225, 164.63, 165.457],
                          [64.958, 64.911, 64.775, 60.882, 57.48, 57.479, 57.461]]
        i = 0
        print("\n", "id:", self.id())
        for column in db_column:
            j = 0
            for momc_value in momc:
                result = storage.hydrostatic_data(momc_value, column)
                result = round(result, 3)
                print(f'column: {column} - momc: {momc_value} -> '
                      f'result: {result} - correct: {correct_values[i][j]}')
                self.assertEqual(result, correct_values[i][j])
                j += 1
            i += 1

if __name__ == '__main__':
   unittest.main()