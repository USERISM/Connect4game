import copy

class ConnectFourBoard:
    def __init__(self):
        self.board = [[' ' for _ in range(7)] for _ in range(6)]
        self.player = 1
        self.winner = None

    def drawBoard(self):
        for row in self.board:
            print('|'.join(row))
        print('-' * 29)

    def getPossibleMoves(self):
        empty_spots = []
        for row in range(len(self.board)):
            for col in range(len(self.board[row])):
                if self.board[row][col] == ' ':
                    empty_spots.append((row, col))
        return empty_spots

    def makeMove(self, col, piece):
        possible_moves = self.getPossibleMoves()
    
        if col < 0 or col >= 7 or (0, col) not in possible_moves:
            print("Invalid move.")
            return

        for row in range(5, -1, -1):
            if self.board[row][col] == ' ':
                self.board[row][col] = piece
                break

    def win(self, piece):
        # rows
        for row in range(len(self.board)):
            for col in range(len(self.board[row]) - 3):
                if self.board[row][col] == piece and self.board[row][col + 1] == piece and self.board[row][col + 2] == piece and self.board[row][col + 3] == piece:
                    return True

        # columns
        for col in range(len(self.board[0])):
            for row in range(len(self.board) - 3):
                if self.board[row][col] == piece and self.board[row + 1][col] == piece and self.board[row + 2][col] == piece and self.board[row + 3][col] == piece:
                    return True

        #diag top left down right
        for row in range(len(self.board) - 3):
            for col in range(len(self.board[row]) - 3):
                if self.board[row][col] == piece and self.board[row + 1][col + 1] == piece and self.board[row + 2][col + 2] == piece and self.board[row + 3][col + 3] == piece:
                    return True

        # diah l3ks
        for row in range(len(self.board) - 3):
            for col in range(3, len(self.board[row])):
                if self.board[row][col] == piece and self.board[row + 1][col - 1] == piece and self.board[row + 2][col - 2] == piece and self.board[row + 3][col - 3] == piece:
                    return True

        return False


    def gameOver(self):
        if self.win('X'):
            print("Player 1 wins! congrats!!")
            return True
        elif self.win('O'):
            print("Player 2 wins! congrats!!")
            return True
        elif len(self.getPossibleMoves()) == 0 and not self.win('X') and not self.win('O'):
            print("Draw!!")
            return True
        else:
            return False
        
    def gameOver2(self):
        if self.win('X') or self.win('O') or len(self.getPossibleMoves()) == 0:
            return True
        else:
            return False


    def heuristicEval(self):
        score = 0

        for row in self.board:
            score += self.checking(row)

        for col in range(7):
            column = [self.board[row][col] for row in range(6)]
            score += self.checking(column)

        # Check diags
        for row in range(3):
            for col in range(4):
                diagonal = [self.board[row+i][col+i] for i in range(4)]
                score += self.checking(diagonal)

                diagonal = [self.board[row+3-i][col+i] for i in range(4)]
                score += self.checking(diagonal)

        return score

    def checking(self, thing):
        if thing.count('O') == 4:
            return 100  # ai yrbh
        elif thing.count('O') == 3 and thing.count(' ') == 1:
            return 10   # blk ai yrbh
        elif thing.count('O') == 2 and thing.count(' ') == 2:
            return 1  
        elif thing.count('X') == 4:
            return -100  # ana nrbh
        elif thing.count('X') == 3 and thing.count(' ') == 1:
            return -10  
        elif thing.count('X') == 2 and thing.count(' ') == 2:
            return -1  
        else:
            return 0    


class Play:
    def __init__(self):
        self.board = ConnectFourBoard()
        self.current_player = 1  

    def switchPlayer(self):
        self.current_player = 3 - self.current_player  

    def humanTurn(self):
        col = int(input("Player {} ({}): Enter column (0-6): ".format(self.current_player, 'X')))
        while col < 0 or col >= 7 or (0, col) not in self.board.getPossibleMoves():
            print("Invalid column. Try again.")
            col = int(input("Player {} ({}): Enter column (0-6): ".format(self.current_player, 'X')))
        
        self.board.makeMove(col, 'X')
        self.board.drawBoard()
        self.switchPlayer() 

    def computerTurn(self):
        print("Player 2 (O) is thinking...")
        col = self.MinimaxAlphaBetaPruning(self.board, 5, float('-inf'), float('inf'), False)
        print(f"Player 2 (O) chooses column {col}")
        self.board.makeMove(col, 'O')
        self.board.drawBoard()
        self.switchPlayer() 

    def MinimaxAlphaBetaPruning(self, board, depth, alpha, beta, maximizingPlayer):
        if depth == 0 or board.gameOver2():
            return board.heuristicEval() 

        possible_moves = board.getPossibleMoves()

        if maximizingPlayer:  #y3ni max li hwa AI
            max_eval = float('-inf')
            best_col = possible_moves[0][1] 

            for _, col in possible_moves:
                new_board = copy.deepcopy(board)   #ndiro copy ela board to simulate the actions li y9dr ydirhm bch nhsbo lwsmo
                new_board.makeMove(col, 'O')  
                eval = self.MinimaxAlphaBetaPruning(new_board, depth - 1, alpha, beta, False)
                
                if eval > max_eval:
                    max_eval = eval
                    best_col = col

                alpha = max(alpha, eval)
                if beta <= alpha:
                    break  

            return best_col
        else:
            min_eval = float('inf')
            best_col = possible_moves[0][1]  

            for _, col in possible_moves:
                new_board = copy.deepcopy(board) 
                new_board.makeMove(col, 'X')  
                eval = self.MinimaxAlphaBetaPruning(new_board, depth - 1, alpha, beta, True)
                
                if eval < min_eval:
                    min_eval = eval
                    best_col = col

                beta = min(beta, eval)
                if beta <= alpha:
                    break  

            return best_col

    def playGame(self):
        self.board.drawBoard()

        while True:
            if self.current_player == 1:
                self.humanTurn()
            else:
                self.computerTurn()

            if self.board.gameOver():
                break

            # self.switchPlayer()


if __name__ == "__main__":
    play = Play()
    play.playGame()

