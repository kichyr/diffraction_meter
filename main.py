import tkinter
import math

def sign(x):
    if x > 0:
        return 1
    if x == 0:
        return 0
    else:
        return -1


class Application(tkinter.Frame):
    pixel_size = 600
    grid_step = 50
    grid_size = int(pixel_size/grid_step)+1
    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        self.prev_x = -1 
        self.prev_y = -1
        self.grid()
        self.flag = 0
        self.create_widgets()
        self.dots = []
        self.draw_finished = 0
        self.Matrix = [[0 for x in range(Application.grid_size)] for y in range(Application.grid_size)] 

    def create_widgets(self):
        self.canvas = tkinter.Canvas(self, width=Application.pixel_size, height=Application.pixel_size)
        self.canvas.grid()
        self.canvas.bind('<B1-Motion>', self.draw)
        #self.canvas.bind('<Button-1>', self.change_flag)
        self.canvas.bind('<ButtonRelease-1>', self.change_flag)



    def change_flag(self, event):
        self.flag = (self.flag+1)%2


    def color_cells(self, x_p, y_p, x, y):
        if x - x_p != 0:
            k = (y - y_p)/(x - x_p)
            if abs(k) <= 1:
                x_start = min(x_p, x)
                x_end = max(x_p, x)
                it_x = math.sqrt(1/(math.sqrt(1+k**2))) * self.grid_step
                while x_start < x_end:
                    self.Matrix[int(((x_start - x)*k + y)/self.grid_step)][int(x_start/self.grid_step)] = 1
                    x_start += it_x
                return
        
        if y - y_p != 0:
            k = (x - x_p)/(y - y_p)
            y_start = min(y_p, y)
            y_end = max(y_p, y)
            it_y = math.sqrt(1/(math.sqrt(1+k**2))) * self.grid_step
            while y_start < y_end:
                self.Matrix[int(y_start/self.grid_step)][int(((y_start - y)*k + x)/self.grid_step)] = 1
                y_start += it_y
        return
                
        

    def draw(self, event):
        if self.prev_x != -1 and self.flag == 0:
            #self.canvas.create_oval(event.x-1, event.y-1, event.x+1, event.y+1)
            self.dots.append([event.x, event.y])
            self.canvas.create_line(self.prev_x, self.prev_y, event.x, event.y, fill="#000", width=2)
            self.color_cells(self.prev_x, self.prev_y, event.x, event.y)
            
        self.prev_x = event.x
        self.prev_y = event.y
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
    #print(app.dots)
    for row in app.Matrix:
        for elem in row:
            print(elem, end=' ')
        print('\n')
 
        
