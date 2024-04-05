from itertools import product


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


def calc_perms(rowConstraints, C):
    # Generate all possible permutations for each row constraint
    permutations = [list(product([0, 1], repeat=C)) for _ in rowConstraints]

    # Filter permutations that satisfy the row constraints
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
        for col_idx in range(len(combination[0])):
            col = [row[col_idx] for row in combination]
            if not combinationIsSafe(col, col_constraints[col_idx], len(combination), R):
                return False
        return True

    def backtrack(combination, row_idx):
        if row_idx == R:
            return combination
        for perm in permutations[row_idx]:
            if is_valid_combination(combination + [perm]):
                result = backtrack(combination + [perm], row_idx + 1)
                if result:
                    return result
        return None

    return backtrack([], 0)


"""
row_constraints = [[3,6],
                   [2,3,3],
                   [1,2,3],
                   [2,5,2],
                   [1,2,2,2],
                   [2,1,1,2],
                   [1,1,1,2],
                   [2,1,2,2],
                   [2,1,2,1],
                   [2,2,3,1],
                   [2,4,2],
                   [2],
                   [3,1,1],
                   [3,3,2],
                   [6,3]
                   ]
col_constraints = [[3,6],
                   [2,9],
                   [1,3,2],
                   [2,2],
                   [2,4,1],
                   [1,2,2,1],
                   [2,1,1,1],
                   [1,1,1,1],
                   [1,1,2,1],
                   [1,1,3,1],
                   [1,8,1],
                   [2,2,1,1],
                   [2,1,1,1],
                   [8,2],
                   [6,3]]
"""


def test_solvePuzzle():
    R = 10
    C = 6
    row_constraints = [[1, 1], [1], [1, 1], [1], [1, 1], [2], [6], [2, 1], [2, 1], [4]]
    col_constraints = [[1], [1, 4], [1, 1, 5], [1, 4, 1], [1, 1, 4], [1]]
    grid = [[0 for x in range(C)] for y in range(R)]
    solved_grid = solvePuzzle(grid, 0, 0, R, C, row_constraints, col_constraints)
    print(solved_grid)


def test_multicon():
    con = [3, 4]
    C = 10
    tempRow = [0 for a in range(C)]
    if len(con) > 1 and (con[0] > C - (sum(con) + len(con) - 1)):
        for a in range(len(con) - 1):
            startList = con[0:a + 1:1]
            startsum = sum(startList) + len(startList) - 1
            endList = con[-1:(-len(con)) + a - 1:-1]
            endsum = sum(endList) + len(endList) - 1
            if startsum > C - endsum:
                start = C - endsum
                end = startsum
                for i in range(start, end):
                    tempRow[i] = 2

    assert tempRow == [0, 0, 2, 0, 0, 0, 0, 0, 0, 0]


def test_calcAllPermutations():
    C = 6
    permutations = [list(product([0, 1], repeat=C))]
    count = 0
    for i, row_perms in enumerate(permutations):
        print(f"Row {i + 1} Permutations:")
        for perm in row_perms:
            count += 1
            print(perm)
        print()
    assert count == 64


def test_calcValidPermutations():
    row_constraints = [[1, 1], [1], [1, 1], [1], [1, 1], [2], [6], [2, 1], [2, 1], [4]]
    C = 6
    permutations = calc_perms(row_constraints, C)
    for i, row_perms in enumerate(permutations):
        print(f"Row {i + 1} Permutations:")
        for perm in row_perms:
            print(perm)
        print()


def test_findValidCombination():
    R = 10
    C = 6
    row_constraints = [[1, 1], [1], [1, 1], [1], [1, 1], [2], [6], [2, 1], [2, 1], [4]]
    col_constraints = [[1], [1, 4], [1, 1, 5], [1, 4, 1], [1, 1, 4], [1]]
    permutations = calc_perms(row_constraints, C)
    for i, row_perms in enumerate(permutations):
        print(f"Row {i + 1} Permutations:")
        for perm in row_perms:
            print(perm)
        print()
    valid_combination = find_valid_combination(permutations, R, col_constraints)
    valid_combination = [list(row) for row in valid_combination]
    print("Valid combination:")
    for row in valid_combination:
        print(row)
