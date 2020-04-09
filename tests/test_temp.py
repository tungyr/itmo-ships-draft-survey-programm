import pkgutil

import sys

print(sys.path)


search_path = ['..'] # Используйте None, чтобы увидеть все модули, импортируемые из sys.path
all_modules = [x[1] for x in pkgutil.iter_modules(path=search_path)]
print(all_modules)

import unittest
# from .. import temp
# from draft_survey.temp import sum
# import draft_survey.__init__
# sys.path.append('draft_survey')
print('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(__file__,__name__,str(__package__)))
from ..temp import sum
# from ..__init__ import aft_dist



# class TestCase(unittest.TestCase):
#
#     def test_aft_dist(self):
#         i = 6
#         result = aft_dist(i)
#         self.assertEqual(result, -2.06)

class TestCase(unittest.TestCase):

    def test_sum(self):
        i = 6
        result = sum(i)
        self.assertEqual(result, 12)


if __name__ == '__main__':
    unittest.main()