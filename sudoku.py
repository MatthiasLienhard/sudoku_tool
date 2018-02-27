#!/usr/bin/env python2
from sudoku_functions import *
from sudoku_gui import *
sudoku=Sudoku(easy_sudoku)
gui=Sudoku_gui(sudoku=sudoku)
gui.w.mainloop()
