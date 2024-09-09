import customtkinter as ctk
import random
import time
class App(ctk.CTk):
    def __init__(self, n, enter):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.title("Maze Generator")
        self.geometry("950x950")
        self.n = n
        self.power_n = pow(n, 2)
        self.borders = {}
        self.border_squares = {}
        self.squares = [[self.power_n, self.power_n, self.power_n, self.power_n, self.power_n, self.power_n, self.power_n, self.power_n, self.power_n, self.power_n,] for _ in range(10)]
        self.central_squares = {}
        self.visted_squares_n = 0
        self.current_square_nr = 1
        self.starting_square = enter
        self.create_board(self.starting_square)
        self.beginning = None
        self.end = None
        self.beginning_bn = None
        self.end_bn = None
        self.seen_squares = []

    def create_board(self, enter):
        global selected_option
        global selected_option_solve
        self.grid_columnconfigure(0, weight=0)
        self.info_label = ctk.CTkLabel(self, text="Click the button to see the algorithm generate maze", font=("Arial", 16))
        self.info_label.grid(row=0, column=0, columnspan=self.n, pady=10)

        for i in range(self.n):
            for j in range(self.n):
                ji = str(j)+str(i)
                frame = ctk.CTkFrame(self, width=60, height=60, fg_color="transparent")  # Outer frame for borders
                frame.grid_propagate(False)  # Prevent frame from resizing to fit children
                frame.grid(row=i+1, column=j, padx=2, pady=2)
                self.border_squares[ji] = [None, None, None, None]
                self.borders[ji] = [1, 1, 1, 1]
                for l in range(3):
                    for k in range(3):
                        kl = str(k)+str(l)
                        if l == 1 and k == 1:
                            square = ctk.CTkLabel(frame, fg_color="white", width=20, height=20, text=ji, text_color='black')
                            square.grid(row=l, column=k)
                        else:
                            square = ctk.CTkLabel(frame, fg_color="black", width=20, height=20, text="")
                            square.grid(row=l, column=k)
                        
                        if kl == "10":
                            self.border_squares[ji][0] = square
                        elif kl == "21":
                            self.border_squares[ji][1] = square
                        elif kl == "12":
                            self.border_squares[ji][2] = square
                        elif kl == "01":
                            self.border_squares[ji][3] = square 
                        elif kl == "11":
                            self.central_squares[ji] = square              
                
                if j == 0:
                    self.borders[ji][3] = -3
                elif j == self.n - 1:
                    self.borders[ji][1] = -3
                if i == 0:
                    self.borders[ji][0] = -3
                elif i == self.n -1:
                    self.borders[ji][2] = -3
        self.buttons = ctk.CTkFrame(self)
        self.buttons.grid(column=0, row=self.n+2, columnspan=self.n, rowspan=2)
        self.button = ctk.CTkButton(self.buttons, text="test maze genrator", command=lambda: self.create_maze(enter), font=('Arial', 20), width=30)
        self.button.grid(row=0, column=0)
        selected_option = ctk.StringVar(value="Example Algorithm")
        self.a_options = ctk.CTkOptionMenu(self.buttons, values=["Example Algorithm", "Prim's Alogorithm"], font=('Arial', 20), width=30, variable=selected_option)
        self.a_options.grid(row=0, column=1)
        self.resetB = ctk.CTkButton(self.buttons, text="reset", command=lambda: self.reset(), font=('Arial', 20), width=30)
        self.resetB.grid(row=0, column=2)
        self.end_and_beggining = ctk.CTkButton(self.buttons, text="end / beggining", command=lambda: self.create_start_and_ending_point(), font=('Arial', 20), width=30)
        self.end_and_beggining.grid(row=0, column=3)

        self.solve_maze_button = ctk.CTkButton(self.buttons, text="Solve Maze", command=lambda: self.solve_maze(), font=('Arial', 20), width=30)
        self.solve_maze_button.grid(row=1, column=0)
        selected_option_solve = ctk.StringVar(value="A")
        self.solve_options = ctk.CTkOptionMenu(self.buttons, values=["A", "B"], font=('Arial', 20), width=30, variable=selected_option_solve)
        self.solve_options.grid(row=1, column=1)

    def reset(self):
        for i in range(self.n):
            for j in range(self.n):
                ji = str(j)+str(i)
                for x in range(len(self.border_squares[ji])):
                    self.border_squares[ji][x].configure(fg_color="black")
                    self.central_squares[ji].configure(fg_color="white")
        self.squares = [[self.power_n, self.power_n, self.power_n, self.power_n, self.power_n, self.power_n, self.power_n, self.power_n, self.power_n, self.power_n,] for _ in range(10)]
        self.visted_squares_n = 0
        self.beginning = None
        self.end = None
        self.beginning_bn = None
        self.end_bn = None
        self.current_square_nr = 1
        self.seen_squares = []

    def create_maze(self, starting_square):
        global selected_option
        if selected_option.get() == "Example Algorithm":
            self.squares[int(starting_square[0])][int(starting_square[1])] = 0
            while True:
                border_nr = self.get_random_border(starting_square)
                if border_nr == -1  and self.visted_squares_n != pow(self.n, 2):
                    try:
                        if self.squares[int(starting_square[0]) + 1][int(starting_square[1])] == self.squares[int(starting_square[0])][int(starting_square[1])] - 1:
                            starting_square = str(int(starting_square[0]) + 1) + starting_square[1]
                            self.current_square_nr = self.current_square_nr - 1
                            continue
                    except IndexError:
                        pass
                    try:
                        if self.squares[int(starting_square[0]) - 1][int(starting_square[1])] == self.squares[int(starting_square[0])][int(starting_square[1])] - 1:
                            starting_square = str(int(starting_square[0]) - 1) + starting_square[1]
                            self.current_square_nr = self.current_square_nr - 1
                            continue
                    except IndexError:
                        pass
                    try:
                        if self.squares[int(starting_square[0])][int(starting_square[1]) + 1] == self.squares[int(starting_square[0])][int(starting_square[1])] - 1:
                            starting_square = starting_square[0] + str(int(starting_square[1]) + 1)
                            self.current_square_nr = self.current_square_nr - 1
                            continue
                    except IndexError:
                        pass
                    try:
                        if self.squares[int(starting_square[0])][int(starting_square[1]) - 1] == self.squares[int(starting_square[0])][int(starting_square[1])] - 1:
                            starting_square = starting_square[0] + str(int(starting_square[1]) - 1)
                            self.current_square_nr = self.current_square_nr - 1
                            continue
                    except IndexError:
                        pass
                elif self.visted_squares_n == pow(self.n, 2):
                    break
                else:
                    starting_square = self.change_color_of_square(starting_square, border_nr, "white")
                    self.squares[int(starting_square[0])][int(starting_square[1])] = self.current_square_nr
                    self.current_square_nr += 1
                self.visted_squares_n += 1
        elif selected_option.get() == "Prim's Alogorithm":
            visited = [starting_square]
            while True:
                if self.visted_squares_n == pow(self.n, 2) or visited == []:
                    break
                random_square = random.choice(visited)
                border_nr = self.get_random_border(random_square)
                if border_nr == -1:
                    visited.remove(random_square)
                    continue
                else:
                    self.squares[int(starting_square[0])][int(starting_square[1])] = -1
                    starting_square = self.change_color_of_square(random_square, border_nr, "white")
                    self.squares[int(starting_square[0])][int(starting_square[1])] = -1
                    self.visted_squares_n += 1
                    visited.append(starting_square)

    def change_color_of_square(self, square, border_nr, color):
            border_nr = self.get_random_border(square)
            self.border_squares[square][border_nr].configure(fg_color=color, text_color="black")
            self.border_squares[square][border_nr].update()
            if border_nr == 0:
                self.border_squares[square[0] + str(int(square[1]) - 1)][2].configure(fg_color=color, text_color="black")
                self.border_squares[square[0] + str(int(square[1]) - 1)][2].update()
                return square[0]+str(int(square[1]) - 1)
            elif border_nr == 1:
                self.border_squares[str(int(square[0]) + 1) + square[1]][3].configure(fg_color=color, text_color="black")
                self.border_squares[str(int(square[0]) + 1) + square[1]][3].update()
                return str(int(square[0]) + 1) + square[1]
            elif border_nr == 2:
                self.border_squares[square[0] + str(int(square[1]) + 1)][0].configure(fg_color=color, text_color="black")
                self.border_squares[square[0] + str(int(square[1]) + 1)][0].update()
                return square[0] + str(int(square[1]) + 1)
            elif border_nr == 3:
                self.border_squares[str(int(square[0]) - 1) + square[1]][1].configure(fg_color=color, text_color="black")
                self.border_squares[str(int(square[0]) - 1) + square[1]][1].update()
                return str(int(square[0]) - 1)+square[1]
            
    def get_random_border(self, square):
        possible_borders = []
        for i in range(4):
            if self.borders[square][i] != -3:
                try:
                    if i == 0:
                        if self.squares[int(square[0])][int(square[1]) - 1] != self.power_n or self.border_squares[square][i].cget("fg_color") == "white":
                            continue
                        elif self.squares[int(square[0])][int(square[1]) - 1] == -1:
                            continue
                except IndexError:
                    pass
                try:
                    if i == 1:
                        if self.squares[int(square[0]) + 1][int(square[1])] != self.power_n or self.border_squares[square][i].cget("fg_color") == "white":
                            continue
                        elif self.squares[int(square[0]) + 1][int(square[1])] == -1:
                            continue
                except IndexError:
                    pass
                try:
                    if i == 2:
                        if self.squares[int(square[0])][int(square[1]) + 1] != self.power_n or self.border_squares[square][i].cget("fg_color") == "white":
                            continue
                        elif self.squares[int(square[0])][int(square[1]) + 1] == -1:
                            continue
                except IndexError:
                    pass
                try:
                    if i == 3:
                        if self.squares[int(square[0]) - 1][int(square[1])] != self.power_n or self.border_squares[square][i].cget("fg_color") == "white":
                            continue
                        elif self.squares[int(square[0]) - 1][int(square[1])] == -1:
                            continue
                except IndexError:
                    pass
                possible_borders.append(i)
        if len(possible_borders) > 0:
            return random.choice(possible_borders)
        else:
            return -1
    def create_start_and_ending_point(self):
        possible_end_or_beggining = []
        for i in range(self.n):
            sqrs = []
            sqrs.append("0" + str(i))
            sqrs.append(str(self.n - 1) + str(i))
            sqrs.append(str(i) + "0")
            sqrs.append(str(i) + str(self.n - 1))
            for square in sqrs:
                n_white_borders = 0
                for bn in range(4):
                    if self.border_squares[square][bn].cget("fg_color") == "white":
                        n_white_borders += 1
                if n_white_borders == 1 and square not in possible_end_or_beggining:
                    possible_end_or_beggining.append(square)
        if len(possible_end_or_beggining) < 2:
            self.reset()
            self.create_maze(self.starting_square)
            self.create_start_and_ending_point()
        else:
            beginning = random.choice(possible_end_or_beggining)
            possible_end_or_beggining.remove(beginning)
            end = random.choice(possible_end_or_beggining)
            self.central_squares[beginning].configure(fg_color="#ffdb8c")
            self.central_squares[end].configure(fg_color="#8bff4d")
            self.beginning = beginning
            self.end = end

            if beginning[0] == "0":
                self.border_squares[beginning][3].configure(fg_color="white")
                self.beginning_bn = 3
            elif beginning[0] == str(self.n - 1):
                self.border_squares[beginning][1].configure(fg_color="white")
                self.beginning_bn = 1
            elif beginning[1] == "0":
                self.border_squares[beginning][0].configure(fg_color="white")
                self.beginning_bn = 0
            elif beginning[1] == str(self.n - 1):
                self.border_squares[beginning][2].configure(fg_color="white")
                self.beginning_bn = 2
            
            if end[0] == "0":
                self.border_squares[end][3].configure(fg_color="white")
                self.end_bn = 3
            elif end[0] == str(self.n - 1):
                self.border_squares[end][1].configure(fg_color="white")
                self.end_bn = 1
            elif end[1] == "0":
                self.border_squares[end][0].configure(fg_color="white")
                self.end_bn = 0
            elif end[1] == str(self.n - 1):
                self.border_squares[end][2].configure(fg_color="white")
                self.end_bn = 2
    def solve_maze(self):
        global selected_option_solve
        if selected_option_solve.get() == "A":
            squares_to_explore = [self.beginning]
            while True:
                br = False
                list_of_sqaures = squares_to_explore
                for square in list_of_sqaures:
                    self.central_squares[square].configure(fg_color="#7a7a7a")
                    self.central_squares[square].update()
                    if 
                    

                    if square == self.end:
                        self.central_squares[square].configure(fg_color="#8bff4d")
                        self.central_squares[square].update()
                        time.sleep(0.5)
                        self.central_squares[square].configure(fg_color="white")
                        self.central_squares[square].update()
                        time.sleep(0.5)
                        self.central_squares[square].configure(fg_color="#8bff4d")
                        self.central_squares[square].update()
                        time.sleep(0.5)
                        self.central_squares[square].configure(fg_color="#00ff22")
                        self.central_squares[square].update()
                        br = True
                        break



                    for bn in range(4):
                        if self.border_squares[square][bn].cget("fg_color") == "white":
                            if bn == 0:
                                if square == self.end and self.end_bn == 0:
                                    pass
                                elif square == self.beginning and self.beginning_bn == 0:
                                    pass
                                elif square not in self.seen_squares:
                                    squares_to_explore.append(square[0] + str(int(square[1]) - 1))
                            elif bn == 1:
                                if square == self.end and self.end_bn == 1:
                                    pass
                                elif square == self.beginning and self.beginning_bn == 1:
                                    pass
                                elif square not in self.seen_squares:
                                    squares_to_explore.append(str(int(square[0]) + 1) + square[1])
                            elif bn == 2:
                                if square == self.end and self.end_bn == 2:
                                    pass
                                elif square == self.beginning and self.beginning_bn == 2:
                                    pass
                                elif square not in self.seen_squares:
                                    squares_to_explore.append(square[0] + str(int(square[1]) + 1))
                            elif bn == 3:
                                if square == self.end and self.end_bn == 3:
                                    pass
                                elif square == self.beginning and self.beginning_bn == 3:
                                    pass
                                elif square not in self.seen_squares:
                                    squares_to_explore.append(str(int(square[0]) - 1) + square[1])
                    self.seen_squares.append(square)
                    squares_to_explore.remove(square)
                if br:
                    break
                
        elif selected_option_solve.get() == "B":
            pass


if __name__ == '__main__':
    app = App(10, "44")
    app.mainloop()