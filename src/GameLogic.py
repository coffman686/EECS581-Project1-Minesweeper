import random
import enum

from BoardManager import BoardManager


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


class GameLogic:
  def __init__(self):
    self.state: GameState = GameState.Start
    self.total_mines: int = 0
    self.flags_remaining: int = 0
    self.covered_cells: int = 0
    self.board = BoardManager()

  # sets the total number of mines to be placed
  def set_mines(self, mines):
    self.total_mines = mines
    self.flags_remaining = mines
    self.covered_cells = 100 - mines

  # moves the game to the playing state and places mines
  def start_game(self):
    self.state = GameState.Playing
    self.initialize_board()

  # ends game on win or loss based on passed condition
  def end_game(self, win: EndCondition):
    if win == EndCondition.Win:
      self.state = GameState.EndWin
    else:
      self.state = GameState.EndLose

  # resets the game state and the board state
  def reset_game(self, win: EndCondition):
    self.board.reset()

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
      self.board.toggle_mine(row, col)

  # safely uncover the first cell
  def uncover_first_cell(self, old_row, old_col):
    # continue normal processing if the cell is already safe
    if not self.board.cell(old_row, old_col).is_mine:
      return

    while True:
      # pick a random cell
      new_row, new_col = self.convert_coord_to_indices(random.randrange(100))
      new_cell = self.board.cell(new_row, new_col)
      # check that the cell does not already has a mine
      # prevents reselecting the same cell the user has
      if not new_cell.is_mine:
        # place a mine at the new cell
        self.board.toggle_mine(new_row, new_col)
        break
    # remove the mine at the original location
    self.board.toggle_mine(old_row, old_col)

  # uncover a selected cell
  def uncover_cell(self, row, col, first_cell: bool = False):
    cell = self.board.cell(row, col)

    # uncover the first cell safely
    if first_cell:
      self.uncover_first_cell(row, col)

    if cell.is_mine:
      self.end_game(EndCondition.Loss)
    else:
      # uncover the cell
      self.board.uncover(row, col)
      self.covered_cells -= 1

      # end if the cell has neighboring mines
      if cell.neighbor_count:
        return

      # recursively uncover neighbors
      adjacent = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
      for i, j in adjacent:
        if not self.board.in_bounds(i, j):
          continue
        cell = self.board.cell(i, j)
        if not cell.is_mine and cell.is_covered:
          self.uncover_cell(i, j)

    # check whether the user has uncovered all cells
    if self.covered_cells == 0:
      self.end_game(EndCondition.Win)

  # toggles a flag with flag count validation
  def toggle_flagged_cell(self, row, col):
    cell = self.board.cell(row, col)
    if cell.flagged:
      self.board.set_flag(row, col, False)
      self.flags_remaining += 1
    elif self.flags_remaining > 0:
      self.board.set_flag(row, col, True)
      self.flags_remaining -= 1
