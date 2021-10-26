import numpy as np
import random


class sudoku():

    def __init__(self):
        self.filled_grid = np.full((9, 9), -1)
        self.possible_grid = np.empty((9, 9,), dtype=object)
        self.numbers_by_order=[]
        for i, v in enumerate(self.possible_grid):
            for j, u in enumerate(self.possible_grid[i]): self.possible_grid[i][j] = [1, 2, 3, 4, 5, 6, 7, 8, 9]
        self.possible_by_numbers = np.empty((9,), dtype=object)
        for i, v in enumerate(self.possible_by_numbers): self.possible_by_numbers[i] = []
        for i in range(81):
            self.possible_by_numbers[8].append([1 + i % 9, 1 + int(i / 9)])

    def fill_sudoku(self, last_reversion,increase_reversion):
        succes = False
        for i in range(9):
            if len(self.possible_by_numbers[i]) > 0:
                if self.check_if_all_filled(i):
                    new_number_cords = self.possible_by_numbers[i][
                        random.randrange(0, len(self.possible_by_numbers[i]))]
                    while self.filled_grid[new_number_cords[0] - 1][new_number_cords[1] - 1] != -1:
                        new_number_cords = self.possible_by_numbers[i][
                            random.randrange(0, len(self.possible_by_numbers[i]))]
                    new_numer = self.possible_grid[new_number_cords[0] - 1][new_number_cords[1] - 1][
                        random.randrange(0, i + 1)]
                    succes = self.fill_number(new_number_cords, new_numer)
                    break
        if succes==1:
            if (self.check_if_done()):
                return
            self.fill_sudoku(last_reversion,increase_reversion)
            return
        else:
            temp=0
            while(len(self.possible_grid[succes[0]-1][succes[1]-1])<2):
                temp+=1
                self.revert_number()
            if temp==last_reversion:
                increase_reversion+=1
                for i in range(increase_reversion):
                    self.revert_number()
            self.fill_sudoku(temp,increase_reversion)
            return

    #funkcja odwraca ostatnią wpisaną liczbe i uzupełnia pola, które były przez nią nadpisane
    def revert_number(self):
        new_number_cords=self.numbers_by_order[-1]
        new_numer=self.filled_grid[new_number_cords[0]-1][new_number_cords[1]-1]
        self.numbers_by_order.pop()
        self.filled_grid[new_number_cords[0] - 1, new_number_cords[1] - 1] = -1
        for i in range(9):
            self.revrite_possible_number([i + 1, new_number_cords[1]], new_numer)
            self.revrite_possible_number([new_number_cords[0], i + 1], new_numer)
        for i in range(3 * int((new_number_cords[0] - 1) / 3), 3 * (int((new_number_cords[0] - 1) / 3) + 1)):
            for j in range(3 * int((new_number_cords[1] - 1) / 3), 3 * (int((new_number_cords[1] - 1) / 3) + 1)):
                self.revrite_possible_number([i + 1, j + 1], new_numer)

    #funkcja która sprawdza czy dana liczba może być wpisana w danym polu
    def revrite_possible_number(self, number_cords, new_numer):
        if self.possible_grid[number_cords[0] - 1][number_cords[1] - 1].__contains__(new_numer):
            return
        for i in range(9):
            if self.filled_grid[i, number_cords[1] - 1] == (new_numer):
                return
            if self.filled_grid[number_cords[0] - 1, i] == (new_numer):
                return
        for i in range(3 * int((number_cords[0] - 1) / 3), 3 * (int((number_cords[0] - 1) / 3) + 1)):
            for j in range(3 * int((number_cords[1] - 1) / 3), 3 * (int((number_cords[1] - 1) / 3) + 1)):
                if self.filled_grid[i, j] == (new_numer):
                    return
        self.possible_grid[number_cords[0] - 1][number_cords[1] - 1].append(new_numer)
        if len(self.possible_grid[number_cords[0] - 1][number_cords[1] - 1]) > 1:
            self.possible_by_numbers[len(self.possible_grid[number_cords[0] - 1][number_cords[1] - 1]) - 2].remove(
                number_cords)
        self.possible_by_numbers[len(self.possible_grid[number_cords[0] - 1][number_cords[1] - 1]) - 1].append(
            number_cords)
        return

    #funkcja sprawdza czy w polach o danej ilości możliwych liczb do ich wypełnienia istnieje jedno
    #puste pole
    def check_if_all_filled(self, i):
        for cords in self.possible_by_numbers[i]:
            if self.filled_grid[cords[0] - 1][cords[1] - 1] == -1:
                return True
        return False

    #funkcja która sprawdza czy sudoku zostało zapełnione
    def check_if_done(self):
        for i in range(9):
            for j in range(9):
                if self.filled_grid[i][j] == -1:
                    return False
        return True

    def fill_number(self, new_number_cords, new_numer):
        #zmienna która określa czy podczas ustalania nowych wartości zaszła taka zmiana, że niemożliwym
        #jest wpisanie wartości w dane pole, przyjmuje ona wtedy wartość równom kordynatom danego pola
        # informuje ona o konieczności wrócenia do wcześniejszych stanów programu
        revert = 1
        # dodanie nowej liczby
        self.numbers_by_order.append(new_number_cords)
        self.filled_grid[new_number_cords[0] - 1][new_number_cords[1] - 1] = new_numer
        # ustalenie nowych wartości w kwadracie 3x3
        for i in range(3 * int((new_number_cords[0] - 1) / 3), 3 * (int((new_number_cords[0] - 1) / 3) + 1)):
            for j in range(3 * int((new_number_cords[1] - 1) / 3), 3 * (int((new_number_cords[1] - 1) / 3) + 1)):
                if i != new_number_cords[0] - 1 and j != new_number_cords[1] - 1:
                    if self.possible_grid[i][j].__contains__(new_numer):
                        self.possible_by_numbers[len(self.possible_grid[i][j]) - 1].remove([i + 1, j + 1])
                        if len(self.possible_grid[i][j]) > 0:
                            self.possible_by_numbers[len(self.possible_grid[i][j]) - 2].append([i + 1, j + 1])
                        self.possible_grid[i][j].remove(new_numer)

                        if self.filled_grid[i][j] == -1 and len(self.possible_grid[i][j]) <= 0:
                            revert = [i+1,j+1]

        for i in range(9):
            #ustalenie nowych wartości w danej kolumnie
            if self.possible_grid[new_number_cords[0] - 1][i].__contains__(new_numer):
                self.possible_by_numbers[len(self.possible_grid[new_number_cords[0] - 1][i]) - 1].remove(
                    [new_number_cords[0], i + 1])
                if len(self.possible_grid[new_number_cords[0] - 1][i]) > 0:
                    self.possible_by_numbers[len(self.possible_grid[new_number_cords[0] - 1][i]) - 2].append(
                        [new_number_cords[0], i + 1])
                self.possible_grid[new_number_cords[0] - 1][i].remove(new_numer)
                if self.filled_grid[new_number_cords[0] - 1][i] == -1 and len(
                        self.possible_grid[new_number_cords[0] - 1][i]) <= 0:
                    revert = [new_number_cords[0] ,i+1]
            #ustalenie nowych wartości w danym rzędzie
            if i != new_number_cords[0] - 1:
                if self.possible_grid[i][new_number_cords[1] - 1].__contains__(new_numer):
                    self.possible_by_numbers[len(self.possible_grid[i][new_number_cords[1] - 1]) - 1].remove(
                        [i + 1, new_number_cords[1]])
                    if len(self.possible_grid[i][new_number_cords[1] - 1]) > 0:
                        self.possible_by_numbers[len(self.possible_grid[i][new_number_cords[1] - 1]) - 2].append(
                            [i + 1, new_number_cords[1]])
                    self.possible_grid[i][new_number_cords[1] - 1].remove(new_numer)
                    if self.filled_grid[i][new_number_cords[1] - 1] == -1 and len(
                            self.possible_grid[i][new_number_cords[1] - 1]) <= 0:
                        revert = [i+1,new_number_cords[1] ]
        return revert


s = sudoku()

s.fill_sudoku(0,0)
print(s.filled_grid)
