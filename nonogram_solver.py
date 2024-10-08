from flask import Flask, request, jsonify
from flask_cors import CORS
from itertools import product

app = Flask(__name__)
CORS(app)

global GRID


# Function preprocesses grid by finding nodes that must have a 1, used in initial solver.
def preprocessGrid(grid, row_constraints: list[list], col_constraints: list[list]):
    R, C = len(grid), len(grid[0])

    for y in range(R):
        con = row_constraints[y]
        if con[0] > C // 2 and len(con) == 1:  # If a single constraint is greater than half the length
            start = max(0, C - con[0])
            end = min(C, con[0])
            for i in range(start, end):  # Mark confirmed cells
                grid[y][i] = 2
        if len(con) > 1 and (con[0] > C - (sum(con) + len(con) - 1)):  # If the extremes of constraints overlap
            for a in range(len(con) - 1):
                startList = con[0:a + 1:1]
                startSum = sum(startList) + len(startList) - 1
                endList = con[-1:(-len(con)) + a - 1:-1]
                endSum = sum(endList) + len(endList) - 1
                if startSum > C - endSum:
                    start = C - endSum
                    end = startSum
                    for i in range(start, end):  # Mark confirmed cells
                        grid[y][i] = 2

    for x in range(C):
        con = col_constraints[x]
        if con[0] > R // 2 and len(con) == 1:  # If a single constraint is greater than half the length
            start = max(0, R - con[0])
            end = min(R, con[0])
            for i in range(start, end):  # Mark confirmed cells
                grid[i][x] = 2
        if len(con) > 1 and (con[0] > R - (sum(con) + len(con) - 1)):  # If the extremes of constraints overlap
            for a in range(len(con) - 1):
                startList = con[0:a + 1:1]
                startSum = sum(startList) + len(startList) - 1
                endList = con[-1:(-len(con)) + a - 1:-1]
                endSum = sum(endList) + len(endList) - 1
                if startSum > R - endSum:
                    start = R - endSum
                    end = startSum
                    for i in range(start, end):  # Mark confirmed cells
                        grid[i][x] = 2
    return grid


#  Main Wrapper for initial solver
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
    if y == R:  # If passed final row, end, return true
        return True, grid
    nextY = y
    if x == C - 1:  # If passed final column, increment row.
        nextX = 0
        nextY = y + 1
    else:
        nextX = x + 1
    if grid[y][x] == 2 and solvePic(grid, nextX, nextY, R, C, row_con, col_con)[0]:  # If node is confirmed, continue
        return True, grid
    #  Assume 1, check constraints.
    grid[y][x] = 1
    if is_Safe(grid, x, y, R, C, row_con, col_con) and solvePic(grid, nextX, nextY, R, C, row_con, col_con)[0]:
        return True, grid
    #  Previous node not safe, assume 0.
    grid[y][x] = 0
    if is_Safe(grid, x, y, R, C, row_con, col_con) and solvePic(grid, nextX, nextY, R, C, row_con, col_con)[0]:
        return True, grid
    return False, grid


def is_Safe(grid, x, y, R, C, row_con, col_con):
    #  Convert to restrictions
    currentRow = rowToRestriction(grid, y, C)
    currentCol = colToRestriction(grid, x, R)

    rowRestrict = row_con[y]
    colRestrict = col_con[x]
    if len(currentCol) == len(colRestrict):  # If constraints are same size compare element wise.
        for i in range(len(currentCol)):
            if currentCol[i] > colRestrict[i]:
                return False
    if currentRow > rowRestrict:
        return False
    if x == C - 1 and currentRow != rowRestrict:  # If reached last column and row restraints not satisfied
        return False
    if y == R - 1 and currentCol != colRestrict:  # If reached last row and column restraints not satisfied
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


def calc_perms(rowConstraints, C):
    # Generate all possible permutations for each row constraint
    permutations = [list(product([0, 1], repeat=C)) for _ in rowConstraints]

    # Filter permutations to only valid ones that satisfy constraints
    valid_permutations = []
    for row_constraint, row_permutations in zip(rowConstraints, permutations):
        valid_permutations.append([perm for perm in row_permutations if permIsSafe(perm, row_constraint)])

    return valid_permutations


def permToRestriction(row):
    currentRow = [0]
    l = 0
    for i in range(len(row)):
        if row[i] != 0:
            currentRow[l] += 1
        else:
            currentRow.append(0)
            l += 1
    currentRow = [i for i in currentRow if i != 0]
    return currentRow


def permIsSafe(perm, constraint):
    permRestrict = permToRestriction(perm)
    if permRestrict == constraint:
        return True
    return False


def combinationIsSafe(col, col_constraint, currentR, R):
    colRestrict = permToRestriction(col)
    if colRestrict == col_constraint:
        return True
    if colRestrict < col_constraint and currentR < R:
        return True
    return False


def find_valid_combination(permutations, R, col_constraints):
    def is_valid_combination(combination):
        for col_idx in range(len(combination[0])):  # For row in combination
            col = [row[col_idx] for row in combination]  # Create column by taking nodes at same X position in each row
            if not combinationIsSafe(col, col_constraints[col_idx], len(combination), R):  # Check if safe
                return False
        return True

    def backtrack(combination, row_idx):
        if row_idx == R:  # If final row is passed
            return combination
        for perm in permutations[row_idx]:  # For each permutation
            if is_valid_combination(combination + [perm]):  # Add perm, and check if valid.
                result = backtrack(combination + [perm], row_idx + 1)  # If valid, finalise adding to result
                if result:
                    return result  # If combination is valid return True
        return None

    return backtrack([], 0)  # Start recursion

#  Receiver for axios request, returns an empty grid if unsolvable, or the solution if solved.
@app.route("/solve", methods=["POST"])
def solve_nonogram():
    data = request.get_json()
    R = data.get("R")
    C = data.get("C")
    row_constraints = data.get("row")
    col_constraints = data.get("col")
    grid = [[0 for x in range(C)] for y in range(R)]
    permutations = calc_perms(row_constraints, C)
    valid_combination = find_valid_combination(permutations, R, col_constraints)
    if valid_combination:
        valid_combination = [list(row) for row in valid_combination]
    print(valid_combination)
    return jsonify({"solved_grid": valid_combination})


if __name__ == "__main__":
    app.run(debug=True)
