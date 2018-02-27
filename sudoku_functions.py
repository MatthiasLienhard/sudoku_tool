import math
import numpy as np
import copy

##########
# Sudoku #
# 
##########
__author__ = "Matthias Lienhard"
__email__ = "mali270484@gmail.com"
__version__ = "0.01"


class Sudoku(object):
    def __init__(self, start_num):
        self.start_num=start_num #9x9 array storing the initially known numbers 0=unknown
        self.solved_num=copy.deepcopy(start_num) # 9x9 matrix storing the identified (solved) numbers
        #initialized as start_num, deepcopy to copy also the inner lists
        self.opt_num=np.ones((9,9,9), dtype=bool) # 9x9 matrix with bool arrays of length 9 to encode the options for each field
        # initialize opt_num
        for i in range (9):
            for j in range(9):
                if start_num[i][j] != 0:
                    for k in range(9):
                        if k+1 != start_num[i][j]: self.opt_num[i][j][k]=False


    def update_options(self):
        #for each solved number, check rows, cols and boxes and remove corresponding value from number
        print("update options in function")
        opt_count=0 #number of options removed
        for i in range (9):
            for j in range(9):
                if self.solved_num[i][j] != 0: # found solved number
                    n_idx=self.solved_num[i][j]-1 #corresponding index in bool arrays of opt_num
                    #upper left field of box                    
                    bx_of=(i/3)*3#math.floor(i/3)*3 
                    by_of=(j/3)*3#math.floor(j/3)*3
                    for k in range(9): #iterate over row, col and box
                        #indices for kth field of box
                        bx = bx_of + (k % 3) #floor(k / 3)
                        by = by_of + (k / 3)
                        if k != j and self.opt_num[i][k][n_idx]: 
                            #kth element of column
                            self.opt_num[i][k][n_idx]=False
                            opt_count+=1
                        if k != i and self.opt_num[k][j][n_idx]:
                            #kth element of row
                            self.opt_num[k][j][n_idx]=False
                            opt_count+=1
                        if (bx != i or by != j) and self.opt_num[bx][by][n_idx]:
                            #kth element of box
                            self.opt_num[bx][by][n_idx]=False
                            opt_count+=1
        print("rouled out " +str(opt_count)+ " options")
        return opt_count

    def find_unique_option(self):
        #look for fields with only one option left
        solved_count=0
        for i in range(9):
            for j in range(9):
                if sum(self.opt_num[i][j]) == 1 and self.solved_num[i][j]==0:
                    #new solved filed
                    solved_count+=1
                    self.soved_num[i][j]=np.where(self.opt_num[i][j])
        return solved_count
    
    def find_last_option(self):
        #check rows, cols and boxes for options present in one field only
        solved_count=0
        for i in range(9): #iterate over all rows, cols and boxes
            unsolved=np.ones((3,9), dtype=bool)
            nopt=np.full((3,9),fill_value=9, dtype=int) 
            firstk=np.empty((3,9), dtype=int)
            for k in range(9): #field within ith row, col, box
                if self.solved_num[i][k]!=0: unsolved[0][k]=False
                else: nopt[0][self.opt_num[i][k]] += 1
                    
        return solved_count
    #add more fancy algorithms



####################
#predefined sudokus#
####################
#empty_sudoku to test
empty_sudoku = np.zeros((9,9), dtype=int)
empty_sudoku[4][1]=8
empty_sudoku[0][8]=8
#easy sudoku
easy_sudoku = [[0,0,0,0,0,4,0,2,8],[4,0,6,0,0,0,0,0,5],[1,0,0,0,3,0,6,0,0],[0,0,0,3,0,1,0,0,0],[0,8,7,0,0,0,1,4,0],[0,0,0,7,0,9,0,0,0],[0,0,2,0,1,0,0,0,3],[9,0,0,0,0,0,5,0,7],[6,7,0,4,0,0,0,0,0]]
#another sudoku



