from itertools import product


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


# Test initial solve puzzle

def test_solvePuzzle():
    R = 10
    C = 6
    row_constraints = [[1, 1], [1], [1, 1], [1], [1, 1], [2], [6], [2, 1], [2, 1], [4]]
    col_constraints = [[1], [1, 4], [1, 1, 5], [1, 4, 1], [1, 1, 4], [1]]
    grid = [[0 for x in range(C)] for y in range(R)]
    solved_grid = solvePuzzle(grid, 0, 0, R, C, row_constraints, col_constraints)
    print(solved_grid)


# Test multi-constraint preprocess
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


# Test calculating all possible permutations
def test_calcAllPermutations():
    C = 15
    permutations = [list(product([0, 1], repeat=C))]
    count = 0
    for i, row_perms in enumerate(permutations):
        print(f"Row {i + 1} Permutations:")
        for perm in row_perms:
            count += 1
            print(perm)
        print()


# Test calculating all valid permutations
def test_calcValidPermutations():
    row_constraints = [[7, 2], [1, 3, 1, 2], [4, 1, 1], [4, 1, 1], [6, 5], [1, 2], [1, 4], [2, 3], [2, 3], [2, 3],
                       [2, 1, 3], [2, 6, 1, 3], [2, 1, 4, 1, 3], [2, 1, 4, 1, 3], [2, 1, 4, 1, 3]]
    C = 15
    permutations = calc_perms(row_constraints, C)
    for i, row_perms in enumerate(permutations):
        print(f"Row {i + 1} Permutations:")
        for perm in row_perms:
            print(perm)
        print()


# Test to find a valid combination of rows to complete grid
def test_findValidCombination():
    R = 5
    C = 5
    row_constraints = [[5], [5], [5], [5], [5]]
    col_constraints = [[5], [5], [5], [5], [5]]
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
