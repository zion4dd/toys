# Procedural programming
# Droid with iq

import random
from colorama import init
from colorama import Fore  # 14 строка

init()

def new_game():
    global FIELD
    input('press "ENTER" to START')
    color = random.choice(['CYAN', 'BLUE', 'RED', 'MAGENTA', 'YELLOW'])
    exec(f'print(Fore.{color})')
    print('NEW GAME!............."q" for exit')
    FIELD = [['_'] * 3 for _ in range(3)]
    if random.random() > 0.5:
        show()
        while True:
            human()
            droid()
    else:
        while True:
            droid()
            human()

def show():
    print('B'.rjust(5))
    print(' ', *FIELD[0])
    print('A', *FIELD[1])
    print(' ', *FIELD[2])

def human():
    while True:
        inp = input('A - row, B - column. input "AB": ')
        if inp == 'q':
            exit()
        if len(inp) == 2:
            if inp[0] in '123' and inp[1] in '123':
                x = int(inp[0])-1
                y = int(inp[1])-1
                if FIELD[x][y] == '_':
                    FIELD[x][y] = 'X'
                    check()
                    break

def droid():
    def iq(xo):
        d1 = d2 = '' # diagonals
        for i in range(3):
            row_ch = column_ch = ''
            for j in range(3):
                if i == j:
                    d1 += FIELD[i][j]
                if i + j == 2:
                    d2 += FIELD[i][j]
                row_ch += FIELD[i][j]
                column_ch += FIELD[j][i]
                if row_ch.count(xo) == 2:
                    if row_ch.find('_') != -1:
                        FIELD[i][row_ch.find('_')] = 'O'
                        show()
                        check()
                        return True
                if column_ch.count(xo) == 2:
                    if column_ch.find('_') != -1:
                        FIELD[column_ch.find('_')][i] = 'O'
                        show()
                        check()
                        return True
            if d1.count(xo) == 2:
                if d1.find('_') != -1:
                    FIELD[d1.find('_')][d1.find('_')] = 'O'
                    show()
                    check()
                    return True
            if d2.count(xo) == 2:
                if d2.find('_') != -1:
                    FIELD[d2.find('_')][2 - d2.find('_')] = 'O'
                    show()
                    check()
                    return True

    if FIELD[1][1] == '_':
        FIELD[1][1] = 'O'
        show()
        check()
        return
    if iq('O') or iq('X'):  # поиск двух О или Х
        return
    while True:  # если 3 условия не выполнены, то ход рандомно
        x = random.randint(0, 2)
        y = random.randint(0, 2)
        if FIELD[x][y] == '_':
            FIELD[x][y] = 'O'
            show()
            check()
            break

def check():
    def ch_xo(xo):
        def ch(n):
            return n == xo
        
        row0 = all(map(ch, FIELD[0]))
        row1 = all(map(ch, FIELD[1]))
        row2 = all(map(ch, FIELD[2]))
        col0 = all(map(ch, list(zip(*FIELD))[0]))
        col1 = all(map(ch, list(zip(*FIELD))[1]))
        col2 = all(map(ch, list(zip(*FIELD))[2]))
        dg0 = all(map(ch, sum(FIELD, [])[::4]))
        dg1 = all(map(ch, sum(FIELD, [])[2:7:2]))
        if any([row0, row1, row2, col0, col1, col2, dg0, dg1]):
            return True

    if ch_xo('X'):
        show()
        print('you win! congratulations!\n')
        new_game()
    if ch_xo('O'):
        print('you lose! ha-ha-ha!\n')
        new_game()
    if '_' not in FIELD[0] + FIELD[1] + FIELD[2]:  # проверка на ничью
        print('draw!\n')
        new_game()


if __name__ == "__main__":
    new_game()

