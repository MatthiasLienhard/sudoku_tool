import tkinter as tk
import numpy as np
import sklearn.neighbors


class DigitClassifier(sklearn.neighbors.KNeighborsClassifier):
    def __init__(self, filename='digits.csv', k=5):
        # read filename
        sklearn.neighbors.KNeighborsClassifier.__init__(self, n_neighbors=k, weights="uniform")
        self.filename=filename
        (self.train_numbers, self.train_data) = self.read_traindata()
        # train_data=[[x1,y1,x2,y2,...],...]
        self.trained = False

        if (self.get_ndata() > 20):
            # X=copy.deepcopy(self.train_data)
            # X=X.reshape((self.get_ndata(), 2*self.get_npoints()))
            self.fit(self.train_data, self.train_numbers)
            self.trained = True
        else:
            print("not enough data points: {}".format(self.get_ndata()))

    def read_traindata(self):
        try:
            data = np.genfromtxt(self.filename, dtype=int, delimiter=',')
        except IOError as err:
            print(str(err))
            return [], [[]]
        else:
            numbers = data[..., :1].reshape(data.shape[0])
            lines = data[..., 1:data.shape[1]]
            # lines=lines.reshape((lines.shape[0], lines.shape[1]//2, 2))
            return numbers, lines

    def get_traindata(self):
        return self.train_numbers, self.train_data

    # def predict(self, X):
    #    #X.shape=( 2*self.get_npoints())
    #    print("prediction")
    #    sklearn.neighbors.KNeighborsClassifier(self,X)

    def get_ndata(self):
        return len(self.train_numbers)

    def get_npoints(self):
        if self.get_ndata() > 0:
            return len(self.train_data[0] // 2)

    def add_train_data(self, new_numbers, new_data):
        # add new data and retrain classifier
        if self.get_ndata() > 0:
            # todo: check dimensions
            self.train_data = np.concatenate((self.train_data, new_data))
            self.train_numbers = np.concatenate((self.train_numbers, new_numbers))
        else:
            self.train_data = new_data
            self.train_numbers = new_numbers

        if (self.get_ndata() > 20):
            # X=copy.deepcopy(self.train_data)
            # X.reshape((self.get_ndata(), 2*self.get_npoints()))
            self.fit(self.train_data, self.train_numbers)
            self.trained = True
        else:
            print("not enough data points: {}".format(self.get_ndata()))


class TrainDigits(tk.Tk):
    def __init__(self, filename="digits.csv", n=3, npoints=20):
        tk.Tk.__init__(self)
        # todo: if filename exists, make classifier and check input?, append input
        self.line = []
        self.classifier = DigitClassifier(filename, k=5)
        self.geometry("500x300+500+200")
        self.train_data = np.zeros((n * 10, npoints * 2))
        self.train_numbers = np.repeat([range(10)], n, axis=0).reshape(n * 10)
        self.title("Now draw a " + str(self.train_numbers[0]))
        self.filename = filename
        self.n = n
        self.npoints = npoints
        self.i = 0  # number of learned data
        self.added_i = 0  # learned data added to classifier
        self.protocol("WM_DELETE_WINDOW", self.on_exit)
        self.learn_cv = tk.Canvas(self, width=100, height=100)
        self.learn_cv.configure(background="white")
        self.learn_cv.pack()
        self.tested = 0
        self.correct = 0

        self.btn1pressed = False
        self.learn_cv.bind("<Motion>", self.mousemove)
        self.learn_cv.bind("<ButtonPress-1>", self.mouse1press)
        self.learn_cv.bind("<ButtonRelease-1>", self.mouse1release)

        self.bt_retrain = tk.Button(self, text="train classifier",
                                    command=self.retrain)
        self.bt_retrain.pack()
        self.bt_undo = tk.Button(self, text="remove last",
                                 command=self.undo)
        self.bt_undo.pack()

    def undo(self):
        # remove last learned datum
        if (self.i > 0 and self.i > self.added_i):
            self.i -= 1
            print("now draw a " + str(self.train_numbers[self.i]))
            self.title("now draw a " + str(self.train_numbers[self.i]))

        else:
            print("cannot remove digit that has already been used for training")

    def retrain(self):
        # retrain classifer

        if self.i > self.added_i:
            # numbers, data = self.classifier.get_traindata()
            # numbers=np.concatenate((numbers,self.train_numbers[self.added_i:self.i]))
            # data=np.concatenate((data,self.train_data[self.added_i:self.i]))
            # self.classifier.add_train_data(numbers, data)
            self.classifier.add_train_data(self.train_numbers[self.added_i:self.i],
                                           self.train_data[self.added_i:self.i])
            print("now there are " + str(self.classifier.get_ndata()) + " data points used for training")
        else:
            print("no new data points for training")
        self.added_i = self.i

    def on_exit(self):
        print("Training is over now...")
        if self.tested > 0:
            print("correctly classified {}/{} datapoints ({:.2f}%)".format(self.correct, self.tested,
                                                                           self.correct / self.tested * 100))
        self.write_traindata()
        self.destroy()

    def write_traindata(self):
        self.retrain()
        numbers, data = self.classifier.get_traindata()
        out = np.concatenate((numbers.reshape((len(numbers), 1)), data), axis=1)
        # data.reshape((self.n*10, self.npoints*2))), axis=1)
        np.savetxt(self.filename, out, fmt="%i", delimiter=',')

    def get_traindata(self):
        return (self.train_numbers, self.train_data)

    def mouse1press(self, event):
        self.btn1pressed = True
        self.line.append((event.x, event.y))

    def clear_canvas(self):
        self.learn_cv.delete("all")

    def mouse1release(self, event):
        self.btn1pressed = False
        # set number of sampling points
        x = np.array(self.line, dtype=int)[np.linspace(0, len(self.line) - 1, num=self.npoints, dtype=int)]
        x.shape = 2 * self.npoints
        self.train_data[self.i] = x
        if self.classifier.trained:
            self.tested += 1
            guess = self.classifier.predict(x.reshape(1, -1))[0]

            if guess == self.train_numbers[self.i]:
                print("recognized as " + str(guess))
                self.correct += 1
            else:
                print("missclassified as " + str(guess))

        else:
            print("classifier not trained yet")
        self.clear_canvas()
        self.line=[]
        for i in range(2,len(x),2):
            self.learn_cv.create_line(x[i-2], x[i-1], x[i], x[i+1])
        self.after( 200, self.clear_canvas )

        self.i += 1

        if self.i == len(self.train_numbers):
            self.on_exit()
        else:
            print("now draw a " + str(self.train_numbers[self.i]))
            self.title("now draw a " + str(self.train_numbers[self.i]))

    def mousemove(self, event):
        if self.btn1pressed:
            self.line.append((event.x, event.y))
            self.learn_cv.create_line(self.line[-2][0], self.line[-2][1], self.line[-1][0], self.line[-1][1])


if __name__ == '__main__':
    TrainDigits().mainloop()
