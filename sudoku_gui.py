import Tkinter as tk
import functools 
from sudoku_functions import *

class Sudoku_gui(object):
    
    def __init__(self,sudoku, w=tk.Tk()):
        self.sudoku=sudoku #contains the numbers to be displayed
        self.w=w #the main window
        self.w.title("Sudoku tools v 0.1")
        self.w.geometry("1000x1000")
        self.designmode=True
        self.show_opt=tk.BooleanVar()

        menu=Sudoku_gui_menu(self)
        
        #c=canvas (area where the sudoku is drawn
        c_width = w.winfo_width()*.9
        c_height = w.winfo_height()*.9
        self.c = tk.Canvas(w, width=c_width, height=c_height)
        self.c.configure(background="white")
        self.c.pack() #place somewhere
        self.w.update_idletasks() 
        self.draw_sudoku()
        
        #buttons: reset options, update options, apply solving algorithm
        self.bt_ckopt=tk.Button(w,text="check options", 
                    command=self.update_options )
        self.bt_ckopt.pack()
        self.bt_applyAlg=tk.Button(w,text="apply solving step", 
                    command=self.solve_step )
        self.bt_applyAlg.pack()
        self.sb_alg=tk.Spinbox(w, values=self.sudoku.alg_list)
        self.sb_alg.pack()  
        #self.ck_mode = tk.Checkbutton(self.w, text="design mode", variable=self.designmode)
        #self.ck_mode.pack()
        self.ck_show_opt = tk.Checkbutton(self.w, text="show options", 
                    variable=self.show_opt, command=self.ck_show_opt)        
        self.ck_show_opt.pack()  

    def solve_step(self):  
        self.sudoku.update_options()  
        if self.sb_alg.get() == "find unique":
            self.sudoku.find_unique_option()
        elif self.sb_alg.get() == "hidden singlet":
            self.sudoku.hidden_singlet()
        elif self.sb_alg.get() == "conjugate pair":
            self.sudoku.conjugate_pair()
        else:
            print("this algorithm needs to be defined first")
        self.draw_sudoku(new=True)       

    def restart(self):
        self.sudoku=Sudoku(self.sudoku.start_num)
        self.draw_sudoku(new=True)   


    def new_sudoku(self,start_num=Sudoku.empty_sudoku):
        self.sudoku=Sudoku(start_num)
        self.draw_sudoku(new=True)   
     
    def update_options(self):
        print("update options")
        self.sudoku.update_options()
        self.draw_sudoku(new=True)

    def ck_show_opt(self):
        print ("show options is " + str(self.show_opt.get()))
        self.draw_sudoku(new=True)       
       


    def draw_number(self, i,j ):
        c=self.c
        o_num=self.sudoku.opt_num[i,j]
        s_num=self.sudoku.start_num[i,j]
        f_num=self.sudoku.solved_num[i,j]
        h_step=c.winfo_width()/9
        v_step=c.winfo_height()/9
        x_pos=v_step*(i+.5)
        y_pos=h_step*(j+.5)
        big_font=("Helvetica",32)
        small_font=("Helvetica",12)
        if s_num == 0: #not defined at start
            if f_num != 0: # already found -> draw green number
                #print("draw green {} at {},{}".fromat(o_num[0],i,j))
                c.create_text(x_pos, y_pos,text=str(f_num),fill='green',font=big_font )
            elif sum(o_num) == 0: #contradiction -> draw red X
                #print("found contradiction at {},{}".format(i,j))
                c.create_text(x_pos, y_pos,text='X',fill='red',font=big_font )
            elif self.show_opt.get():    
                #draw all options
                #print("found options at {},{}: ".format(i,j) + ",".join(str(x) for x in o_num))
                y_pos+=h_step*.4
                for opt in range(9):
                    if o_num[opt]:
                        #print("print {}".format(opt))
                        c.create_text(v_step*(i+float(opt+1)/10), y_pos,text=str(opt+1),fill='black',font=small_font )
        else:
            #print("draw black {} at {},{}".format(s_num,i,j) )
            c.create_text(x_pos, y_pos,text=str(s_num),fill='black',font=big_font )
            if sum(o_num) == 0:   # contradiction: cross out
                print("contradiction with start number {} at {},{}".format(s_num,i,j) )
                c.create_text(x_pos, y_pos,text='X',fill='red',font=big_font )
            

    def draw_sudoku(self, new=False):
        c=self.c
        if new:
            c.delete("all")
        h_step=c.winfo_width()/9
        v_step=c.winfo_height()/9
        #draw grid
        print( "stepsize: " + str(h_step) + "x" + str(v_step) ) 
        for i in range(10):
            lwd = 3 if i % 3 == 0 else 1
            c.create_line(0, i*v_step, c.winfo_width(), i*v_step, width=lwd, fill="black")
        for i in range(10):
            lwd = 3 if i % 3 == 0 else 1
            c.create_line(i*h_step,0,i*h_step, c.winfo_height(), width=lwd, fill="black")
        #draw numbers
        for i in range(9):
            for j in range(9):
                self.draw_number(i,j)
    def set_design_mode(self):
        if not self.designmode:
            print("now in design mode")
            self.designmode=True
            self.sudoku=Sudoku(self.sudoku.start_num)
            self.draw_sudoku(new=True)  
        else:
            print("already in design mode")


    def set_solve_mode(self):
        print("now in solve mode")
        self.designmode=False



class Sudoku_gui_menu(object):

    def __init__(self,gui):
        # top menue (just for testing, not really populated)
        menubar = tk.Menu(gui.w)
        puzzle_men = tk.Menu(menubar, tearoff=0)
        new_men=tk.Menu(menubar, tearoff=0)
        mode_men=tk.Menu(menubar, tearoff=0)

        for i in range(len(gui.sudoku.sudoku_start_num)):
            new_men.add_command(label=Sudoku.sudoku_start_name[i], 
                    #command=lambda: gui.new_sudoku(Sudoku.sudoku_start_num[i]) )
                    command=functools.partial(gui.new_sudoku, Sudoku.sudoku_start_num[i]) )
        mode_men.add_command(label="design", command=gui.set_design_mode)
        mode_men.add_command(label="solve", command=gui.set_solve_mode)
            
        #men1.add_command(label="Open", command=self.open_from_file)
        #men1.add_command(label="Save", command=self.save_current)
        #puzzle_men.add_command(label="check options", command=self.update_options)
        #puzzle_men.add_command(label="redraw", command=lambda: self.draw_sudoku(new=True))
        puzzle_men.add_command(label="Clear", command=gui.restart)
        puzzle_men.add_cascade(label="New", menu=new_men)
        puzzle_men.add_cascade(label="Mode", menu=mode_men)
        puzzle_men.add_separator()
        puzzle_men.add_command(label="Exit", command=gui.w.quit)
        menubar.add_cascade(label="Puzzle", menu=puzzle_men)


        gui.w.config(menu=menubar)
        #not sure when i need to call this
        gui.w.update_idletasks()  



