import json

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_game_markup(table, visit, players, turn):
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
            row.append(InlineKeyboardButton(bt, callback_data=f'1 {x} {y}'))
        keyboard.append(row)
    game_state = json.dumps({'players': players, 'turn': 1, 'table': table, 'visit': visit})
    row = []
    while game_state:
        row.append(InlineKeyboardButton('-', callback_data=game_state[:64]))
        game_state = game_state[64:]
    keyboard.append(row)
    return InlineKeyboardMarkup(keyboard)


def get_game_state(markup: InlineKeyboardMarkup):
    row = markup.to_dict()['inline_keyboard'][-1]
    s = ''
    for button in row:
        s += button['callback_data']
    return json.loads(s)
