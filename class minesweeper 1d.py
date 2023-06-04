# one-dimensional array
from random import sample as ran_sample

class Cell:
    def __init__(self, around_mines=0, mine=False) -> None:
        self.around_mines = around_mines
        self.mine = mine
        self.fl_open = False

class GameField:
    def __init__(self, N, M) -> None:
        self.N = N
        self.M = M
        self.pole = [Cell() for _ in range(self.N) for __ in range(self.N)]
        self.init()
        
    def init(self):
        for i in ran_sample(self.pole, self.M):
            i.mine = True

        for i in range(self.N):
            for j in range(self.N):
                cell = self.pole[self.N * i + j]
                if cell.mine == True:
                    continue
                cell.around_mines = self.count(i, j)
    
    def count(self, i, j):
        result = 0
        for k in range(i-1, i+2):
            if 0 <= k < self.N:
                for m in range(j-1, j+2):
                    if 0 <= m < self.N:
                        if self.pole[self.N * k + m].mine == True:
                            result += 1
        return result

    def show(self):
        for i in range(self.N):
            for j in range(self.N):
                cell = self.pole[self.N * i + j]
                print('#' if cell.fl_open == False else cell.around_mines, end=' ')
            print()

    def show_all(self):
        "show 'pole' with mines and numbers"
        for i in range(self.N):
            for j in range(self.N):
                cell = self.pole[self.N * i + j]
                print(cell.around_mines if cell.mine == False else '*', end=' ')
            print()


pole_game = GameField(5, 4)
while True:
    pole_game.show()
    x, y = tuple(map(int, input('Enter row column: ')))
    cell = pole_game.pole[pole_game.N * x + y]
    if cell.mine:
        print('BOOM you loose')
        pole_game.show_all()
        break
    cell.fl_open = True
