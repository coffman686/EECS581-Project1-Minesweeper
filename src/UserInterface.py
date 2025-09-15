

import pygame
import enum

### TESTING ###
class GameState(enum.Enum):
  Start = 0
  Playing = 1
  EndWin = 2
  EndLose = 3

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

class GameLogic:
  def __init__(self, board):
    self.state: GameState = GameState.Start
    self.total_mines: int = 0
    self.flags_remaining: int = 10
    self.covered_cells: int = 0
    self.board: list[list[Cell]] = board

# stub for BoardManager
type Board = list[list[Cell]]

board = []
for _ in range(10):
  row = []
  for _ in range(10):
    row.append(Cell())
  board.append(row)


state = GameState.Playing
testLogic = GameLogic(board)
#board[0][0].is_mine = True
### TESTING ###


# game variables
SCREEN_WIDTH = 1200
SCREEN_LENGTH = 800
CELL_SIZE = (32,32) # size of assets
DISTANCE_BETWEEN_CELLS = 36 # asset size + 4 pixels for gaps
BOARD_SIZE = 10 # 10 x 10 board
BOARD_DISTANCE_DOWN = 300 # distance from top of screen to board
BOARD_DISTANCE_LEFT = (SCREEN_WIDTH // 2) - (DISTANCE_BETWEEN_CELLS*(BOARD_SIZE / 2)) # center of screen - half of total board length


# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED   = (200, 50, 50)


# initialize ui
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_LENGTH))
pygame.display.set_caption("MineSweeper")
screen.fill("white") 
clock = pygame.time.Clock()

# fonts
title_font = pygame.font.SysFont("arialblack", 60)
mine_count_font = pygame.font.SysFont("arialblack", 15)
win_loss_font = pygame.font.SysFont("arialblack", 30)

# function to load all assets in assets folder into a dict that scores path to png
def load_assets():
    assets = {}
    pngs = ["tile", "unexplored_tile", "mine", "flagged_tile", "exploding_mine", "0", "1", "2", "3", "4", "5", "6", "7", "8", "9"]
    for png in pngs:
        path = f"user_interface/assets/{png}.png"
        asset = pygame.image.load(path)
        asset = pygame.transform.scale(asset, CELL_SIZE) # resize asset to cell size
        assets[png] = asset
    return assets

# iterate through game board to render 10 x 10 grid on screen
def render_board():
    
    y = BOARD_DISTANCE_DOWN

    for row in range(10):
        x = BOARD_DISTANCE_LEFT
        for col in range(10):

            # render all uncovered mines on game start
            if state.name == "Start":
                screen.blit(assets["unexplored_tile"], (x,y))

            else:
                # flagged = True -> render flagged tile asset
                if board[row][col].flagged:
                    screen.blit(assets["flagged_tile"], (x,y))
                # is_covered = True -> render unexplored tile
                elif board[row][col].is_covered: 
                    screen.blit(assets["unexplored_tile"], (x,y))

                # NOTE: This assumes that if neighbor_count is 0, then that cell is not an uncovered cell adjacent to a covered cell
                # In other words, if neighbor_count is > 0, I am assuming it will render as a number cell, not an explored cell
                # if cell has neighboring bombs, display # of bombs
                elif board[row][col].neighbor_count > 0:
                    num = str(board[row][col].neighbor_count) # sets num to str of asset name for number of neighboring mines
                    screen.blit(assets[num], (x,y)) # need to account for all nums

                # is_covered = False -> render explored tile
                elif not board[row][col].is_covered:
                    screen.blit(assets["tile"], (x,y))
                
                # win or lose game, reveal all bombs
                if state.name == "EndLose" or state.name == "EndWin":
                    if board[row][col].is_mine: 
                        screen.blit(assets["tile"], (x,y)) # reset to blank tile 
                        screen.blit(assets["mine"], (x,y)) # add mine over tile
            
            x += DISTANCE_BETWEEN_CELLS
        
        y += DISTANCE_BETWEEN_CELLS

             
def coords_to_index(coords):
    x_start = BOARD_DISTANCE_LEFT
    y_start = BOARD_DISTANCE_DOWN

    x_click, y_click = coords

    row = int((x_click - x_start) // DISTANCE_BETWEEN_CELLS)
    col = int((y_click - y_start) // DISTANCE_BETWEEN_CELLS)

    # if clicked within grid return coords
    if 0 <= row <= 9 and 0 <= col <= 9:
        return(row, col)
    

def draw_title():
    title_text = "Minesweeper"
    
    title_surface = title_font.render(title_text, True, RED)
    shadow_surface = title_font.render(title_text, True, BLACK) # shadow for added effect

    title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 90))
    shadow_rect = shadow_surface.get_rect(center=(SCREEN_WIDTH // 2 + 2, 92))  # slight offset for shadow

    screen.blit(shadow_surface, shadow_rect)
    screen.blit(title_surface, title_rect)


def update_mine_counter():
    text = f"Mines Remaining: {testLogic.flags_remaining}"

    mine_counter = mine_count_font.render(text, True, BLACK)
    mine_counter_rect = mine_counter.get_rect(center=(SCREEN_WIDTH // 2, 175))

    pygame.draw.rect(screen, WHITE, mine_counter_rect, 10)

    screen.blit(mine_counter, mine_counter_rect)


def render_win_or_loss():
    if state.name == "EndLose":
       text = "YOU LOSE :("
    elif state.name == "EndWin":
       text = "YOU WIN :)"
    else:
       return

    result = win_loss_font.render(text, True, BLACK)
    result_rect = result.get_rect(center=(SCREEN_WIDTH // 2, 250))
    screen.blit(result, result_rect)

def render_ui():
    # reset screen with updated ui
    screen.fill(WHITE)              
    draw_title()
    render_board()
    update_mine_counter()
    render_win_or_loss()

# INITIALIZE GAME
draw_title()
update_mine_counter()
assets = load_assets()
render_board()


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1: # left click
            # NOTE: send click type and coords to input handler
            print(f"Left click at: {coords_to_index(event.pos)}")
            # after input is sent and handled, render board, update mine counter, check for win/loss
            render_ui()

            
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3: # right click
            # NOTE: send click type and coords to input handler
            print(f"Right click at: {coords_to_index(event.pos)}")
            # after input is sent and handled, render board, update mine counter, check for win/loss
            render_ui()
            


    pygame.display.flip()
    clock.tick(60)




pygame.quit()
