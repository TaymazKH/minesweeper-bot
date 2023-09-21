from telegram import InlineKeyboardButton, InlineKeyboardMarkup


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
        for i in row:
            game_state += i
    game_state += ' '
    for row in visit:
        for i in row:
            game_state += i
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
