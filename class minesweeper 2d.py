# two-dimensional array
from random import sample

class Cell:
    def __init__(self, around_mines=0, mine=False) -> None:
        self.around_mines = around_mines
        self.mine = mine
        self.fl_open = False

class GameField:
    def __init__(self, N, M) -> None:
        self.N = N
        self.M = M
        self.pole = [[Cell() for _ in range(self.N)] for __ in range(self.N)]
        self.init()
        
    def init(self):
        for indx in sample(range(self.N**2), self.M):  # random.sample
            i, j = divmod(indx, self.N)  # divmod -> (a//b, a%b)
            self.pole[i][j].mine = True

        for i in range(self.N):
            for j in range(self.N):
                if self.pole[i][j].mine == True:
                    continue
                self.pole[i][j].around_mines = self.count(i, j)
    
    def count(self, i, j):
        result = 0
        for k in range(i-1, i+2):
            if 0 <= k < self.N:
                for m in range(j-1, j+2):
                    if 0 <= m < self.N:
                        if self.pole[k][m].mine == True:
                            result += 1
        return result

    def show(self):
        for i in range(self.N):
            for j in range(self.N):
                cell = self.pole[i][j]
                print('#' if cell.fl_open == False else cell.around_mines, end=' ')
            print()

    def show_all(self):
        "show 'pole' with mines and numbers"
        for i in range(self.N):
            for j in range(self.N):
                cell = self.pole[i][j]
                print(cell.around_mines if cell.mine == False else '*', end=' ')
            print()


pole_game = GameField(5, 4)
# pole_game.show_all() # TEST
while True:
    pole_game.show()
    x, y = tuple(map(int, input('Enter row column: ')))
    cell = pole_game.pole[x][y]
    if cell.mine:
        print('BOOM you lose!')
        pole_game.show_all()
        break
    cell.fl_open = True



# Для того чтобы посчитать кол-во мин в соседних полях совсем не обязательно обходить все клетки поля. 
# Вместо этого можно обходить поля с минами и добавлять по единичке в соседние с ней поля!
#
#     def init(self):
#         for idx in rnd.sample(range(self.size ** 2), self.num_mines):
#             i, j = divmod(idx, self.size)
#             self.pole[i][j].mine = True
#
#             for di, dj in itertools.product((-1, 0, 1), repeat=2):
#                 if all(0 <= coord < self.size for coord in (i + di, j + dj)):
#                     self.pole[i + di][j + dj].around_mines += 1