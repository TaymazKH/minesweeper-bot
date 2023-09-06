import json

from telegram import InlineKeyboardButton, InlineKeyboardMarkup


def get_game_markup(table, visit, players, turn):
    height = len(table)
    width = len(table[0])
    keyboard = []
    for x in range(height):
        row = []
        for y in range(width):
            if visit[x][y] == -1:
                bt = '⬜'
            elif visit[x][y] == 0:
                bt = str(table[x][y])
                if bt == '0':
                    bt = ' '
            elif visit[x][y] == 1:
                bt = '🔴'
            else:
                bt = '🔵'
            row.append(InlineKeyboardButton(
                bt,
                callback_data=json.dumps(
                    {'operation': 'move', 'players': players, 'turn': 1, 'table': table, 'visit': visit, 'x': x,
                     'y': y})
            ))
        keyboard.append(row)
    return InlineKeyboardMarkup(keyboard)
