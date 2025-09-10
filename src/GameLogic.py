import random
import enum

# TODO: remove random seeding
random.seed(0)


class Cell:
  def __init__(self):
    self.is_covered = True
    self.flagged = False
    self.is_mine = False
    self.neighbor_count = 0

  def reset(self):
    self.is_covered = True
    self.flagged = False
    self.is_mine = False
    self.neighbor_count = 0


class GameState(enum.Enum):
  Start = 0
  Playing = 1
  EndWin = 2
  EndLose = 3


class EndCondition(enum.Enum):
  Win = True
  Loss = False


type Board = list[list[Cell]]


# stub for board
board = []
for _ in range(10):
  row = []
  for _ in range(10):
    row.append(Cell())
  board.append(row)


class GameLogic:
  def __init__(self, board):
    self.state: GameState = GameState.Start
    self.total_mines: int = 0
    self.flags_remaining: int = 0
    self.covered_cells: int = 0
    self.board: list[list[Cell]] = board

  def set_mines(self, mines):
    self.total_mines = mines

  def start_game(self):
    self.state = GameState.Playing
    self.initialize_board()

  def end_game(self, win: EndCondition):
    if win:
      self.state = GameState.EndWin
    else:
      self.state = GameState.EndLose

  def reset_game(self, win: EndCondition):
    # self.board.reset()

    self.state: GameState = GameState.Start
    self.total_mines: int = 0
    self.flags_remaining: int = 0
    self.covered_cells: int = 0

  def convert_coord_to_indices(self, id) -> tuple[int, int]:
    return (id // 10, id % 10)

  def initialize_board(self):
    mines_coordinates = random.sample(range(100), k=self.total_mines)
    for coord in mines_coordinates:
      row, col = self.convert_coord_to_indices(coord)
      self.place_mine(row, col)

  def valid_position(self, row, col):
    return 0 <= row <= 9 and 0 <= col <= 9

  def place_mine(self, row, col):
    self.board[row][col].is_mine = True
    for i in range(row - 1, row + 2):
      for j in range(col - 1, col + 2):
        if self.valid_position(i, j):
          self.board[i][j].neighbor_count += 1

  def remove_mine(self, row, col):
    self.board[row][col].is_mine = False
    for i in range(row - 1, row + 2):
      for j in range(col - 1, col + 2):
        if self.valid_position(i, j):
          self.board[i][j].neighbor_count -= 1

  def uncover_first_cell(self, old_row, old_col):
    while True:
      new_row, new_col = self.convert_coord_to_indices(random.randrange(100))
      new_cell = self.board[new_row][new_col]
      if not new_cell.is_mine:
        self.place_mine(new_row, new_col)
        break
    self.remove_mine(old_row, old_col)

  def uncover_cell(self, row, col, first_cell: bool = False):
    cell = self.board[row][col]

    if first_cell and cell.is_mine:
      self.uncover_first_cell(row, col)

    if cell.is_mine:
      self.end_game(EndCondition.Loss)
    else:
      cell.is_covered = False
      self.covered_cells -= 1

      if cell.neighbor_count:
        return

      for i in range(row - 1, row + 2):
        for j in range(col - 1, col + 2):
          if not self.valid_position(i, j):
            continue
          cell = self.board[i][j]
          if not cell.is_mine and cell.is_covered:
            self.uncover_cell(i, j)

    if self.covered_cells == 0:
      self.end_game(EndCondition.Win)

  def toggle_flagged_cell(self, row, col):
    cell = self.board[row][col]
    if cell.flagged:
      if self.flags_remaining > 0:
        cell.flagged = False
        self.flags_remaining -= 1
    else:
      if self.flags_remaining < 10:
        cell.flagged = True
        self.flags_remaining += 1

  def print_board(self, debug: bool = False):
    for row in self.board:
      for cell in row:
        if cell.flagged:
          print(" ", end="")
        if not debug and cell.is_covered:
          print(" ", end="")
          continue
        if cell.is_mine:
          print(" ", end="")
        else:
          print(f"{cell.neighbor_count} ", end="")
      print("")

  def __repr__(self):
    print(self.state)
    self.print_board(debug=True)
    return ""


logic = GameLogic(board)
logic.set_mines(10)
logic.start_game()

logic.print_board(True)

first = True
while True:
  logic.print_board()
  inp = int(input("Enter coordinate:"))
  row, col = logic.convert_coord_to_indices(inp)

  logic.uncover_cell(row, col, first)
  if first:
    first = False

  if logic.state == GameState.EndWin or logic.state == GameState.EndLose:
    print("Win!")
    break
