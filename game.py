import random

class Game():
    def __init__(self):
        self.board = [""] * 9
        self.current_player = "X"
        self.turn = ["X", "O"]
        self.players = {}
        self.player_count = 0
        self.bot_enable = False
        self.wining_combinations = [
                (0, 1, 2),
                (3, 4, 5),
                (6, 7, 8),
                (0, 3, 6),
                (1, 4, 7),
                (2, 5, 8),
                (0, 4, 8),
                (2, 4, 6)
        ]

    def move_position(self, position):
        if 0<= position < 9:
                if self.board[position] == "":
                        self.board[position] = self.current_player
                        response = self.check_winner()
                        if response:
                                return response
                        if all(self.board):
                                return {
                                       "status": "draw",
                                       "msg": "game draw!"
                                }
                        if self.current_player == self.turn[0]:
                                            self.current_player = self.turn[1]
                        else: self.current_player = self.turn[0]
                else:
                       return {
                              "status": "wrong",
                              "msg": "position already occupied"
                       }
        else:
              return {
                     "status": "wrong",
                     "msg": "invalid position"
              }

    def check_winner(self):
        for a, b, c in self.wining_combinations:
                if self.board[a] != "" and self.board[a] == self.board[b] == self.board[c]:
                        return {"status": "win",
                                "msg": f"player {self.board[a]} is winner"
                               }


    def reset_board(self):
        self.board = [""] * 9


    def bot_move(self):
        opposite_corner = {
               0:8,
               2:6,
               6:2,
               8:0
        }
        side = [1, 3, 5, 7]
        
        empty_position = [
                i for i, cell in enumerate(self.board)
                if cell==""
                ]
        for pos in empty_position:
                
                self.board[pos] = "O"
                if self.check_winner():
                      self.board[pos] = ""
                      return self.move_position(pos)
                
                self.board[pos] = "X"
                if self.check_winner():
                        self.board[pos] = ""
                        return self.move_position(pos)
                self.board[pos] = ""
        
        if self.board[4] == "":
               return self.move_position(4)

        
        
        for corner, opposite in opposite_corner.items():
               if self.board[corner] == "X"and self.board[opposite] == "X" and self.board[4] == "O":
                      for s in side:
                             if self.board[s] == "":
                                    return self.move_position(s)
        for corner, opposite in opposite_corner.items():
                if self.board[corner] == "":
                        return self.move_position(corner)
        position = random.choice(empty_position)
        return self.move_position(position)



