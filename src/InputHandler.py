import pygame
import enum
from GameLogic import GameLogic, GameState, Cell

# enum to handle the type of response given by the input handler
class ResponseCode(enum.Enum):
    Finished = 0
    Failed = 1
    InProgress = 2
    Ignored = 3

# response object designed to package and send input handling results
class Response:
    def __init__(self, game, response_code, message=''):
        self.game: GameLogic = game
        self.response_code: ResponseCode = response_code
        self.message: str = message

# input handler class for handling both keyboard inputs and mouse click inputs
class InputHandler:
    # Keyboard input handling
    # Will be used at the beginning of the game when user enters number of mines
    def handle_keyboard_input(self, game, event, text):
        if game.state != GameState.Start:
            return Response(game, ResponseCode.Ignored, "Game must be in starting state")
        #if keyboard input
        if event.type == pygame.KEYDOWN:
            #if enter (user is done typing)
            if event.key == pygame.K_RETURN:
                if text.isdigit():
                    mines = int(text)
                    if 10 <= mines <= 20:
                        game.set_mines(mines)
                        return Response(game, ResponseCode.Finished, f"Set {mines} mines")
                    else:
                        return Response(game, ResponseCode.Failed, "Mine count must be between 10 and 20")
                else:
                    return Response(game, ResponseCode.Failed, "Input must be a number between 10 and 20")
            #if backspace
            elif event.key == pygame.K_BACKSPACE:
                text = text[:-1]
                return Response(game, ResponseCode.InProgress, text)
            else:
                text += event.unicode
                return Response(game, ResponseCode.InProgress, text)
        return Response(game, ResponseCode.Ignored, "Ignored irrelevant input")

    # Function to handle mouse clicks
    # This will be used to handle cell clearing, cell flagging, and resetting
    def handle_click(self, game, event, x, y):
        if game.state != GameState.Playing:
            return Response(game, ResponseCode.Ignored, "Game must be in progress")
        if event.type == pygame.MOUSEBUTTONDOWN:
            if game.valid_position:
                # if left click -> uncover mine
                if event.button == 1:
                    game.uncover_cell(row=y, col=x)
                    return Response(game, ResponseCode.Finished, f"Uncovered cell at ({x}, {y})")
                # if right click -> toggle flag
                elif event.button == 3:
                    game.toggle_flagged_cell(row=y, col=x)
                    return Response(game, ResponseCode.Finished, f"Toggled flag at ({x}, {y})")
                else:
                    return Response(game, ResponseCode.Ignored, "Ignored irrelevant input")
            else:
                return Response(game, ResponseCode.Ignored, "Click out of range")
        else:
            return Response(game, ResponseCode.Ignored, "Ignored irrelevant input")


# The following code is temporary and is used for testing

# stub for BoardManager
type Board = list[list[Cell]]

board = []
for _ in range(10):
    row = []
    for _ in range(10):
        row.append(Cell())
    board.append(row)

game = GameLogic(board)

#Simple pygame instance to test the clicking handling
def test_click_input():
    pygame.init()
    SCREEN_LENGTH=500
    SCREEN_WIDTH=500
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_LENGTH))

    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    GRAY = (200, 200, 200)
    GRID_SIZE = 50
    GRID_COLOR = GRAY
    running = True
    input_handler = InputHandler()
    game.state=GameState.Playing
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                response = input_handler.handle_click(game, event)
                print(response.message)

        screen.fill(BLACK)

        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(screen, GRID_COLOR, (x, 0), (x, SCREEN_LENGTH))
        for y in range(0, SCREEN_LENGTH, GRID_SIZE):
            pygame.draw.line(screen, GRID_COLOR, (0, y), (SCREEN_WIDTH, y))

        pygame.display.flip()

    pygame.quit()

#Simple pygame instance to check the keyboard input handling
def test_keyboard_input():
    pygame.init()
    SCREEN_LENGTH = 500
    SCREEN_WIDTH = 500
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_LENGTH))
    font = pygame.font.Font(None, 48)
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    input_handler = InputHandler()
    text = ""
    message=""
    clock = pygame.time.Clock()
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            else:
                response = input_handler.handle_keyboard_input(game, event, text)
                print(response.message)
                if response.response_code == ResponseCode.Finished:
                    text = ""
                    message = response.message
                elif response.response_code == ResponseCode.InProgress:
                    text = response.message
                    message = ""
                elif response.response_code == ResponseCode.Failed:
                    message = response.message
        screen.fill(WHITE)
        text_surface = font.render(text, True, BLACK)
        error_surface = font.render(message, True, BLACK)
        screen.blit(text_surface, (50, 200))
        screen.blit(error_surface, (50, 300))

        pygame.display.flip()
        clock.tick(60)
    pygame.quit()


#test_click_input()
test_keyboard_input()
        
        
