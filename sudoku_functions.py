import math
import numpy as np
import copy

##########
# Sudoku #
##########
__author__ = "Matthias Lienhard"
__email__ = "mali270484@gmail.com"
__version__ = "0.01"


class Sudoku(object):
    alg_list=("find unique", "hidden singlet")
    def __init__(self, start_num):
        self.start_num=start_num #9x9 array storing the initially known numbers 0=unknown
        self.solved_num=copy.deepcopy(start_num) # 9x9 matrix storing the identified (solved) numbers
        #initialized as start_num, deepcopy to copy also the inner lists
        self.opt_num=np.ones((9,9,9), dtype=bool) # 9x9 matrix with bool arrays of length 9 to encode the options for each field
        # initialize opt_num
        for i in range (9):
            for j in range(9):
                if start_num[i,j] != 0:
                    for k in range(9):
                        if k+1 != start_num[i,j]: self.opt_num[i,j,k]=False

    @classmethod
    def get_index(cls, n, k,what="row", elem=0):
        if what=="column":
            i=n; j=k
        elif what =="row":
            i=k; j=n
        elif what == "box":
            i= (n * 3 ) % 9 + k % 3
            j= (n // 3) * 3 + k // 3
            #print ("index of box {}, {}th field: {},{}".format(n,k,i,j))
        else:
            raise ValueError('index not found for '+what)
        if elem == 0:
            return (i,j)
        else:
            return (i,j,elem)

    @classmethod
    def get_set(cls, idx, what="row"):
        if what=="row":
            n=idx[0]
        elif what =="column":
            n=idx[1]
        elif what == "box":
            n=(idx[0] // 3) * 3 + idx[1] // 3
            #print("box at {},{}: {}".format(idx[0],idx[1],n))
        else:
            raise ValueError('index not found for '+what)
        return n
     

    def update_options(self):
        #for each solved number, check rows, cols and boxes and remove corresponding value from number
        print("update options in function")
        opt_count=0 #number of options removed
        for i in range (9):
            for j in range(9):
                if self.solved_num[i,j] != 0: # found solved number
                    n_idx=self.solved_num[i,j]-1 #corresponding index in bool arrays of opt_num
                    #upper left field of box                    
                    bx_of=(i//3)*3#math.floor(i/3)*3 
                    by_of=(j//3)*3#math.floor(j/3)*3
                    for k in range(9): #iterate over row, col and box
                        #indices for kth field of box
                        bx = bx_of + (k % 3) 
                        by = by_of + (k // 3)#floor(k / 3)
                        if k != j and self.opt_num[i,k,n_idx]: 
                            #kth element of column
                            self.opt_num[i,k,n_idx]=False
                            opt_count+=1
                        if k != i and self.opt_num[k,j,n_idx]:
                            #kth element of row
                            self.opt_num[k,j,n_idx]=False
                            opt_count+=1
                        if (bx != i or by != j) and self.opt_num[bx,by,n_idx]:
                            #kth element of box
                            self.opt_num[bx,by,n_idx]=False
                            opt_count+=1
        print("removed " +str(opt_count)+ " options")
        return opt_count

    def find_unique_option(self):
        #look for fields with only one option left
        solved_count=0
        for i in range(9):
            for j in range(9):
                if sum(self.opt_num[i,j]) == 1 and self.solved_num[i,j]==0:
                    #new solved filed
                    solved_count+=1
                    self.solved_num[i,j]=np.where(self.opt_num[i,j])[0][0]+1
        print("unique options solved {} fileds".format(solved_count)) 
        return solved_count
    
    def hidden_singlet(self):
        #check rows, cols and boxes for options present in one field only
        solved_count=0
        for t in ("row", "column", "box"):
            for n in range(9): #iterate over all rows, cols and boxes
                solved=np.zeros(9, dtype=bool)
                nopt=np.zeros(9, dtype=int) 
                seen_at=np.empty(9, dtype=int)
                for k in range(9): #field within ith row, col, box
                    idx=self.get_index(n,k,what=t)
                    if self.solved_num[idx]!=0: solved[self.solved_num[idx]-1]=True
                    nopt[self.opt_num[idx]] += 1
                    seen_at[self.opt_num[idx]] = k
                for num in range(9):
                    if not solved[num] and nopt[num] == 1:
                        idx=self.get_index(n,seen_at[num],what=t)
                        print(str(num+1) + " has only one option in "+t+" "+str(n+1)+" at " + str(seen_at[num]+1)+" "+str(idx))
                        solved_count+=1
                        self.solved_num[idx]=num+1
                        self.opt_num[idx]=np.zeros(9,dtype=bool)
                        self.opt_num[idx][num]=True                
        print("hidden singlets solved {} fileds".format(solved_count)) 
        return solved_count

    #add more fancy algorithms



####################
#predefined sudokus#
####################
#empty_sudoku to test
empty_sudoku = np.zeros((9,9), dtype=int)
empty_sudoku[4,1]=8
empty_sudoku[0,8]=8
#easy sudoku
easy_sudoku = np.array([[0,0,0,0,0,4,0,2,8],[4,0,6,0,0,0,0,0,5],[1,0,0,0,3,0,6,0,0],[0,0,0,3,0,1,0,0,0],[0,8,7,0,0,0,1,4,0],[0,0,0,7,0,9,0,0,0],[0,0,2,0,1,0,0,0,3],[9,0,0,0,0,0,5,0,7],[6,7,0,4,0,0,0,0,0]])
#another sudoku



