import collections
import copy
import itertools
import queue
import random

def sudoku_cells():
    cells_list = []
    for i in range(9):
        for j in range(9):
            cell = [i, j]
            cell = tuple(cell)
            cells_list.append(cell)

    return cells_list

def sudoku_arcs():
    arcs_list = []

    for x in range(9):
        for y in range(9):

            cell = [x, y]
            cell = tuple(cell)

            # ADD SAME ROWS
            for k in range(9):
                if k == y:
                    continue
                neighbor = [x, k]
                neighbor = tuple(neighbor)

                arc = [cell, neighbor]
                arc = tuple(arc)
                if arc not in arcs_list:
                    arcs_list.append(arc)

            # ADD SAME COLS
            for j in range(9):
                if j == x:
                    continue
                neighbor = [j, y]
                neighbor = tuple(neighbor)

                arc = [cell, neighbor]
                arc = tuple(arc)
                if arc not in arcs_list:
                    arcs_list.append(arc)

            # ADD SAME BLOCK
            if x <= 2 and y <= 2:
                for i in range(3):
                    for j in range(3):
                        neighbor = [i, j]
                        neighbor = tuple(neighbor)

                        if neighbor == cell:
                            continue
                        arc = [cell, neighbor]
                        arc = tuple(arc)
                        if arc not in arcs_list:
                            arcs_list.append(arc)

            elif x <= 2 and y <= 5:
                for i in range(3):
                    for j in range(3, 6):
                        neighbor = [i, j]
                        neighbor = tuple(neighbor)

                        if neighbor == cell:
                            continue
                        arc = [cell, neighbor]
                        arc = tuple(arc)
                        if arc not in arcs_list:
                            arcs_list.append(arc)

            elif x <= 2 and y <= 8:
                for i in range(3):
                    for j in range(6, 9):
                        neighbor = [i, j]
                        neighbor = tuple(neighbor)

                        if neighbor == cell:
                            continue
                        arc = [cell, neighbor]
                        arc = tuple(arc)
                        if arc not in arcs_list:
                            arcs_list.append(arc)

            elif x <= 5 and y <= 2:
                for i in range(3, 6):
                    for j in range(3):
                        neighbor = [i, j]
                        neighbor = tuple(neighbor)

                        if neighbor == cell:
                            continue
                        arc = [cell, neighbor]
                        arc = tuple(arc)
                        if arc not in arcs_list:
                            arcs_list.append(arc)

            elif x <= 5 and y <= 5:
                for i in range(3, 6):
                    for j in range(3, 6):
                        neighbor = [i, j]
                        neighbor = tuple(neighbor)

                        if neighbor == cell:
                            continue
                        arc = [cell, neighbor]
                        arc = tuple(arc)
                        if arc not in arcs_list:
                            arcs_list.append(arc)

            elif x <= 5 and y <= 8:
                for i in range(3, 6):
                    for j in range(6, 9):
                        neighbor = [i, j]
                        neighbor = tuple(neighbor)

                        if neighbor == cell:
                            continue
                        arc = [cell, neighbor]
                        arc = tuple(arc)
                        if arc not in arcs_list:
                            arcs_list.append(arc)

            elif x <= 8 and y <= 2:
                for i in range(6, 9):
                    for j in range(3):
                        neighbor = [i, j]
                        neighbor = tuple(neighbor)

                        if neighbor == cell:
                            continue
                        arc = [cell, neighbor]
                        arc = tuple(arc)
                        if arc not in arcs_list:
                            arcs_list.append(arc)

            elif x <= 8 and y <= 5:
                for i in range(6, 9):
                    for j in range(3, 6):
                        neighbor = [i, j]
                        neighbor = tuple(neighbor)

                        if neighbor == cell:
                            continue
                        arc = [cell, neighbor]
                        arc = tuple(arc)
                        if arc not in arcs_list:
                            arcs_list.append(arc)

            elif x <= 8 and y <= 8:
                for i in range(6, 9):
                    for j in range(6, 9):
                        neighbor = [i, j]
                        neighbor = tuple(neighbor)

                        if neighbor == cell:
                            continue
                        arc = [cell, neighbor]
                        arc = tuple(arc)
                        if arc not in arcs_list:
                            arcs_list.append(arc)
    return arcs_list

def read_board(path):
    dictionary = {}
    values = set()
    for num in range(1, 10):
        values.add(num)

    i = 0
    j = 0

    file = open(path)

    for line in file:
        linelist = list(line)

        for char in linelist:
            cell = [i, j]
            cell = tuple(cell)

            if char == "*":
                dictionary[cell] = values

            elif char == " " or char == "\n":
                continue

            else:
                singlevalue = set()
                char = int(char.strip(), 10)
                singlevalue.add(char)
                dictionary[cell] = singlevalue

            j += 1

        j = 0
        i += 1

    return dictionary

class Sudoku(object):

    CELLS = sudoku_cells()
    ARCS = sudoku_arcs()

    def __init__(self, board):
        self.board = board

    def get_values(self, cell):
        board = self.board
        return board[cell]

    def remove_inconsistent_values(self, cell1, cell2):
        board = self.board

        arc = [cell1, cell2]
        arc = tuple(arc)

        # CHECK IF CONFLICTING CELLS
        if arc in Sudoku.ARCS:
            value_set_2 = board[cell2]

            # Check IF CELL2 FILLED (only one value in set)
            if len(value_set_2) == 1:
                value = list(value_set_2)[0]

                value_set_1 = board[cell1]

                # CHECK IF VALUE IS IN CELL2'S SET
                if value in value_set_1:
                    value_list = list(value_set_1)

                    new_value_set = set()

                    # EDIT CELL1'S SET
                    for item in value_list:
                        if item == value:
                            continue
                        new_value_set.add(item)

                    board[cell1] = new_value_set
                    return True
        return False

    def infer_ac3(self):
        arc_queue = queue.Queue()

        for arc in Sudoku.ARCS:
            arc_queue.put(arc)

        while not arc_queue.empty():
            arc = arc_queue.get()
            first = arc[0]
            second = arc[1]

            if Sudoku.remove_inconsistent_values(self, first, second):
                for arc in Sudoku.ARCS:
                    if arc[1] == first and not arc[0] == second:
                        arc_queue.put(arc)

    def infer_improved(self):
        # LOOP UNTIL SOLVED
        flag = True
        while flag:

            # RUN AC3 - UPDATE VALUE SETS
            self.infer_ac3()
            flag = False

            # FOR EACH CELL
            for cell in Sudoku.CELLS:
                value_set = self.board[cell]

                if len(value_set) == 1:
                    continue

                row = cell[0]
                col = cell[1]
                block_row = cell[0] // 3
                block_col = cell[1] // 3


                # FOR EACH VALUE
                for value in value_set:

                    check_row = True
                    check_col = True
                    check_block = True

                    # CHECK ROW
                    for i in range(9):
                        neighbor_row = (row, i)
                        if i == col:
                            continue
                        value_set_2 = self.board[neighbor_row]
                        if value in value_set_2:
                            check_row = False
                            break

                    if check_row:
                        # CHANGE VALUE!
                        self.board[cell] = {value}
                        self.infer_ac3()
                        flag = True
                        break

                    # CHECK COL
                    for j in range(9):
                        neighbor_col = (j, col)
                        if j == row:
                            continue
                        value_set_3 = self.board[neighbor_col]
                        if value in value_set_3:
                            check_col = False
                            break

                    if check_col:
                        # CHANGE VALUE!
                        self.board[cell] = {value}
                        self.infer_ac3()
                        flag = True
                        break

                    # CHECK BLOCK
                    for another_cell in Sudoku.CELLS:
                        if another_cell[0]//3 == block_row and another_cell[1]//3 == block_col:
                            if another_cell[0] == row and another_cell[1] == col:
                                continue
                            value_set_4 = self.board[another_cell]
                            if value in value_set_4:
                                check_block = False
                                break

                    if check_block:
                        # CHANGE VALUE!
                        self.board[cell] = {value}
                        self.infer_ac3()
                        flag = True
                        break

    def check_solved(self):
        board = self.board
        for i in range(9):
            for j in range(9):
                cell = [i, j]
                cell = tuple(cell)
                value_set = board[cell]
                if not len(value_set) == 1:
                    return False
        return True


    def infer_with_guessing(self):
        # CALL INFER IMPROVED
        self.infer_improved()

        # FOR ALL CELLS THAT AREN'T ASSIGNED
        for cell in Sudoku.CELLS:

            value_set = self.board[cell]

            if len(value_set) == 1:
                continue

            # MAKE A COPY OF THE BOARD FOR BACKTRACKING
            board_copy = copy.deepcopy(self.board)

            # GUESS A VALUE
            for value in value_set:
                self.board[cell] = {value}

                # RECURSE!
                self.infer_with_guessing()

                # IF SOLVED BREAK
                if self.check_solved():
                    break
                # ELSE BACKTRACK!
                else:
                    self.board = board_copy

    def create_solution(self):
        if not self.check_solved():
            print('Problem not solved')
            return False
        else:
            file = open('solution.txt', 'w')
            board = self.board
            for i in range(9):
                row = []
                for j in range(9):
                    cell = [i, j]
                    cell = tuple(cell)
                    value_set = board[cell]
                    for item in value_set:
                        row.append(item)
                for num in row:
                    file.write(str(num))
                file.write('\n')
            file.close()
            return True