# Module: GameLogic
# Description: handles base game functionality and management of state
# Inputs: None
# Outputs: None
# External sources: None
# Created ~2025-09-05 by Aryan Kevat

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

  def set_mines(self, mines: int):
    """sets the total number of mines to be placed"""
    self.total_mines = mines
    self.flags_remaining = mines
    self.covered_cells = 100 - mines

  def start_game(self):
    """moves the game to the playing state and places mines"""
    self.state = GameState.Playing
    self.initialize_board()

  def end_game(self, condition: EndCondition):
    """ends game based on passed condition"""
    if condition == EndCondition.Win:
      self.state = GameState.EndWin
    else:
      self.state = GameState.EndLose

  def reset_game(self):
    """resets the game state and the board state"""
    self.board.reset()
    self.state = GameState.Start
    self.total_mines = 0
    self.flags_remaining = 0
    self.covered_cells = 0

  def initialize_board(self):
    """samples and places mines in random locations"""
    mines_coordinates = random.sample(range(100), k=self.total_mines)
    for coord in mines_coordinates:
      row, col = coord // 10, coord % 10
      self.board.toggle_mine(row, col)

  def uncover_first_cell(self, old_row: int, old_col: int):
    """safely uncover the first cell"""
    # continue normal processing if the cell is already safe
    if not self.board.cell(old_row, old_col).is_mine:
      return

    while True:
      # pick a random cell
      new_row, new_col = random.randrange(10), random.randrange(10)
      new_cell = self.board.cell(new_row, new_col)
      # check that the cell does not already has a mine
      # prevents reselecting the same cell the user has
      if not new_cell.is_mine:
        # place a mine at the new cell
        self.board.toggle_mine(new_row, new_col)
        break
    # remove the mine at the original location
    self.board.toggle_mine(old_row, old_col)

  def uncover_cell(self, row: int, col: int):
    """uncover a selected cell"""
    cell = self.board.cell(row, col)

    if cell.flagged:
      return

    # uncover the first cell safely
    if self.covered_cells == 100 - self.total_mines:
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

  def toggle_flagged_cell(self, row: int, col: int):
    """toggles flagged state with flag count validation"""
    cell = self.board.cell(row, col)
    if cell.flagged:
      self.board.set_flag(row, col, False)
      self.flags_remaining += 1
    elif self.flags_remaining > 0:
      self.board.set_flag(row, col, True)
      self.flags_remaining -= 1
