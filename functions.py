from random import seed, randint, sample
from threading import Lock

from baseconv import base2, BaseConverter
from telegram import InlineKeyboardButton, InlineKeyboardMarkup

base64 = BaseConverter('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz._')
lock = Lock()


def get_game_markup(table: list[list[int]], visit: list[list[int]], players: tuple[int, int], turn: int, iv: int):
    height = len(table)
    width = len(table[0])
    str1, str2 = encode_game_state(table, visit, players, turn, iv)
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
            row.append(InlineKeyboardButton(bt, callback_data=str1 + base64.encode(16 * (y - 5) + (x - 5)) + str2))
        keyboard.append(row)
    return InlineKeyboardMarkup(keyboard)


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

def encode_game_state(table: list[list[int]], visit: list[list[int]], players: tuple[int, int], turn: int, iv: int):
    height = len(table)
    width = len(table[0])
    mines = 0
    for row in table:
        for e in row:
            if e == 9:
                mines += 1
    sign = 0
    if players[0] < 0:
        sign += 2
    if players[1] < 0:
        sign += 1
    if turn == 2:
        sign += 4
    str1 = base64.encode(abs(players[0])) + base64.encode(abs(players[1])) + str(sign)
    iv_str = base64.encode(iv)
    iv_str = ('0' * (6 - len(iv_str))) + iv_str
    visit_str = ''
    d = {0: '00', 1: '01', 2: '10', 3: '11'}
    for row in visit:
        for e in row:
            visit_str += d[e]
    str2 = base64.encode(16 * (width - 5) + (height - 5)) + base64.encode(mines) + iv_str + \
           base64.encode(base2.decode(visit_str))
    return str1, str2


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
    cords = int(base64.decode(query[19]))
    x = (cords % 16) + 5
    y = (cords // 16) + 5
    return x, y


def extract_table(query: str) -> tuple[list[list[int]], int]:
    mines = int(base64.decode(query[21]))
    iv = int(base64.decode(query[22:28]))
    width, height = extract_table_size(query)
    table, iv = generate_table(height, width, mines, iv)
    return table, iv


def extract_visit(query: str) -> list[list[int]]:
    width, height = extract_table_size(query)
    visit_str = base2.encode(base64.decode(query[28:62]))
    visit_str = ('0' * (width * height * 2 - len(visit_str))) + visit_str
    visit = []
    d = {'00': 0, '01': 1, '10': 2, '11': 3}
    for i in range(height):
        row = []
        for j in range(width):
            row.append(d[visit_str[(width * i + j) * 2:(width * i + j) * 2 + 1]])
        visit.append(row)
    return visit
