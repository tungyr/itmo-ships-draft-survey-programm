import unittest
# from .. import temp
# from draft_survey.temp import sum
# import draft_survey.__init__
# sys.path.append('draft_survey')
print('__file__={0:<35} | __name__={1:<20} | __package__={2:<20}'.format(__file__, __name__, str(__package__)))
from draft_survey.widgets.anyvsl_eng import MainWindowAnyvslEng



class TestMainWindowEng(unittest.TestCase):

    def setUp(self):
        self.window = MainWindowAnyvslEng()

    def test1(self):
        self.assertTrue(True)


# class TestCase(unittest.TestCase):
#
#     def test_sum(self):
#         i = 6
#         result = sum(i)
#         self.assertEqual(result, 12)


if __name__ == '__main__':
    unittest.main()