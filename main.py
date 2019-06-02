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
    grid_step = 10
    grid_size = int(pixel_size/grid_step)+2
    color_grid_size = 60
    color_grid_step = int(pixel_size/color_grid_size)

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
        self.color_matrix = [[0 for x in range(Application.color_grid_size)] for y in range(Application.color_grid_size)] # Матрица интенсивностей
        #--------------------------------
        self.L = 10**5 # расстояние до линзы+экран mkm - микрометров
        self.pixel_len = 10 # mkm - длина одного пикселя
        self.Lambda = 500*10**(-1) # длина волны микрометры

    def create_widgets(self):
        self.canvas = tkinter.Canvas(self, width=Application.pixel_size, height=Application.pixel_size)
        self.canvas.grid()
        self.canvas.bind('<B1-Motion>', self.draw)
        #self.canvas.bind('<Button-1>', self.change_flag)
        self.canvas.bind('<ButtonRelease-1>', self.change_flag)
    #--------------------------phys-part-------------------------
    def summing_tension(self, s_x, s_y, s_z, default_E):
        E = 0
        for i in range(Application.grid_size):
            for j in range(Application.grid_size):
                if self.Matrix[i][j] != 0:
                    x_c = (j * Application.grid_step + Application.grid_step/2) * self.pixel_len
                    y_c = (i * Application.grid_step + Application.grid_step/2) * self.pixel_len
                    E += default_E * math.cos((x_c*s_x + y_c*s_y) * 2 * math.pi/self.Lambda)
        return E**2


    def calc_intensity(self):
        #для каждой точки экрана
        for i in range(Application.color_grid_size):
            for j in range(Application.color_grid_size):
                s_x = (Application.color_grid_step * j - int(Application.pixel_size/2)) * self.pixel_len
                s_y = (Application.color_grid_step * i - int(Application.pixel_size/2))* self.pixel_len 
                s_z = self.L
                ro = math.sqrt(s_x**2 + s_y**2 + s_z**2)
                s_x /= ro
                s_y /= ro
                s_z /= ro
                alpha = math.pi*self.pixel_len*Application.grid_step*s_x/self.Lambda
                beta = math.pi*self.pixel_len*Application.grid_step*s_y/self.Lambda

                if alpha == 0:
                    a_s = 0
                else:
                    a_s = math.sin(alpha)/alpha

                if beta == 0:
                    b_s = 0
                else:
                    b_s = math.sin(beta)/beta

                default_E = (self.pixel_len*Application.grid_step)**2*a_s*b_s
                #print(s_x, s_y, s_z)
                self.color_matrix[i][j] = self.summing_tension(s_x, s_y, s_z, default_E)

        
    #------------------------------------------------------------
    def change_flag(self, event):
        self.flag = (self.flag+1)%2


    def stop_drawing(self):
        self.canvas.bind("<B1-Motion>", lambda e: None)
        self.color_int()
        self.calc_intensity()
        self.display_diff_picture()

    
    def display_diff_picture(self):
        max = -999999
        min = 999999
        for i in range(Application.color_grid_size):
            for j in range(Application.color_grid_size):
                if max < self.color_matrix[i][j]:
                    max = self.color_matrix[i][j]
                if min > self.color_matrix[i][j]:
                    min = self.color_matrix[i][j]

        """ for row in self.color_matrix:
            for elem in row:
                print(elem, end=' ')
            print('\n') """
        print(max, min)

        for i in range(Application.color_grid_size):
            for j in range(Application.color_grid_size):
                self.color_matrix[i][j] = int(self.color_matrix[i][j]/(max-min) * 255)

        


        step = Application.pixel_size/Application.color_grid_size
        for i in range(Application.color_grid_size):
            for j in range(Application.color_grid_size):
                colorval = "#%02x%02x%02x" % (self.color_matrix[i][j], self.color_matrix[i][j], self.color_matrix[i][j])
                self.canvas.create_rectangle(i*step, j*step, i*step+step, j*step+step, fill=colorval,  outline="")
        

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

    def color_int(self):
        for i in range(Application.grid_size):
            state = 0
            first_zero = -1
            first_one = -1
            j = 0
            first_one_locked = 0
            while j < Application.grid_size:
                if self.Matrix[i][j] == 1:
                    if self.Matrix[i][j+1] == 1:
                        if first_one_locked == 0:
                            first_one = j
                            first_one_locked = 1
                        if self.Matrix[i][j+2] == 0:
                            if (((self.Matrix[i+1][first_one] == 1) or (self.Matrix[i+1][first_one - 1] == 1)) and 
                            ((self.Matrix[i-1][j+1] == 1) or (self.Matrix[i-1][j+2] == 1))) or (((self.Matrix[i-1][first_one] == 1) or (self.Matrix[i-1][first_one - 1] == 1)) and 
                            ((self.Matrix[i+1][j+1] == 1) or (self.Matrix[i+1][j+2] == 1))):
                                if state == 0:
                                    state = 1
                                    first_zero = j + 2
                                    j = j + 2
                                    first_one = -1
                                    first_one_locked = 0
                                    continue
                                else:
                                    for k in range(first_zero, first_one):
                                        self.Matrix[i][k] = 2
                                    first_zero = -1
                                    state = 0
                                    j =  j + 2
                                    first_one = -1
                                    first_one_locked = 0
                                    continue
                            elif state == 0:
                                j = j + 2
                                first_one = -1
                                first_one_locked = 0
                                continue
                            else:
                                for k in range(first_zero, first_one):
                                    self.Matrix[i][k] = 2
                                first_zero = j + 2
                                j = j + 2
                                first_one = -1
                                first_one_locked = 0
                                continue
                        j += 1
                        continue
                    if (self.Matrix[i][j + 1] == 0) and (state == 0):
                        first_zero = j + 1
                        state = 1

                    elif (first_zero >= 0) and (state == 1):
                        for k in range(first_zero, j):
                            self.Matrix[i][k] = 2
                        first_zero = -1
                        state = 0
                j += 1

        


if __name__ == "__main__":
    root = tkinter.Tk()
    root.title("diffraction meter")

    app = Application(root)
    button1 = tkinter.Button(root, text = "finish", command=app.stop_drawing)
    button1.configure(width = 10, activebackground = "#33B5E5")
    button1_window = app.canvas.create_window(300, 20, window=button1)
    root.mainloop()
    #print(app.dots)
        
