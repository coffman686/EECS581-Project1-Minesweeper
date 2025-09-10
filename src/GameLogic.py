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


class ToggleMine(enum.Enum):
  Place = 1
  Remove = -1


# stub for BoardManager
type Board = list[list[Cell]]

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

  # sets the total number of mines to be placed
  def set_mines(self, mines):
    self.total_mines = mines

  # moves the game to the playing state and places mines
  def start_game(self):
    self.state = GameState.Playing
    self.initialize_board()

  # ends game on win or loss based on passed condition
  def end_game(self, win: EndCondition):
    if win:
      self.state = GameState.EndWin
    else:
      self.state = GameState.EndLose

  # resets the game state and the board state
  def reset_game(self, win: EndCondition):
    # self.board.reset()

    self.state: GameState = GameState.Start
    self.total_mines: int = 0
    self.flags_remaining: int = 0
    self.covered_cells: int = 0

  # converts ordered cell ids to indices
  def convert_coord_to_indices(self, id) -> tuple[int, int]:
    return (id // 10, id % 10)

  # samples and places mines in random locations
  def initialize_board(self):
    mines_coordinates = random.sample(range(100), k=self.total_mines)
    for coord in mines_coordinates:
      row, col = self.convert_coord_to_indices(coord)
      self.toggle_mine(row, col)

  # validates a given row and col within the board limits
  def valid_position(self, row, col):
    return 0 <= row <= 9 and 0 <= col <= 9

  # toggles a given cell as a mine and updates its neighbors' neighbor_count
  def toggle_mine(self, row, col):
    cell = self.board[row][col]
    # decrement if removing mine, increment if placing mine
    inc = -1 if cell.is_mine else 1
    cell.is_mine = not cell.is_mine
    for i in range(row - 1, row + 2):
      for j in range(col - 1, col + 2):
        if self.valid_position(i, j):
          self.board[i][j].neighbor_count += inc

  # safely uncover the first cell
  def uncover_first_cell(self, old_row, old_col):
    # continue normal processing if the cell is already safe
    if not self.board[old_row][old_col].is_mine:
      return

    while True:
      # pick a random cell
      new_row, new_col = self.convert_coord_to_indices(random.randrange(100))
      new_cell = self.board[new_row][new_col]
      # check that the cell does not already has a mine
      # prevents reselecting the same cell the user has
      if not new_cell.is_mine:
        # toggle and place a mine at the new cell
        self.toggle_mine(new_row, new_col)
        break
    # remove the mine at the original location
    self.toggle_mine(old_row, old_col)

  # uncover a selected cell
  def uncover_cell(self, row, col, first_cell: bool = False):
    cell = self.board[row][col]

    # uncover the first cell safely
    if first_cell:
      self.uncover_first_cell(row, col)

    if cell.is_mine:
      self.end_game(EndCondition.Loss)
    else:
      # uncover the cell
      cell.is_covered = False
      self.covered_cells -= 1

      # end if the cell has neighboring mines
      if cell.neighbor_count:
        return

      # recursively uncover neighbors
      for i in range(row - 1, row + 2):
        for j in range(col - 1, col + 2):
          if not self.valid_position(i, j):
            continue
          cell = self.board[i][j]
          if not cell.is_mine and cell.is_covered:
            self.uncover_cell(i, j)

    # check whether the user has uncovered all cells
    if self.covered_cells == 0:
      self.end_game(EndCondition.Win)

  # toggles a flag with flag count validation
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

  # temporary helpers for user interface
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

# stub for UserInterface and InputHandler
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
