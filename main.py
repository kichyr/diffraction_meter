import tkinter

class Application(tkinter.Frame):
    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        self.prev_x = -1 
        self.prev_y = -1
        self.grid()
        self.flag = 0
        self.create_widgets()
        self.dots = []
        self.draw_finished = 0

    def create_widgets(self):
        self.canvas = tkinter.Canvas(self, width=600, height=600)
        self.canvas.grid()
        self.canvas.bind('<B1-Motion>', self.draw)
        #self.canvas.bind('<Button-1>', self.change_flag)
        self.canvas.bind('<ButtonRelease-1>', self.change_flag)



    def change_flag(self, event):
        self.flag = (self.flag+1)%2

    def draw(self, event):
        if self.prev_x != -1 and self.flag == 0:
            self.canvas.create_oval(event.x-1, event.y-1, event.x+1, event.y+1)
            self.dots.append([event.x, event.y])
            #self.canvas.create_line(self.prev_x, self.prev_y, event.x, event.y, fill="#000", width=2)
        self.prev_x = event.x-1
        self.prev_y = event.y-1
        if self.flag != 0:
            self.flag = 0


if __name__ == "__main__":
    root = tkinter.Tk()
    root.title("diffraction meter")

    app = Application(root)
    button1 = tkinter.Button(root, text = "finish", command=root.destroy)
    button1.configure(width = 10, activebackground = "#33B5E5")
    button1_window = app.canvas.create_window(300, 20, window=button1)
    root.mainloop()
    print(app.dots)
        
