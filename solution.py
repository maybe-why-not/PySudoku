from collections import OrderedDict

assignments = []

rows = 'ABCDEFGHI'
cols = '123456789'

def cross(a, b):
    return [(r + c) for r in a for c in b]

boxes = cross(rows, cols)

row_units = [cross(r, cols) for r in rows]
column_units = [cross(rows, c) for c in cols]
square_units = [cross(rs, cs) for rs in ('ABC', 'DEF', 'GHI') for cs in ('123', '456', '789')]
diagonal_uldr_units = [['A1', 'B2', 'C3', 'D4', 'E5', 'F6', 'G7', 'H8', 'I9']]
diagonal_urdl_units = [['A9', 'B8', 'C7', 'D6', 'E5', 'F4', 'G3', 'H2', 'I1']]

unit_list = row_units + column_units + square_units + diagonal_uldr_units + diagonal_urdl_units

units = dict((s, [u for u in unit_list if s in u]) for s in boxes)
peers = dict((s, set(sum(units[s], []))-set([s])) for s in boxes)


def assign_value(values, box, value):
    values[box] = value
    if len(value) == 1:
        assignments.append(values.copy())
    return values

def naked_twins(values):
    twins = [box for box in values.keys() if len(values[box]) == 2]
    # print(twins)

    if not twins:
        return values # No twins found on this iteration

    peer_twins = [(twin1, twin2) for twin1 in twins for twin2 in peers[twin1] if set(values[twin1]) == set(values[twin2])]
    # print(peer_twins)

    if not peer_twins:
        return values # No twins of peers found on this iteration

    for index in range(len(peer_twins)):
        common_peers = peers[peer_twins[index][0]] & peers[peer_twins[index][1]] # Get common peers of both twins

        for common in common_peers:
            # print(common_peers)
            if len(values[common]) > 2:
                for digit in values[peer_twins[index][0]]:
                    # Circle through both digits of a twin and remove them from each common peer
                    values = assign_value(values, common, values[common].replace(digit, ''))

    return values

def grid_values(grid):
    """
    Convert grid string into {<box>: <value>} dict with '123456789' value for empties.

    Args:
        grid: Sudoku grid in string form, 81 characters long
    Returns:
        Sudoku grid in dictionary form:
        - keys: Box labels, e.g. 'A1'
        - values: Value in corresponding box, e.g. '8', or '123456789' if it is empty.
    """
    grid_dict = dict(zip(boxes, grid))

    for index, box in grid_dict.items():
        if box == ".":
            grid_dict[index] = '123456789'

    return grid_dict

def display(values):
    width = 1+max(len(values[s]) for s in boxes)
    line = '+'.join(['-'*(width*3)]*3)
    for r in rows:
        print(''.join(values[r+c].center(width)+('|' if c in '36' else '') for c in cols))
        if r in 'CF': print(line)
    print

def eliminate(values):
    solved_values = [box for box in values.keys() if len(values[box]) == 1]

    for box in solved_values:
        digit = values[box]

        for peer in peers[box]:
            values[peer] = values[peer].replace(digit,'')
    return values

def only_choice(values):
    """
    Finalize all values that are the only choice for a unit.

    Go through all the units, and whenever there is a unit with a value
    that only fits in one box, assign the value to this box.

    Input: Sudoku in dictionary form.
    Output: Resulting Sudoku in dictionary form after filling in only choices.
    """
    for unit in unit_list:

        for digit in '123456789':

            dplaces = [box for box in unit if digit in values[box]]

            if len(dplaces) == 1:
                values[dplaces[0]] = digit

    return values

def reduce_puzzle(values):
    """
    Iterate eliminate() and only_choice(). If at some point, there is a box with no available values, return False.
    If the sudoku is solved, return the sudoku.
    If after an iteration of both functions, the sudoku remains the same, return the sudoku.

    Input: A sudoku in dictionary form.
    Output: The resulting sudoku in dictionary form.
    """
    stalled = False

    while not stalled:
        solved_values_before = len([box for box in values.keys() if len(values[box]) == 1])

        values = eliminate(values)

        values = only_choice(values)

        values = naked_twins(values)

        solved_values_after = len([box for box in values.keys() if len(values[box]) == 1])
        stalled = solved_values_before == solved_values_after

        if len([box for box in values.keys() if len(values[box]) == 0]):
            return False

    return values

def search(values):
    """
    Using depth-first search and propagation, try all possible values.
    """
    values = reduce_puzzle(values)

    if values is False:
        return False

    if all(len(values[s]) == 1 for s in boxes):
        return values

    n, s = min((len(values[s]), s) for s in boxes if len(values[s]) > 1)

    for value in values[s]:
        new_sudoku = values.copy()
        new_sudoku[s] = value
        attempt = search(new_sudoku)
        if attempt:
            return attempt

def solve(grid):
    """
    Find the solution to a Sudoku grid.
    Args:
        grid(string): a string representing a sudoku grid.
            Example: '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    Returns:
        The dictionary representation of the final sudoku grid. False if no solution exists.
    """

    return search(grid_values(grid))


if __name__ == '__main__':
    diag_sudoku_grid = '2.............62....1....7...6..8...3...9...7...6..4...4....8....52.............3'
    #diag_sudoku_grid = '4.....8.5.3..........7......2.....6.....8.4......1.......6.3.7.5..2.....1.4......'
    display(solve(diag_sudoku_grid))

    try:
        from visualize import visualize_assignments
        visualize_assignments(assignments)

    except SystemExit:
        pass
    except:
        print('We could not visualize your board due to a pygame issue. Not a problem! It is not a requirement.')
