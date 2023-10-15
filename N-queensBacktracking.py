Q = 10
board = [[0 for x in range(Q)] for y in range(Q)]
def is_Safe(board, col, row):
    for x in range(col):
        if board[row][x] == 1:
            return False
    for x, y in zip(range(row, -1, -1), range(col, -1, -1)):
        if board[x][y] == 1:
            return False
    for x, y in zip(range(row, Q, 1), range(col, -1, -1)):
        if board[x][y] == 1:
            return False
    return True

def solveNQueens(board, col):
    if col == Q:
        for x in board:
            print(x)
        return True
    for i in range(Q):
        if is_Safe(board, col, i):
            board[i][col] = 1
            if solveNQueens(board, col + 1):
                return True
            board[i][col] = 0
    return False

if not solveNQueens(board, 0):
    print("No solution found")
