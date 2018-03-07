import tkinter as tk
import tkinter.filedialog
import functools
from sudoku import *
import digit_recognition
##########
# Sudoku #
##########
__author__ = "Matthias Lienhard"
__email__ = "mali270484@gmail.com"
__version__ = "0.02"


class SudokuApp(tk.Tk):

    def __init__(self, sudoku=Sudoku()):
        tk.Tk.__init__(self)
        self.sudoku = sudoku  # contains the numbers to be displayed
        self.title("Sudoku tools v."+__version__)
        self.geometry("1000x1000")
        self.designmode = False
        self.show_opt = tk.BooleanVar(value=True)
        self.classifier=digit_recognition.DigitClassifier(filename='digits.csv', k=5)
        self.menu = SudokuAppMenu(self)
        # c=canvas (area where the sudoku is drawn
        self.fieldSz = min(self.winfo_width(),self.winfo_height()) * .1

        self.c = tk.Canvas(self, width=self.fieldSz*9, height=self.fieldSz*9)
        self.c.configure(background="white")
        self.c.pack()  # place somewhere
        self.update_idletasks()
        self.draw_sudoku()

        # buttons: reset options, update options, apply solving algorithm
        self.bt_ckopt = tk.Button(self, text="check options",
                                  command=self.update_options)
        self.bt_ckopt.pack()
        self.bt_applyAlg = tk.Button(self, text="apply solving step",
                                     command=self.solve_step)
        self.bt_applyAlg.pack()
        self.sb_alg = tk.Spinbox(self, values=list(self.sudoku.alg_list.keys()))
        self.sb_alg.pack()
        # self.ck_mode = tk.Checkbutton(self, text="design mode", variable=self.designmode)
        # self.ck_mode.pack()
        self.ck_show_opt = tk.Checkbutton(self, text="show options",
                                          variable=self.show_opt, command=self.ck_show_opt)

        self.btn1pressed = False
        self.c.bind("<Motion>", self.mousemove)
        self.c.bind("<ButtonPress-1>", self.mouse1press)
        self.c.bind("<ButtonRelease-1>", self.mouse1release)
        self.line=[]

        self.ck_show_opt.pack()

    def solve_step(self):
        self.sudoku.update_options()
        self.sudoku.alg_list[self.sb_alg.get()]()
        # if self.sb_alg.get() == "find unique":
        #    self.sudoku.find_unique_option()
        # elif self.sb_alg.get() == "hidden singlet":
        #    self.sudoku.hidden_singlet()
        # elif self.sb_alg.get() == "conjugate pair":
        #    self.sudoku.conjugate_pair()
        # else:
        #    print("this algorithm needs to be defined first")

        self.draw_sudoku(new=True)

    def restart(self):
        self.sudoku = Sudoku(self.sudoku.start_num)
        self.draw_sudoku(new=True)

    def new_sudoku(self, start_num=Sudoku.empty_sudoku):
        self.sudoku = Sudoku(start_num)
        self.draw_sudoku(new=True)

    def update_options(self):
        print("update options")
        self.sudoku.update_options()
        self.draw_sudoku(new=True)

    def ck_show_opt(self):
        print("show options is " + str(self.show_opt.get()))
        self.draw_sudoku(new=True)

    def draw_number(self, i, j):
        c = self.c
        o_num = self.sudoku.opt_num[i, j]
        s_num = self.sudoku.start_num[i, j]
        f_num = self.sudoku.solved_num[i, j]
        h_step = c.winfo_width() / 9
        v_step = c.winfo_height() / 9
        x_pos = v_step * (i + .5)
        y_pos = h_step * (j + .5)
        big_font = ("Helvetica", 32)
        small_font = ("Helvetica", 12)
        if s_num == 0:  # not defined at start
            if f_num != 0:  # already found -> draw green number
                # print("draw green {} at {},{}".fromat(o_num[0],i,j))
                c.create_text(x_pos, y_pos, text=str(f_num), fill='green', font=big_font)
            elif sum(o_num) == 0:  # contradiction -> draw red X
                # print("found contradiction at {},{}".format(i,j))
                c.create_text(x_pos, y_pos, text='X', fill='red', font=big_font)
            elif self.show_opt.get():
                # draw all options
                # print("found options at {},{}: ".format(i,j) + ",".join(str(x) for x in o_num))
                y_pos += h_step * .4
                for opt in range(9):
                    if o_num[opt]:
                        # print("print {}".format(opt))
                        c.create_text(v_step * (i + float(opt + 1) / 10), y_pos, text=str(opt + 1), fill='black',
                                      font=small_font)
        else:
            # print("draw black {} at {},{}".format(s_num,i,j) )
            c.create_text(x_pos, y_pos, text=str(s_num), fill='black', font=big_font)
            if sum(o_num) == 0:  # contradiction: cross out
                print("contradiction with start number {} at {},{}".format(s_num, i, j))
                c.create_text(x_pos, y_pos, text='X', fill='red', font=big_font)

    def draw_sudoku(self, new=False):
        c = self.c
        if new:
            c.delete("all")
        # draw grid
        print("stepsize: " + str(self.fieldSz))
        for i in range(10):
            lwd = 3 if i % 3 == 0 else 1
            c.create_line(0, i * self.fieldSz, c.winfo_width(), i * self.fieldSz, width=lwd, fill="black")
        for i in range(10):
            lwd = 3 if i % 3 == 0 else 1
            c.create_line(i * self.fieldSz, 0, i * self.fieldSz, c.winfo_height(), width=lwd, fill="black")
        # draw numbers
        for i in range(9):
            for j in range(9):
                self.draw_number(i, j)

    def set_design_mode(self):
        if not self.designmode:
            print("now in design mode")
            self.designmode = True
            self.sudoku = Sudoku(self.sudoku.start_num)
            self.draw_sudoku(new=True)
        else:
            print("already in design mode")

    def set_solve_mode(self):
        print("now in solve mode")
        self.designmode = False

    def mouse1press(self, event):
        self.btn1pressed = True
        self.line.append((event.x, event.y))

    def mouse1release(self, event):
        self.btn1pressed = False
        # set number of sampling points
        if not self.classifier.trained:
            print("train classifier first!")
        elif len (self.line) < 20:
            print("line to short")
        else:
            x = np.array(self.line, dtype=int)[np.linspace(0, len(self.line) - 1, num=self.classifier.get_npoints() // 2 , dtype=int)]
            # get field
            pos=np.mean(x, axis=0) // self.fieldSz
            pos=pos.astype(dtype='int')
            print("digit at {},{}".format(pos[0],pos[1]))
            # remove offset
            x=np.subtract(x,pos*self.fieldSz)
            # check: 90% of points in field: > 0 and < self.fieldSz
            within=np.sum(np.all(np.logical_and(x>0, x< self.fieldSz),axis=1))/len(x)
            if within < .9:
                print("draw the number within one field!!! {}% are outside {}, {}".format(within, pos[0],pos[1]))
            else:
                # crop points outside filed
                x.shape = self.classifier.get_npoints()
                x[x<0]=0
                x[x>self.fieldSz]=self.fieldSz
                guess = self.classifier.predict(x.reshape(1, -1))[0]
                if guess is None:
                    guess = 0
                print("recognized as {} at {},{}".format(guess, pos[0],pos[1]))
                if self.designmode:
                    self.sudoku.start_num[ pos[0],pos[1] ] = guess
                    self.restart()
                else:
                    if self.sudoku.start_num[ pos[0],pos[1]] != 0:
                        print("cannot change start number in solve mode")
                    else:
                        if self.sudoku.solved_num[ pos[0],pos[1]] != 0:
                            self.sudoku.reset_options()
                        self.sudoku.solved_num[ pos[0],pos[1]]=guess
                    self.sudoku.update_options()
        self.line=[]
        self.draw_sudoku(new=True)


    def mousemove(self, event):
        if self.btn1pressed:
            self.line.append((event.x, event.y))
            self.c.create_line(self.line[-2][0], self.line[-2][1], self.line[-1][0], self.line[-1][1])

    def save_current(self):
        # save the start number
        filename = tk.filedialog.asksaveasfilename(title = "Select file",filetypes = [("sudoku","*.sudoku")])
        if filename:
            print("saving sudoku to file:", filename)
            np.savetxt(filename, self.sudoku.start_num, fmt="%i", delimiter=',')


    def open_from_file(self):
        # read from file
        filename =  tk.filedialog.askopenfilename(title = "Select file",filetypes = [("sudoku","*.sudoku")])
        if filename:
            print("reading sudoku from file:", filename)
            try:
                num = np.genfromtxt(filename, dtype=int, delimiter=',')
                num.shape = (9,9) #check dimensions
            except IOError as err:
                print(str(err))
                self.new_sudoku(Sudoku.empty_sudoku)
            else:
                self.new_sudoku(num)



class SudokuAppMenu(tk.Menu):

    def __init__(self, master):
        # top menue (just for testing, not really populated)
        tk.Menu.__init__(self, master)

        puzzle_men = tk.Menu(self, tearoff=0)
        new_men = tk.Menu(self, tearoff=0)
        mode_men = tk.Menu(self, tearoff=0)

        for i in range(len(master.sudoku.sudoku_start_num)):
            new_men.add_command(label=Sudoku.sudoku_start_name[i],
                                # command=lambda: gui.new_sudoku(Sudoku.sudoku_start_num[i]) )
                                command=functools.partial(master.new_sudoku, Sudoku.sudoku_start_num[i]))
        mode_men.add_command(label="design", command=master.set_design_mode)
        mode_men.add_command(label="solve", command=master.set_solve_mode)

        puzzle_men.add_command(label="Open", command=master.open_from_file)
        puzzle_men.add_command(label="Save", command=master.save_current)
        # puzzle_men.add_command(label="check options", command=self.update_options)
        # puzzle_men.add_command(label="redraw", command=lambda: self.draw_sudoku(new=True))
        puzzle_men.add_command(label="Clear", command=master.restart)
        puzzle_men.add_cascade(label="New", menu=new_men)
        puzzle_men.add_cascade(label="Mode", menu=mode_men)
        puzzle_men.add_separator()
        puzzle_men.add_command(label="Exit", command=master.quit)
        self.add_cascade(label="Sudoku", menu=puzzle_men)

        master.config(menu=self)
        # not sure when i need to call this
        master.update_idletasks()


if __name__ == '__main__':
    SudokuApp().mainloop()
