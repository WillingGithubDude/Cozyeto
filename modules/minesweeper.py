class Tile:
  def __init__(self, displayValue, value, x_pos, y_pos):
    self.displayValue = displayValue
    self.value = value
    self.position = x_pos, y_pos
    self.revealed = False
  
  def reveal(self, board):
    self.revealed = True
    if self.displayValue != "[₱]":
      if self.value == "X":
        return True
      else:
        if self.value == 0:
          self.displayValue = " "
          self.reveal_neighbors(board)
        else:
          self.displayValue = self.value
  
  def reveal_neighbors(self, board):
    for neighbor in self.get_surroundings(board):
      if neighbor.displayValue != "[₱]" and neighbor.revealed == False:
        if neighbor.reveal(board) == True:
          return True

  def flag(self, board):
    if self.displayValue == "[₱]":
      self.displayValue = "[=]"
      board.change_marker_count("add")
    else:
      self.displayValue = "[₱]"
      board.change_marker_count("sub")

  def set_value(self, value):
    self.value = value

  def get_surroundings(self, board):
    x, y = self.position
    n = len(board)
    surroundings = []
    if (x >=0 and x <= n-2) and (y >= 0 and y <= n-1):
        surroundings.append(board[y][x+1]) # center right
    if (x >=1 and x <= n-1) and (y >= 0 and y <= n-1):
        surroundings.append(board[y][x-1]) # center left
    if (x >= 1 and x <= n-1) and (y >= 1 and y <= n-1):
        surroundings.append(board[y-1][x-1]) # top left
    if (x >= 0 and x <= n-2) and (y >= 1 and y <= n-1):
        surroundings.append(board[y-1][x+1]) # top right
    if (x >= 0 and x <= n-1) and (y >= 1 and y <= n-1):
        surroundings.append(board[y-1][x]) # top center

    if (x >=0 and x <= n-2) and (y >= 0 and y <= n-2):
        surroundings.append(board[y+1][x+1]) # bottom right
    if (x >= 1 and x <= n-1) and (y >= 0 and y <= n-2):
        surroundings.append(board[y+1][x-1]) # bottom left
    if (x >= 0 and x <= n-1) and (y >= 0 and y <= n-2):
        surroundings.append(board[y+1][x]) # bottom center
    return surroundings


class Game:

  def __init__(self, choice):
    dictionary = {
      "1️⃣": {"difficulty": "Beginner", "size": 5, "bombs": 3},
      "2️⃣": {"difficulty": "Easy", "size": 6, "bombs": 8},
      "3️⃣": {"difficulty": "Medium", "size": 7, "bombs": 10},
      "4️⃣": {"difficulty": "Hard", "size": 9, "bombs": 16}
    }
    self.difficulty = dictionary[choice]["difficulty"]
    self.bombs = dictionary[choice]["bombs"]
    self.size = dictionary[choice]["size"]
    self.unmarked_bombs = self.bombs
    self.board = [[Tile("[=]", 0, row, column) for row in range(self.size)] for column in range(self.size)]
  
  def convert(self, character):
    if isinstance(character, str):
      dictionary = {letter: number for number, letter in enumerate('abcdefghijklmnopqrstuvwxyz')}
      return dictionary[character.lower()]
    elif isinstance(character, int):
      dictionary = {number: letter for number, letter in enumerate('abcdefghijklmnopqrstuvwxyz')}
      return dictionary[character]

  def get_board(self, showValues=False, ):
    board_rows = []
    board_len = range((len(self.board)))
    separator = "  -" + ''.join(["------" for amount in board_len])
    board_rows.append(f'     {"     ".join([self.convert(number).upper() for number in board_len])}   ')
    board_rows.append(separator)
    for row_position, row in enumerate(self.board):
      if showValues == False:
        row_values = []
        for tile in row:
          if tile.displayValue in ["[=]", "[₱]"]:
            row_values.append(tile.displayValue)
          else:
            row_values.append(f" {tile.displayValue} ")
        row_values = " | ".join(row_values)
      else:
        row_values = " " + "  |  ".join([str(tile.value) for tile in row]) + " "
      board_rows.append(f'{row_position+1} | {row_values} |')
      board_rows.append(separator)
    return board_rows

  def place_bombs(self, starting_pos):
    import random
    place_bombs = self.bombs
    while place_bombs > 0:
      n = len(self.board)-1
      x = random.randint(0, n)
      y = random.randint(0, n)
      if (self.board[y][x].value !="X") and (starting_pos != {y: x}):
        self.board[y][x].set_value("X")
        for tile in self.board[y][x].get_surroundings(self.board):
          if tile.value != "X":
            tile.set_value(tile.value + 1)
        place_bombs -= 1

  def change_marker_count(self, operation):
    if operation == "add":
      self.unmarked_bombs += 1
    elif operation == "sub":
      self.unmarked_bombs -= 1

  def has_won(self):
    for row in self.board:
      for tile in row:
        if str(tile.displayValue) in ["[₱]", "[=]"]:
          if tile.value != "X":
            return False
    return True

  def play(self, tile: Tile, flag=False):
    if flag == False:
      if tile.displayValue != "[₱]":
        if tile.value == "X":
              return False
        if (tile.value != 0) and (tile.displayValue != "[=]"):
          if tile.reveal_neighbors(self.board) == True:
            return False
        tile.reveal(self.board)
    else:
      if tile.displayValue in ["[=]", "[₱]"]:
        tile.flag(self)
    if self.has_won():
      return True