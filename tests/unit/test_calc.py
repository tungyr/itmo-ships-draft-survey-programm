import unittest
from draft_survey import calc

class Test_aft_dist(unittest.TestCase):
    def test_aft_dist(self):
        self.assertEqual(calc.aft_dist(1.5), 1.5)

print(calc.aft_dist(7))
