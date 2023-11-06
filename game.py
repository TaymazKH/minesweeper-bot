from functions import generate_table


def generate_map(height: int, width: int, mines: int) -> tuple[list[list[int]], list[list[int]], int]:
    if width > 8 or width < 5 or height > 20 or height < 5 or width * height > 100 or width * height < mines or \
            mines < 7 or mines % 2 == 0:
        raise ValueError()
    table, iv = generate_table(height, width, mines, None)
    visit = [[0] * width for _ in range(height)]
    return table, visit, iv


def move(table: list[list[int]], visit: list[list[int]], x: int, y: int, turn: int) -> tuple[bool, bool, int]:
    height = len(table)
    width = len(table[0])
    if visit[x][y] == 0:
        if table[x][y] == 9:
            visit[x][y] = turn
            return has_won(table, visit, turn), True, turn
        else:
            dfs_visit(table, visit, height, width, x, y)
            turn = (turn % 2) + 1
            return False, True, turn
    return False, False, turn


def dfs_visit(table: list[list[int]], visit: list[list[int]], height: int, width: int, x: int, y: int) -> None:
    if visit[x][y] != 0:
        return
    visit[x][y] = 3
    if table[x][y] == 0:
        for i in range(max(x - 1, 0), min(x + 2, height)):
            for j in range(max(y - 1, 0), min(y + 2, width)):
                dfs_visit(table, visit, height, width, i, j)


def has_won(table: list[list[int]], visit: list[list[int]], turn: int) -> bool:
    height = len(table)
    width = len(table[0])
    mines = 0
    found = 0
    for i in range(height):
        for j in range(width):
            if table[i][j] == 9:
                mines += 1
                if visit[i][j] == turn:
                    found += 1
    return found > mines / 2
