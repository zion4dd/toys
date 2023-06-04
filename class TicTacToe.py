# OOP
# Droid random

from random import randint

class Cell:
    def __init__(self, value=0):
        self.value = value
    
    def __bool__(self):
        return self.value == 0

    def __repr__(self) -> str:
        if self.value == 0:
            return '_'
        return 'X' if self.value == 1 else 'O'

class TicTacToe:
    FREE_CELL = 0      # свободная клетка
    HUMAN_X = 1        # крестик (игрок - человек)
    COMPUTER_O = 2     # нолик (игрок - компьютер)

    def __init__(self):
        self.pole = tuple(tuple(Cell() for _ in range(3)) for _ in range(3))
        self.__win = 0  # 1 - hum, 2 - comp, 3 - draw
    
    @staticmethod
    def __check_index(index):
        if type(index) != tuple or len(index) != 2:
            raise IndexError('некорректно указанные индексы')

        r, c = index
        if r not in range(3) or c not in range(3):
            raise IndexError('некорректно указанные индексы')

    def __check_win(self, r, c, value):
        row = all((x.value == value for x in self.pole[r]))  # проверяем строку на выигрыш
        col = all((x[c].value == value for x in self.pole))  # проверяем столбец на выигрыш
        diag1 = diag2 = False
        if r == c:  # если входит главная диагональ
            diag1 = all((self.pole[i][i].value == value for i in range(3)))
        if (r + c) == 2:  # если входит побочная диагональ
            diag2 = all((self.pole[i][-i+2].value == value for i in range(3)))

        if any((row, col, diag1, diag2)):
            if value == self.HUMAN_X:
                self.__win = 1
            else:
                self.__win = 2
            return
            
        # проверка на ничью
        if not any((x.value == self.FREE_CELL for row in self.pole for x in row)):
            self.__win = 3

    def __getitem__(self, item):
        r, c = item
        return self.pole[r][c].value

    def __setitem__(self, key, value):
        r, c = key
        self.pole[r][c].value = value
        self.__check_win(r, c, value)

    def init(self):
        self.__win = 0  # 1 - hum, 2 - comp, 3 - draw
        for row in self.pole:
            for i in row:
                i.value = self.FREE_CELL
    
    def show(self):
        for row in self.pole:
            for i in row:
                print(str(i), end=' ')
            print()
        print()
    
    def human_go(self):
        index = tuple(map(int, input('введите координаты без пробела: ')))
        self.__check_index(index)
        r, c = index
        if self[r, c] == self.FREE_CELL:
            self[r, c] = self.HUMAN_X
        else:
            print('клетка занята')
            self.human_go()

    def computer_go(self):
        r, c = randint(0, 2), randint(0, 2)
        if self[r, c] == self.FREE_CELL:
            self[r, c] = self.COMPUTER_O
        else:
            self.computer_go()
    
    @property
    def is_human_win(self):  # True, если победил человек
        return self.__win == 1

    @property
    def is_computer_win(self):  # True, если победил комп
        return self.__win == 2

    @property
    def is_draw(self):  # True, если ничья
        return self.__win == 3
    
    def __bool__(self):  # возвращает True, если игра не окончена
        return not any((self.is_human_win, self.is_computer_win, self.is_draw))


game = TicTacToe()
game.init()
step_game = 0
while game:
    game.show()

    if step_game % 2 == 0:
        game.human_go()
    else:
        game.computer_go()

    step_game += 1


game.show()

if game.is_human_win:
    print("Поздравляем! Вы победили!")
elif game.is_computer_win:
    print("Все получится, со временем")
else:
    print("Ничья.")

