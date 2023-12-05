import numpy as np

from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

global GRID


def solvePuzzle(grid, x, y, R, C, row_con, col_con) -> list[list[int]]:
    solved, solved_grid = solvePic(grid, 0, 0, R, C, row_con, col_con)
    print(solved_grid)
    if solved:
        return solved_grid
    else:
        return []


def solvePic(grid, x, y, R, C, row_con, col_con):
    if y == R and is_Safe:
        return True, grid
    nextY = y
    if x == C - 1:
        nextX = 0
        nextY = y + 1
    else:
        nextX = x + 1
    grid[y][x] = 1
    if is_Safe(grid, x, y, R, C, row_con, col_con) and solvePic(grid, nextX, nextY, R, C, row_con, col_con)[0]:
        return True, grid
    grid[y][x] = 0
    if is_Safe(grid, x, y, R, C, row_con, col_con) and solvePic(grid, nextX, nextY, R, C, row_con, col_con)[0]:
        return True, grid
    return False, grid


def is_Safe(grid, x, y, R, C, row_con, col_con):
    currentRow = rowToRestriction(grid, y, C)
    currentCol = colToRestriction(grid, x, R)

    rowRestrict = row_con[y]
    colRestrict = col_con[x]
    if currentCol > colRestrict:
        return False
    if currentRow > rowRestrict:
        return False
    if x == C - 1 and currentRow != rowRestrict:
        return False
    if y == R - 1 and currentCol != colRestrict:
        return False
    return True


def rowToRestriction(grid, y, C):
    currentRow = [0]
    l = 0
    for i in range(C):
        if grid[y][i] != 0:
            currentRow[l] = currentRow[l] + grid[y][i]
        else:
            currentRow.append(0)
            l += 1
    currentRow = [i for i in currentRow if i != 0]
    return currentRow


def colToRestriction(grid, x, R):
    currentCol = [0]
    l = 0
    for i in range(R):
        if grid[i][x] != 0:
            currentCol[l] = currentCol[l] + grid[i][x]
        else:
            currentCol.append(0)
            l += 1
    currentCol = [i for i in currentCol if i != 0]
    return currentCol


"""
row_constraints = [[3],
                   [1, 1],
                   [1, 1],
                   [1],
                   [5],
                   [2, 2],
                   [5],
                   [5],
                   [3]]
col_constraints = [[2, 4],
                   [1, 5],
                   [1, 1, 3],
                   [1, 5],
                   [7]]
solution = solvePic(grid, 0, 0)
"""


@app.route("/solve", methods=["POST"])
def solve_nonogram():
    data = request.get_json()
    R = data.get("R")
    C = data.get("C")
    row_constraints = data.get("row")
    col_constraints = data.get("col")
    grid = [[0 for x in range(C)] for y in range(R)]

    solved_grid = solvePuzzle(grid, 0, 0, R, C, row_constraints, col_constraints)
    print(solved_grid)
    return jsonify({"solved_grid": solved_grid})


if __name__ == "__main__":
    app.run(debug=True)
