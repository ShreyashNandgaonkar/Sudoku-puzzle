class Cell:
    

    def __init__(self, column_number, row_number, number, game):
        # Whether or not to include the cell in the backtracking
        self.solved = True if number > 0 else False
        self.number = number  # the current value of the cell
        # Which numbers the cell could potentially be
        self.possibilities = set(range(1, 10)) if not self.solved else []
        self.row = row_number  # the index of the row the cell is in
        self.column = column_number  # the index of the column the cell is in
        self.current_index = 0  # the index of the current possibility
        self.game = game  # the sudoku game the cell belongs to
        if not self.solved:  # runs the possibility checker
            self.find_possibilities()

    def check_area(self, area):
        
        values = [item for item in area if item != 0]
        return len(values) == len(set(values))
    def set_number(self):
        
        if not self.solved:
            self.number = self.possibilities[self.current_index]
            self.game.puzzle[self.row][self.column] = self.possibilities[self.current_index]

    def handle_one_possibility(self):
        if len(self.possibilities) == 1:
            self.solved = True
            self.set_number()

    def find_possibilities(self):
        for item in self.game.get_row(self.row) + self.game.get_column(self.column) + self.game.get_box(self.row, self.column):
            if not isinstance(item, list) and item in self.possibilities:
                self.possibilities.remove(item)
        self.possibilities = list(self.possibilities)
        self.handle_one_possibility()

    def is_valid(self):
        
        for unit in [self.game.get_row(self.row), self.game.get_column(self.column), self.game.get_box(self.row, self.column)]:
            if not self.check_area(unit):
                return False
        return True

    def increment_value(self):
        
        while not self.is_valid() and self.current_index < len(self.possibilities) - 1:
            self.current_index += 1
            self.set_number()
class SudokuSolver: 
    def __init__(self, puzzle):
        self.puzzle = puzzle  # the 2d list of spots on the board
        self.solve_puzzle = []  # 1d list of the Cell objects
        # the size of the boxes within the puzzle -- 3 for a typical puzzle
        self.box_size = int(len(self.puzzle) ** .5)
        self.backtrack_coord = 0  # what index the backtracking is currently at

    def get_row(self, row_number):
        
        return self.puzzle[row_number]

    def get_column(self, column_number):
        
        return [row[column_number] for row in self.puzzle]

    def find_box_start(self, coordinate):
        
        return coordinate // self.box_size * self.box_size
    def get_box_coordinates(self, row_number, column_number):
        
        return self.find_box_start(column_number), self.find_box_start(row_number)

    def get_box(self, row_number, column_number):
       
        start_y, start_x = self.get_box_coordinates(row_number, column_number)
        box = []
        for i in range(start_x, self.box_size + start_x):
            box.extend(self.puzzle[i][start_y:start_y+self.box_size])
        return box

    def initialize_board(self):
        
        for row_number, row in enumerate(self.puzzle):
            for column_number, item in enumerate(row):
                self.solve_puzzle.append(
                        Cell(column_number, row_number, item, self))

    def move_forward(self):
        
        while self.backtrack_coord < len(self.solve_puzzle) - 1 and self.solve_puzzle[self.backtrack_coord].solved:
            self.backtrack_coord += 1

    def backtrack(self):
        
        self.backtrack_coord -= 1
        while self.solve_puzzle[self.backtrack_coord].solved:
            self.backtrack_coord -= 1

    def set_cell(self):
        
        cell = self.solve_puzzle[self.backtrack_coord]
        cell.set_number()
        return cell
    def reset_cell(self, cell):
      
        cell.current_index = 0
        cell.number = 0
        self.puzzle[cell.row][cell.column] = 0

    def decrement_cell(self, cell):
        
        while cell.current_index == len(cell.possibilities) - 1:
            self.reset_cell(cell)
            self.backtrack()
            cell = self.solve_puzzle[self.backtrack_coord]
        cell.current_index += 1

    def change_cells(self, cell):
       
        if cell.is_valid():
            self.backtrack_coord += 1
        else:
            self.decrement_cell(cell)

    def solve(self):
        
        self.move_forward()
        cell = self.set_cell()
        cell.increment_value()
        self.change_cells(cell)

    def run_solve(self):
        
        while self.backtrack_coord <= len(self.solve_puzzle) - 1:
            self.solve()


def solve(puzzle):
    solver = SudokuSolver(puzzle)
    solver.initialize_board()
    solver.run_solve()
    return solver.puzzle
puzzle = [[5, 3, 0, 0, 7, 0, 0, 0, 0],
          [6, 0, 0, 1, 9, 5, 0, 0, 0],
          [0, 9, 8, 0, 0, 0, 0, 6, 0],
          [8, 0, 0, 0, 6, 0, 0, 0, 3],
          [4, 0, 0, 8, 0, 3, 0, 0, 1],
          [7, 0, 0, 0, 2, 0, 0, 0, 6],
          [0, 6, 0, 0, 0, 0, 2, 8, 0],
          [0, 0, 0, 4, 1, 9, 0, 0, 5],
          [0, 0, 0, 0, 8, 0, 0, 7, 9]]
pp=pprint.PrettyPrinter(width=41,compact=True)
solve(puzzle)
pp.pprint(puzzle)
