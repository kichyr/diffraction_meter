import tkinter
import threading
import math
import time
from concurrent.futures import ThreadPoolExecutor

class Application(tkinter.Frame):
    pixel_size = 600 # Размер сетки(в координатах)
    grid_step = 8 # Размер квадрата сетки
    grid_size = int(pixel_size/grid_step) # Размер сетки(в квадратах)

    color_grid_step = 5 # Размер квадрата матрицы интенсивностей
    color_grid_size = int(pixel_size/color_grid_step) # Размер матрицы интенсивностей

    def __init__(self, master):
        tkinter.Frame.__init__(self, master)
        self.end_threads_counter = 0
        self.prev_x = -1
        self.prev_y = -1
        self.grid()
        self.flag = 0
        self.create_widgets()
        self.dots = [] # Точки контура
        self.matrix = [[0 for x in range(Application.grid_size)]
                       for y in range(Application.grid_size)] # Сетка
        self.color_matrix = [[0 for x in range(Application.color_grid_size)]
                             for y in range(Application.color_grid_size)] # Матрица интенсивностей
        self.n_initial_phases = 6 # Количество начальных фаз при поиске амплитуды
        self.l_0 = 5*10**5 # Расстояние до линзы, микрометры
        self.pixel_len = 5 # Размер пикселя, микрометры
        self.lambda_wave = 500*10**(-3) # Длина волны, микрометры


    def create_widgets(self):
        self.canvas = tkinter.Canvas(self, width=Application.pixel_size,
                                     height=Application.pixel_size)
        self.canvas.grid()
        self.canvas.bind('<B1-Motion>', self.draw)
        self.canvas.bind('<ButtonRelease-1>', self.change_flag)

    #--------------------------Физическая часть-------------------------
    # Вычисление суммы волн от всех квадратов сетки по направлению (s_x, s_y, s_z)
    # Приблизительное нахождение амплитуды волны посредством сдвига фазы и взятия максимального значения E
    def summing_tension(self, s_x, s_y, default_e, i_pos, j_pos):
        initial_phases = []
        e_phased = []
        for i in range(self.n_initial_phases):
            e_phased.append(0)
            initial_phases.append(i*2*math.pi/self.n_initial_phases)
        for i in range(Application.grid_size):
            for j in range(Application.grid_size):
                if self.matrix[i][j] != 0:
                    x_c = (j*Application.grid_step - Application.pixel_size/2)*self.pixel_len
                    y_c = (i*Application.grid_step - Application.pixel_size/2)*self.pixel_len
                    for k in range(self.n_initial_phases):
                        e_phased[k] += default_e * math.cos(initial_phases[k] + (x_c*s_x + y_c*s_y)
                                                            *2*math.pi/self.lambda_wave)
        for i in range(self.n_initial_phases):
            e_phased[i] = abs(e_phased[i])
        self.color_matrix[j_pos][i_pos] = max(e_phased)
        self.end_threads_counter += 1


    # Вычисление всей матрицы интенсивностей    
    def calc_intensity(self):
        pool = ThreadPoolExecutor(40)
        for i in range(Application.color_grid_size):
            for j in range(Application.color_grid_size):
                s_x = (Application.color_grid_step*j - Application.pixel_size/2)*self.pixel_len
                s_y = (Application.color_grid_step*i - Application.pixel_size/2)*self.pixel_len
                s_z = self.l_0
                r_0 = math.sqrt(s_x**2 + s_y**2 + s_z**2)
                s_x /= r_0
                s_y /= r_0
                s_z /= r_0
                alpha = math.pi*self.pixel_len*s_x/self.lambda_wave
                beta = math.pi*self.pixel_len*s_y/self.lambda_wave

                if alpha == 0:
                    a_s = 1
                else:
                    a_s = math.sin(alpha)/alpha

                if beta == 0:
                    b_s = 1
                else:
                    b_s = math.sin(beta)/beta

                # Волна от одного квадрата в направлении (s_x, s_y, s_z)
                default_e = ((self.pixel_len*Application.grid_step)**2)*a_s*b_s

                pool.submit(self.summing_tension, s_x, s_y, default_e, Application.color_grid_size - j - 1, i)
        #Ждем завершения вычислений
        while self.end_threads_counter != Application.color_grid_size ** 2:
            time.sleep(0.1)

        self.display_diff_picture()
        
            
        

    def change_flag(self, event):
        self.flag = (self.flag + 1)%2


    def stop_drawing(self):
        self.canvas.bind("<B1-Motion>", lambda e: None)
        self.color_int()
        #запускаем поток вычислений
        t = threading.Thread(target=self.calc_intensity(), args=())
        t.start()

        


    # Рисовалка матрицы интенсивностей
    def display_diff_picture(self):
        max_value = -999999
        min_value = 999999
        for i in range(Application.color_grid_size):
            for j in range(Application.color_grid_size):
                if max_value < self.color_matrix[i][j]:
                    max_value = self.color_matrix[i][j]
                if min_value > self.color_matrix[i][j]:
                    min_value = self.color_matrix[i][j]

        for i in range(Application.color_grid_size):
            for j in range(Application.color_grid_size):
                self.color_matrix[i][j] = int((self.color_matrix[i][j]/(max_value - min_value)) * 255)


        step = Application.pixel_size/Application.color_grid_size
        for i in range(Application.color_grid_size):
            for j in range(Application.color_grid_size):
                colorval = "#%02x%02x%02x" % (self.color_matrix[i][j],
                                              self.color_matrix[i][j], self.color_matrix[i][j])

                self.canvas.create_rectangle(i*step, j*step, i*step+step, j*step+step,
                                             fill=colorval, outline="")


    # Обведение полученных точек в сплошной контур
    def color_cells(self, x_p, y_p, x_n, y_n):
        if x_n - x_p != 0:
            k = (y_n - y_p)/(x_n - x_p)
            if abs(k) <= 1:
                x_start = min(x_p, x_n)
                x_end = max(x_p, x_n)
                it_x = math.sqrt(1/(math.sqrt(1 + k**2))) * self.grid_step
                while x_start < x_end:
                    self.matrix[int(((x_start - x_n)*k + y_n)/self.grid_step)][int(x_start/self.grid_step)] = 1
                    x_start += it_x

        if y_n - y_p != 0:
            k = (x_n - x_p)/(y_n - y_p)
            y_start = min(y_p, y_n)
            y_end = max(y_p, y_n)
            it_y = math.sqrt(1/(math.sqrt(1+k**2)))*self.grid_step
            while y_start < y_end:
                self.matrix[int(y_start/self.grid_step)][int(((y_start - y_n)*k + x_n)/self.grid_step)] = 1
                y_start += it_y


    def draw(self, event):
        if self.prev_x != -1 and self.flag == 0:
            self.dots.append([event.x, event.y])
            self.canvas.create_line(self.prev_x, self.prev_y, event.x, event.y, fill="#000", width=2)
            self.color_cells(self.prev_x, self.prev_y, event.x, event.y)
        self.prev_x = event.x
        self.prev_y = event.y

        if self.flag != 0:
            self.flag = 0


    # Определение внутренности контура
    def color_int(self):
        for i in range(Application.grid_size):
            state = 0
            first_zero = -1
            first_one = -1
            j = 0
            first_one_locked = 0
            while j < Application.grid_size:
                if self.matrix[i][j] == 1:
                    if self.matrix[i][j + 1] == 1:
                        if first_one_locked == 0:
                            first_one = j
                            first_one_locked = 1
                        if self.matrix[i][j + 2] == 0:
                            if (((self.matrix[i + 1][first_one] == 1) or (self.matrix[i + 1][first_one - 1] == 1)) and
                                 ((self.matrix[i - 1][j + 1] == 1) or (self.matrix[i - 1][j + 2] == 1))) or (((self.matrix[i - 1][first_one] == 1) or
                                   (self.matrix[i - 1][first_one - 1] == 1)) and 
                                   ((self.matrix[i + 1][j + 1] == 1) or (self.matrix[i + 1][j + 2] == 1))):
                                if state == 0:
                                    state = 1
                                    first_zero = j + 2
                                    j = j + 2
                                    first_one = -1
                                    first_one_locked = 0
                                    continue
                                else:
                                    for k in range(first_zero, first_one):
                                        self.matrix[i][k] = 2
                                    first_zero = -1
                                    state = 0
                                    j = j + 2
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
                                    self.matrix[i][k] = 2
                                first_zero = j + 2
                                j = j + 2
                                first_one = -1
                                first_one_locked = 0
                                continue
                        j += 1
                        continue
                    if (self.matrix[i][j + 1] == 0) and (state == 0):
                        first_zero = j + 1
                        state = 1

                    elif (first_zero >= 0) and (state == 1):
                        for k in range(first_zero, j):
                            self.matrix[i][k] = 2
                        first_zero = -1
                        state = 0
                j += 1


if __name__ == "__main__":
    ROOT = tkinter.Tk()
    ROOT.title("diffraction meter")

    APP = Application(ROOT)
    BUTTON_1 = tkinter.Button(ROOT, text="finish", command=APP.stop_drawing)
    BUTTON_1.configure(width=10, activebackground="#33B5E5")
    BUTTON_1_WINDOW = APP.canvas.create_window(300, 20, window=BUTTON_1)
    ROOT.mainloop()