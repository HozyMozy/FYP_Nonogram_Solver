from flask import Flask, request, jsonify
from flask_cors import CORS
app = Flask(__name__)
CORS(app)

global GRID


def preprocessGrid(grid, row_constraints: list[list], col_constraints: list[list]):
    R, C = len(grid), len(grid[0])

    for y in range(R):
        con = row_constraints[y]
        if con[0] > C // 2 and len(con) == 1:
            start = max(0, C - con[0])
            end = min(C, con[0])
            for i in range(start, end):
                grid[y][i] = 2
        if len(con) > 1 and (con[0] > C - (sum(con) + len(con) - 1)):
            for a in range(len(con) - 1):
                startList = con[0:a + 1:1]
                startSum = sum(startList) + len(startList) - 1
                endList = con[-1:(-len(con)) + a - 1:-1]
                endSum = sum(endList) + len(endList) - 1
                if startSum > C - endSum:
                    start = C - endSum
                    end = startSum
                    for i in range(start, end):
                        grid[y][i] = 2
        for i in range(C):
            if grid[y][i] == 2:
                if con[0] > i + 1:
                    end = con[0]
                    start = i
                    for x in range(start, end):
                        grid[y][x] = 2
                elif con[len(con)-1] > C - i+1:
                    end = i
                    start = C - con[len(con)-1]
                    for x in range(start,end):
                        grid[y][x] = 2


    for x in range(C):
        con = col_constraints[x]
        if con[0] > R // 2 and len(con) == 1:
            start = max(0, R - con[0])
            end = min(R, con[0])
            for i in range(start, end):
                grid[i][x] = 2
        if len(con) > 1 and (con[0] > R - (sum(con) + len(con) - 1)):
            for a in range(len(con) - 1):
                startList = con[0:a + 1:1]
                startSum = sum(startList) + len(startList) - 1
                endList = con[-1:(-len(con)) + a - 1:-1]
                endSum = sum(endList) + len(endList) - 1
                if startSum > R - endSum:
                    start = R - endSum
                    end = startSum
                    for i in range(start, end):
                        grid[i][x] = 2
        for i in range(R):
            if grid[i][x] == 2:
                if con[0] > i + 1:
                    end = con[0]
                    start = i
                    for y in range(start, end):
                        grid[y][x] = 2
                elif con[len(con)-1] > R - i+1:
                    end = i
                    start = R - con[len(con)-1]
                    for y in range(start,end):
                        grid[y][x] = 2

    return grid


def solvePuzzle(grid, x, y, R, C, row_con: list[list], col_con: list[list]) -> list[list[int]]:
    pGrid = preprocessGrid(grid, row_con, col_con)
    print(pGrid)
    solved, solved_grid = solvePic(pGrid, 0, 0, R, C, row_con, col_con)
    print(solved_grid)
    if solved:
        for i in range(R):
            for j in range(C):
                if solved_grid[i][j] == 2:
                    solved_grid[i][j] = 1
        return solved_grid
    else:
        return []


def solvePic(grid, x, y, R, C, row_con, col_con):
    if y == R:
        return True, grid
    nextY = y
    if x == C - 1:
        nextX = 0
        nextY = y + 1
    else:
        nextX = x + 1
    if grid[y][x] == 2 and solvePic(grid, nextX, nextY, R, C, row_con, col_con)[0]:
        return True, grid
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
    if len(currentCol) == len(colRestrict):
        for i in range(len(currentCol)):
            if currentCol[i] > colRestrict[i]:
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
            currentRow[l] = currentRow[l] + 1
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
            currentCol[l] = currentCol[l] + 1
        else:
            currentCol.append(0)
            l += 1
    currentCol = [i for i in currentCol if i != 0]
    return currentCol


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




