import tkinter

class Application(tkinter.Frame):
    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        self.prev_x = -1 
        self.prev_y = -1
        self.grid()
        self.flag = 0
        self.create_widgets()

    def create_widgets(self):
        self.canvas = tkinter.Canvas(root, width=600, height=600)
        self.canvas.grid()
        self.canvas.bind('<B1-Motion>', self.draw)
        #self.canvas.bind('<Button-1>', self.change_flag)
        self.canvas.bind('<ButtonRelease-1>', self.change_flag)


    def change_flag(self, event):
        self.flag = (self.flag+1)%2

    def draw(self, event):
        if self.prev_x != -1 and self.flag == 0:
            self.canvas.create_oval(event.x-1, event.y-1, event.x+1, event.y+1)
            #self.canvas.create_line(self.prev_x, self.prev_y, event.x, event.y, fill="#000", width=2)
        self.prev_x = event.x-1
        self.prev_y = event.y-1
        if self.flag != 0:
            self.flag = 0

if __name__ == "__main__":
    root = tkinter.Tk()
    root.title("diffraction meter")
    
    app = Application(root)
    root.mainloop()