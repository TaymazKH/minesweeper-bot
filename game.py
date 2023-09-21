from random import sample


def generate_map(height: int, width: int, mines: int) -> tuple[list[list[int]], list[list[int]]]:
    if width > 8 or height > 11 or width * height > 100 or width * height < mines or mines % 2 == 0:
        raise ValueError()
    table = []
    visit = []
    choices = []
    for i in range(height):
        table.append([0] * width)
        visit.append([0] * width)
        for j in range(width):
            choices.append((i, j))
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
    return table, visit


def move(table: list[list[int]], visit: list[list[int]], x: int, y: int, turn: int) -> tuple[bool, int]:
    height = len(table)
    width = len(table[0])
    if visit[x][y] == 0:
        if table[x][y] == 9:
            visit[x][y] = turn
        else:
            dfs_visit(table, visit, height, width, x, y)
            turn = (turn % 2) + 1
        return True, turn
    return False, turn


def dfs_visit(table: list[list[int]], visit: list[list[int]], height: int, width: int, x: int, y: int) -> None:
    if visit[x][y] != 0:
        return
    visit[x][y] = 3
    if table[x][y] == 0:
        for i in range(max(x - 1, 0), min(x + 2, height)):
            for j in range(max(y - 1, 0), min(y + 2, width)):
                dfs_visit(table, visit, height, width, i, j)
