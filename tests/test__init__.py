import unittest
from . import __init__

def test_main_win_fields():
    i = 2
    win = bealuna_eng.MainWindowEng()
    for draft_line in win.draft_lines:
        while i != 7.8:
            draft_line.setText(str(i + 0.1))
        else:
            continue



test_main_win_fields()
# if __name__ == '__main__':
#     unittest.main()