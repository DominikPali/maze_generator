import customtkinter as ctk
import random
import time

class App(ctk.CTk):
    def __init__(self, n):
        super().__init__()
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
        self.title("Maze Generator")
        self.geometry("750x750")
        self.n = n
        self.borders = {}
        self.border_squares = {}
        self.squares = [[200, 200, 200, 200, 200, 200, 200, 200, 200, 200] for _ in range(10)]
        self.central_squares = {}
        self.visted_squares_n = 0
        self.current_square_nr = 1
        self.create_board()

    def create_board(self):
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
                            square = ctk.CTkLabel(frame, fg_color="white", width=20, height=20, text="", text_color='black')
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
                elif j == 9:
                    self.borders[ji][1] = -3
                if i == 0:
                    self.borders[ji][0] = -3
                elif i == 9:
                    self.borders[ji][2] = -3
        self.button = ctk.CTkButton(self, text="test  maze genrator", command=lambda: self.create_maze("73"), font=('Arial', 7), width=30)
        self.button.grid(row=self.n+2, column=0)


    def create_maze(self, starting_square):
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
                self.central_squares[starting_square].configure(fg_color='white')
                self.central_squares[starting_square].update()
                starting_square = self.change_color_of_square(starting_square, border_nr)
                self.central_squares[starting_square].configure(fg_color='white')
                self.central_squares[starting_square].update()
                self.squares[int(starting_square[0])][int(starting_square[1])] = self.current_square_nr
                self.current_square_nr += 1
            self.visted_squares_n += 1

    def change_color_of_square(self, square, border_nr):
            border_nr = self.get_random_border(square)
            self.border_squares[square][border_nr].configure(fg_color="white", text_color="black")
            self.border_squares[square][border_nr].update()
            if border_nr == 0:
                self.border_squares[square[0] + str(int(square[1]) - 1)][2].configure(fg_color="white", text_color="black")
                return square[0]+str(int(square[1]) - 1)
            elif border_nr == 1:
                self.border_squares[str(int(square[0]) + 1) + square[1]][3].configure(fg_color="white", text_color="black")
                return str(int(square[0]) + 1) + square[1]
            elif border_nr == 2:
                self.border_squares[square[0] + str(int(square[1]) + 1)][0].configure(fg_color="white", text_color="black")
                return square[0] + str(int(square[1]) + 1)
            elif border_nr == 3:
                self.border_squares[str(int(square[0]) - 1) + square[1]][1].configure(fg_color="white", text_color="black")
                return str(int(square[0]) - 1)+square[1]
            
    def get_random_border(self, square):
        possible_borders = []
        for i in range(4):
            if self.borders[square][i] != -3:
                try:
                    if i == 0:
                        if self.squares[int(square[0])][int(square[1]) - 1] != 200 or self.border_squares[square][i].cget("fg_color") == "white":
                            continue
                except IndexError:
                    pass
                try:
                    if i == 1:
                        if self.squares[int(square[0]) + 1][int(square[1])] != 200 or self.border_squares[square][i].cget("fg_color") == "white":
                            continue
                except IndexError:
                    pass
                try:
                    if i == 2:
                        if self.squares[int(square[0])][int(square[1]) + 1] != 200 or self.border_squares[square][i].cget("fg_color") == "white":
                            continue
                except IndexError:
                    pass
                try:
                    if i == 3:
                        if self.squares[int(square[0]) - 1][int(square[1])] != 200 or self.border_squares[square][i].cget("fg_color") == "white":
                            continue
                except IndexError:
                    pass
                possible_borders.append(i)
        if len(possible_borders) > 0:
            return random.choice(possible_borders)
        else:
            return -1

if __name__ == '__main__':
    app = App(10)
    app.mainloop()