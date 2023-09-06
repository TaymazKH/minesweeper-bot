from random import sample


def generate_map(height: int = 8, width: int = 8, mines: int = 21) -> tuple[list[list[int]], list[list[int]]]:
    if width > 8 or width * height > 100 or width * height < mines or mines % 2 == 0:
        raise ValueError()
    table = []
    visit = []
    choices = []
    for i in range(height):
        table.append([0] * width)
        visit.append([-1] * width)
        for j in range(width):
            choices.append((i, j))
    choices = sample(choices, mines)
    for cell in choices:
        x = cell[0]
        y = cell[1]
        if table[x][y] != -1:
            table[x][y] = -1
            for i in range(max(x - 1, 0), min(x + 2, height)):
                for j in range(max(y - 1, 0), min(y + 1, width)):
                    if table[i][j] != -1:
                        table[i][j] += 1
    return table, visit


def move(table: list[list[int]], visit: list[list[int]], x: int, y: int, turn: int):
    height = len(table)
    width = len(table[0])
    if visit[x][y] == -1:
        if table[x][y] == -1:
            visit[x][y] = turn
        else:
            dfs_visit(table, visit, height, width, x, y)
            turn = (turn % 2) + 1


def dfs_visit(table: list[list[int]], visit: list[list[int]], height: int, width: int, x: int, y: int) -> None:
    if visit[x][y] != -1:
        return
    visit[x][y] = 0
    if table[x][y] == 0:
        for i in range(max(x - 1, 0), min(x + 2, height)):
            for j in range(max(y - 1, 0), min(y + 1, width)):
                dfs_visit(table, visit, height, width, i, j)
