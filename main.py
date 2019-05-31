import tkinter

def sign(x):
    if x > 0:
        return 1
    if x == 0:
        return 0
    else:
        return -1


class Application(tkinter.Frame):
    pixel_size = 600
    grid_step = 10
    grid_size = int(pixel_size/grid_step) + 2
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

    def draw(self, event):
        if self.prev_x != -1 and self.flag == 0:
            #self.canvas.create_oval(event.x-1, event.y-1, event.x+1, event.y+1)
            self.dots.append([event.x, event.y])
            self.canvas.create_line(self.prev_x, self.prev_y, event.x, event.y, fill="#000", width=2)
            x = self.prev_x
            y = self.prev_y
            it_x = Application.grid_step*sign(event.x-self.prev_x)
            it_y = Application.grid_step*sign(event.y-self.prev_y)
            while it_x*x < it_x*(event.x + (event.x-self.prev_x)) and it_y*y < it_y*(event.y + (event.y-self.prev_y)):
                self.Matrix[int(y/Application.grid_step)][int(x/Application.grid_step)] = 1
                self.Matrix[int((y+it_y)/Application.grid_step)][int((x+it_x)/Application.grid_step)] = 1
                break
                x += it_x
                y += it_y
            
        self.prev_x = event.x
        self.prev_y = event.y
        if self.flag != 0:
            self.flag = 0

        def color_cells(self, x_p, y_p, x, y) {
            k = (y - y_p)/(x - x_5)
            if abs(k) <= 1:
                x_start = min(x_p, x)
                x_end = max(x_p, x)
                it_x = sqrt(1/(sqrt(1+k^2))) * self.grid_step
                while x_start < x_end:
                    self.Matrix[((x_start - x)*k + y)/self.grid_step][x_start]
                    x_strat += it_x
                
        }


if __name__ == "__main__":
    root = tkinter.Tk()
    root.title("diffraction meter")

    app = Application(root)
    button1 = tkinter.Button(root, text = "finish", command=root.destroy)
    button1.configure(width = 10, activebackground = "#33B5E5")
    button1_window = app.canvas.create_window(300, 20, window=button1)
    root.mainloop()
    print(app.dots)
    for row in app.Matrix:
        for elem in row:
            print(elem, end=' ')
        print('\n')
    print(int(3/3))
 
        
