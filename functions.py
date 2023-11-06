from random import seed, randint, sample
from threading import Lock

from baseconv import BaseConverter
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

base64 = BaseConverter('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz._')
lock = Lock()


def get_game_markup(table: list[list[int]], visit: list[list[int]], players: tuple[int, int], turn: int):
    height = len(table)
    width = len(table[0])
    keyboard = []
    for x in range(height):
        row = []
        for y in range(width):
            if visit[x][y] == 0:
                bt = '⬜'
            elif visit[x][y] == 3:
                bt = str(table[x][y])
                if bt == '0':
                    bt = ' '
            elif visit[x][y] == 1:
                bt = '🔴'
            else:
                bt = '🔵'
            row.append(InlineKeyboardButton(bt, callback_data=f'm {x} {y}'))
        keyboard.append(row)
    game_state = f'{turn} {players[0]} {players[1]} {len(table)} {len(table[0])} '
    for row in table:
        for cell in row:
            game_state += str(cell)
    game_state += ' '
    for row in visit:
        for cell in row:
            game_state += str(cell)
    row = []
    while game_state:
        row.append(InlineKeyboardButton('-', callback_data=game_state[:64]))
        game_state = game_state[64:]
    keyboard.append(row)
    return InlineKeyboardMarkup(keyboard)


def get_game_state(markup: InlineKeyboardMarkup):
    button_row = markup.to_dict()['inline_keyboard'][-1]
    s = ''
    for button in button_row:
        s += button['callback_data']
    li = s.split()
    height = int(li[3])
    width = int(li[4])
    table_str = li[5]
    visit_str = li[6]
    table = []
    visit = []
    for x in range(height):
        table.append(list(table_str[x * width:(x + 1) * width]))
        visit.append(list(visit_str[x * width:(x + 1) * width]))
    return {'turn': int(li[0]), 'players': (int(li[1]), int(li[2])), 'table': table, 'visit': visit}


def generate_table(height: int, width: int, mines: int, iv: int | None) -> tuple[list[list[int]], int]:
    table = []
    choices = []
    for i in range(height):
        table.append([0] * width)
        for j in range(width):
            choices.append((i, j))
    with lock:
        if iv is None:
            seed()
            iv = randint(0, 0x7FFFFFFF)
        seed(iv)
        choices = sample(choices, mines)
    for cell in choices:
        x = cell[0]
        y = cell[1]
        if table[x][y] != 9:
            table[x][y] = 9
            for i in range(max(x - 1, 0), min(x + 2, height)):
                for j in range(max(y - 1, 0), min(y + 1, width)):
                    if table[i][j] != 9:
                        table[i][j] += 1
    return table, iv


# 9    9    1             1   1     1      6     34
# id1  id2  turn & signs  xy  size  mines  seed  visit

def extract_user_ids(query: str) -> tuple[int, int]:
    str1 = query[:9]
    str2 = query[9:18]
    signs = int(query[18])
    id1 = int(base64.decode(str1))
    id2 = int(base64.decode(str2))
    if signs % 4 > 1:
        id1 *= -1
    if signs % 2 == 1:
        id2 *= -1
    return id1, id2


def extract_turn(query: str) -> int:
    return 1 if int(query[18]) < 5 else 2


def extract_table_size(query: str) -> tuple[int, int]:
    size = int(base64.decode(query[20]))
    width = (size // 16) + 5
    height = (size % 16) + 5
    return width, height


def extract_xy(query: str) -> tuple[int, int]:
    size = int(base64.decode(query[19]))
    x = (size % 16) + 5
    y = (size // 16) + 5
    return x, y


def extract_table(query: str) -> list[list[int]]:
    mines = int(base64.decode(query[21]))
    iv = int(base64.decode(query[22:28]))
    width, height = extract_table_size(query)
    table, iv = generate_table(height, width, mines, iv)
    return table


def extract_visit(query: str) -> list[list[int]]:
    pass
