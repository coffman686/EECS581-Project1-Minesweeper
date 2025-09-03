## Game Flow

To begin the game, the user specifies the number of mines they would like on the board. Once this input is received, the board is displayed, and the system waits for the first user click. Upon receiving a click, the game records the clicked position. If it is the first click, the game initializes the mine locations and cell states, ensuring that the first clicked cell is never a mine. 

If the selected cell is not flagged, the game determines whether the cell contains a mine or has zero nearby mines. If it has zero nearby mines, the system recursively clears all adjacent cells that also have no surrounding mines. After each move, the game checks if the player has successfully revealed all non-mine cells, thereby winning the game. 

If the player wins, a “You win” message is displayed, and the player is given the option to play again. Upon clicking to restart, the game state and board are reset, the board is re-rendered, and the game returns to the waiting-for-click state to continue gameplay.

---

## Key Objects

### Cell
Represents an individual tile on the board and stores all relevant attributes:
- `is_mine`: Indicates if the cell contains a mine.
- `nearby_mines`: The number of mines adjacent to this cell.
- `is_flagged`: Whether the cell has been flagged by the user.

### Game
Manages the overall game logic:
- Stores the board as an array of `Cell` objects.
- Tracks game state, including:
  - Total number of mines.
  - Number of remaining flags.
  - Overall progress.

### GUI
Handles all visual representation and user interaction:
- Displays the game board.
- Stores a reference to the `Game` object.
- Manages rendering and any additional UI elements (e.g., buttons).

<img width="1039" height="883" alt="Untitled Diagram drawio (2)" src="https://github.com/user-attachments/assets/dc2a0d2e-9935-4a22-953c-535eec86cccb" />

