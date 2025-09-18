'''
BoardManager.py
Description: Manages the game board state for Minesweeper. Owns the Cell class representing each cell and the BoardManager class for the grid.
Inputs: None
Outputs: None
Author: Landon Bever
External Sources Used: None, all code is original
Creation Date: 09/10/2025
'''

import random


class Cell:
  '''represents a single cell on the Minesweeper board'''
  def __init__(self):
    '''initialize cell properties'''
    self.is_covered = True
    self.flagged = False
    self.is_mine = False
    self.neighbor_count = 0

  def reset(self):
    '''reset cell to initial state'''
    self.is_covered = True
    self.flagged = False
    self.is_mine = False
    self.neighbor_count = 0


class BoardManager:
  '''manages the Minesweeper board'''
  def __init__(self, rows=10, cols=10):
    '''initialize board with given dimensions'''
    self.rows = rows
    self.cols = cols
    self.grid = []

    # create grid of cells
    for r in range(rows):
      row = []
      for c in range(cols):
        row.append(Cell())
      self.grid.append(row)

  def in_bounds(self, r, c):
    """check if (r,c) is within board"""
    return 0 <= r < self.rows and 0 <= c < self.cols

  def neighbors(self, r, c):
    """return a list of in bounds neighbors"""
    result = []
    nr = r - 1
    while nr <= r + 1: # iterate through rows
      nc = c - 1
      while nc <= c + 1: # iterate through cols
        if not (nr == r and nc == c) and self.in_bounds(nr, nc): # skip self and out of bounds
          result.append((nr, nc))
        nc += 1
      nr += 1
    return result

  def reset(self):
    """reset all cells"""
    r = 0
    while r < self.rows: # iterate through rows
      c = 0
      while c < self.cols: # iterate through cols
        self.grid[r][c].reset() # reset each cell
        c += 1
      r += 1

  def clear_mines_and_counts(self):
    """remove all mines and set neighbor counts to 0"""
    r = 0
    while r < self.rows: # iterate through rows
      c = 0
      while c < self.cols: # iterate through cols
        cell = self.grid[r][c] # get cell
        cell.is_mine = False 
        cell.neighbor_count = 0
        c += 1
      r += 1

  def adjust_neighbor_counts(self, r, c, amount):
    """adjust neighbor_count in 3x3 area around (r,c)"""
    nr = r - 1
    while nr <= r + 1: # iterate through rows
      nc = c - 1
      while nc <= c + 1: # iterate through cols
        if self.in_bounds(nr, nc): # skip out of bounds
          self.grid[nr][nc].neighbor_count += amount # adjust count
        nc += 1
      nr += 1

  def set_mine(self, r, c, value):
    """mine setter with neighbor count updates"""
    cell = self.grid[r][c] # get cell
    if cell.is_mine == value:
      return
    cell.is_mine = value 
    if value: # if placing a mine, increment neighbor counts
      self.adjust_neighbor_counts(r, c, 1)
    else: # if removing a mine, decrement neighbor counts
      self.adjust_neighbor_counts(r, c, -1)

  def toggle_mine(self, r, c):
    """toggle mine"""
    self.set_mine(r, c, not self.grid[r][c].is_mine)

  def place_unique_mines(self, total_mines, exclude=None):
    """place mines at unique random locations, guarantee safe spot if exclude is given"""
    self.clear_mines_and_counts() # clear existing mines and counts
    coords = []
    r = 0
    while r < self.rows: # iterate through rows
      c = 0
      while c < self.cols: # iterate through cols
        # only add to possible coords if not excluded
        if exclude is None or not (r == exclude[0] and c == exclude[1]):
          coords.append((r, c)) 
        c += 1
      r += 1

    chosen = random.sample(coords, k=total_mines) # choose unique random coordinates

    i = 0
    while i < len(chosen): # place mines at chosen coordinates
      rr, cc = chosen[i]
      self.set_mine(rr, cc, True)
      i += 1

  def uncover(self, r, c):
    '''uncover cell at (r,c)'''
    self.grid[r][c].is_covered = False

  def cover(self, r, c):
    '''cover cell at (r,c)'''
    self.grid[r][c].is_covered = True

  def set_flag(self, r, c, value):
    '''set flag state at (r,c)'''
    self.grid[r][c].flagged = value

  def toggle_flag(self, r, c):
    '''toggle flag state at (r,c)'''
    self.grid[r][c].flagged = not self.grid[r][c].flagged

  def cell(self, r, c):
    '''get cell at (r,c)'''
    return self.grid[r][c]