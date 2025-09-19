"""
PROLOGUE
Module: InputHandler
Description: Contains InputHandler class with functions that handle user clicks and keyboard
             inputs and returns updated game state and the type of response that was given
Inputs: None
Outputs: None
External Sources: n/a
Created At: 9/10/2025 by Sam Suggs
"""

# Import required libraries and classes
import pygame
import enum
from GameLogic import GameLogic, GameState

# enum class to handle the type of response given by the input handler
class ResponseCode(enum.Enum):
    Finished = 0
    Failed = 1
    InProgress = 2
    Ignored = 3

# Response object designed to package and send input handling results
# Inputs: game: GameLogic, response_code: ResponseCode, message: str
class Response:
    def __init__(self, game, response_code, message=''):
        self.game: GameLogic = game
        self.response_code: ResponseCode = response_code
        self.message: str = message

# input handler class for handling both keyboard inputs and mouse click inputs
class InputHandler:
    # Keyboard input handling
    # Will be used at the beginning of the game when user enters number of mines
    # Inputs: game: GameLogic, event: PygameEvent, text: str
    # Output: Response
    def handle_keyboard_input(self, game, event, text):
        # Keyboard inputs will only be accepted at the start of the game
        # (that's when a user will enter the number of mines they want)
        if game.state != GameState.Start:
            return Response(game, ResponseCode.Ignored, "Game must be in starting state")
        #if keyboard input
        if event.type == pygame.KEYDOWN:
            #if enter (user is done typing)
            if event.key == pygame.K_RETURN:
                # verify that the input is a number
                if text.isdigit():
                    # convert to int
                    mines = int(text)
                    # if it's a legal amount of mines, update the game object
                    if 10 <= mines <= 20:
                        game.set_mines(mines)
                        return Response(game, ResponseCode.Finished, f"Set {mines} mines")
                    # otherwise return error response
                    else:
                        return Response(game, ResponseCode.Failed, "Mine count must be between 10 and 20")
                # otherwise return error response
                else:
                    return Response(game, ResponseCode.Failed, "Input must be a number between 10 and 20")
            #if backspace
            elif event.key == pygame.K_BACKSPACE:
                # remove the last character from the text string
                text = text[:-1]
                # return response object including updated text
                return Response(game, ResponseCode.InProgress, text)
            else:
                # add input to text variable and return it in a response
                text += event.unicode
                return Response(game, ResponseCode.InProgress, text)
        # return ignored response if input is not a keyboard input
        return Response(game, ResponseCode.Ignored, "Ignored irrelevant input")

    # Function to handle mouse clicks
    # This will be used to handle cell clearing, cell flagging, and resetting
    # Inputs: game: GameLogic, event: PygameEvent, x: int, y: int
    # Output: Response
    def handle_click(self, game, event, x, y):
        # Click inputs will only be handled when the game is in progress
        if game.state != GameState.Playing:
            return Response(game, ResponseCode.Ignored, "Game must be in progress")
        # if the event was a mouse click
        if event.type == pygame.MOUSEBUTTONDOWN:
            # if left click -> uncover mine
            if event.button == 1:
                game.uncover_cell(row=y, col=x)
                 # return updated game
                return Response(game, ResponseCode.Finished, f"Uncovered cell at ({x}, {y})")
            # if right click -> toggle flag
            elif event.button == 3:
                game.toggle_flagged_cell(row=y, col=x)
                # return updated game
                return Response(game, ResponseCode.Finished, f"Toggled flag at ({x}, {y})")
            # if not a valid mouse click, return ignored response
            else:
                return Response(game, ResponseCode.Ignored, "Ignored irrelevant input")
        # if not a click, return ignored response
        else:
            return Response(game, ResponseCode.Ignored, "Ignored irrelevant input")