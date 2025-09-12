import random


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


class BoardManager:
  def __init__(self, rows=10, cols=10):
    self.rows = rows
    self.cols = cols
    self.grid = []
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
    while nr <= r + 1:
      nc = c - 1
      while nc <= c + 1:
        if not (nr == r and nc == c) and self.in_bounds(nr, nc):
          result.append((nr, nc))
        nc += 1
      nr += 1
    return result

  def reset(self):
    """reset all cells"""
    r = 0
    while r < self.rows:
      c = 0
      while c < self.cols:
        self.grid[r][c].reset()
        c += 1
      r += 1

  def clear_mines_and_counts(self):
    """remove all mines and set neighbor counts to 0"""
    r = 0
    while r < self.rows:
      c = 0
      while c < self.cols:
        cell = self.grid[r][c]
        cell.is_mine = False
        cell.neighbor_count = 0
        c += 1
      r += 1

  def adjust_neighbor_counts(self, r, c, amount):
    """adjust neighbor_count in 3x3 area around (r,c)"""
    nr = r - 1
    while nr <= r + 1:
      nc = c - 1
      while nc <= c + 1:
        if self.in_bounds(nr, nc):
          self.grid[nr][nc].neighbor_count += amount
        nc += 1
      nr += 1

  def set_mine(self, r, c, value):
    """mine setter with neighbor count updates"""
    cell = self.grid[r][c]
    if cell.is_mine == value:
      return
    cell.is_mine = value
    if value:
      self.adjust_neighbor_counts(r, c, 1)
    else:
      self.adjust_neighbor_counts(r, c, -1)

  def toggle_mine(self, r, c):
    """toggle mine"""
    self.set_mine(r, c, not self.grid[r][c].is_mine)

  def place_unique_mines(self, total_mines, exclude=None):
    """place mines at unique random locations, guarantee safe spot if exclude is given"""
    self.clear_mines_and_counts()
    coords = []
    r = 0
    while r < self.rows:
      c = 0
      while c < self.cols:
        if exclude is None or not (r == exclude[0] and c == exclude[1]):
          coords.append((r, c))
        c += 1
      r += 1

    chosen = random.sample(coords, k=total_mines)

    i = 0
    while i < len(chosen):
      rr, cc = chosen[i]
      self.set_mine(rr, cc, True)
      i += 1

  def uncover(self, r, c):
    self.grid[r][c].is_covered = False

  def cover(self, r, c):
    self.grid[r][c].is_covered = True

  def set_flag(self, r, c, value):
    self.grid[r][c].flagged = value

  def toggle_flag(self, r, c):
    self.grid[r][c].flagged = not self.grid[r][c].flagged

  def cell(self, r, c):
    return self.grid[r][c]

  # def covered_count(self):
  #   count = 0
  #   r = 0
  #   while r < self.rows:
  #     c = 0
  #     while c < self.cols:
  #       if self.grid[r][c].is_covered:
  #         count += 1
  #       c += 1
  #     r += 1
  #   return count

  # def flagged_count(self):
  #   count = 0
  #   r = 0
  #   while r < self.rows:
  #     c = 0
  #     while c < self.cols:
  #       if self.grid[r][c].flagged:
  #         count += 1
  #       c += 1
  #     r += 1
  #   return count

  # def mine_count(self):
  #   count = 0
  #   r = 0
  #   while r < self.rows:
  #     c = 0
  #     while c < self.cols:
  #       if self.grid[r][c].is_mine:
  #         count += 1
  #       c += 1
  #     r += 1
  #   return count

  # def get_info(self):
  #   """return board info for UI"""
  #   cells = []
  #   r = 0
  #   while r < self.rows:
  #     row_list = []
  #     c = 0
  #     while c < self.cols:
  #       cell = self.grid[r][c]
  #       row_list.append(
  #         {
  #           "covered": cell.is_covered,
  #           "flagged": cell.flagged,
  #           "is_mine": cell.is_mine,
  #           "neighbor_count": cell.neighbor_count,
  #         }
  #       )
  #       c += 1
  #     cells.append(row_list)
  #     r += 1
  #   return {
  #     "rows": self.rows,
  #     "cols": self.cols,
  #     "cells": cells,
  #     "covered_count": self.covered_count(),
  #     "flagged_count": self.flagged_count(),
  #     "mine_count": self.mine_count(),
  #   }


### USAGE ###
"""
# create board
board = BoardManager(10, 10)

# place mines exclusing (x,y) for first click safety
bm.place_unique_mines(10, exclude=(x, y))))

# flood reveal neighbors
for nr, nc in bm.neighbors(row, col):
    if bm.cell(nr, nc).is_covered and not bm.cell(nr, nc).is_mine:
        bm.uncover(nr, nc)

# clean reset
board.reset()

# get board info for UI
info = board.get_info()


"""
