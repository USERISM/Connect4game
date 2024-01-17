from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, emit
import subprocess
from flask import request
import math
import random

app = Flask(__name__)
socketio = SocketIO(app)

# Apply CORS specifically for SocketIO
socketio.init_app(app, cors_allowed_origins="http://localhost:3001")







import copy

class ConnectFourBoard:
    def __init__(self):
        self.board = [[' ' for _ in range(7)] for _ in range(6)]
        self.player = 1
        self.winner = None

    def resetBoard(self):
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
            socketio.emit('etat',"win1")
            return True
        elif self.win('O'):
            print("Player 2 wins! congrats!!")
            socketio.emit('etat',"win2")
            return True
        elif len(self.getPossibleMoves()) == 0 and not self.win('X') and not self.win('O'):
            print("Draw!!")
            socketio.emit('etat',"draw")
            return True
        else:
            return False
    def gameOver1(self):
        if self.win('X'):
            return True
        elif self.win('O'):
            return True
        elif len(self.getPossibleMoves()) == 0 and not self.win('X') and not self.win('O'):
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

class Node:
    def __init__(self, board, move=None, parent=None):
        self.board = board
        self.move = move
        self.parent = parent
        self.children = []
        self.untried_moves = board.getPossibleMoves()
        self.wins = 0
        self.visits = 0

    def selectChild(self):
        exploration_constant = 1.41  # You can adjust this constant based on your preference
        best_child = None
        best_score = float("-inf")

        for child in self.children:
            if child.visits == 0:
                return child

            ucb1 = child.wins / child.visits + exploration_constant * math.sqrt(
                math.log(self.visits) / child.visits
            )

            if ucb1 > best_score:
                best_score = ucb1
                best_child = child

        return best_child

    def addChild(self, move, board):
        child = Node(board, move, self)
        self.untried_moves.remove(move)
        self.children.append(child)
        return child

    def getBestChild(self):
        return max(self.children, key=lambda c: c.visits)

    def update(self, win, score):
        self.visits += 1
        if win:
            self.wins += 1
        # Update other statistics based on the simulation result



class Play:
    def __init__(self):
        self.board = ConnectFourBoard()
        self.current_player = 1
        self.selected_column = None

    def switchPlayer(self):
        self.current_player = 3 - self.current_player  
        

    def humanTurn(self, col):
        self.board.makeMove(col, 'X')
        self.board.drawBoard()
        if self.board.gameOver():
            return
        self.computerTurn()
        ##############################################################################
    def CarlosTurn(self):
        print("Player 1 (O) is thinking...")
        col = self.MonteCarlo(self.board, 1000)
        self.board.makeMove(col, 'X')
        socketio.emit('player1Move', {'col': col})
        self.board.drawBoard()
        self.switchPlayer()

    def MonteCarlo(self, board, iterations):
        root = Node(board)

        for i in range(iterations):
            node = root
            temp_board = copy.deepcopy(board)

            # Selection phase
            while node.untried_moves == [] and node.children:
                node = node.selectChild()
                temp_board.makeMove(node.move[1], 'X')

            # Expansion phase
            if node.untried_moves:
                random_move = random.choice(node.untried_moves)
                column_to_play = random_move[1]
                temp_board.makeMove(column_to_play, 'X')
                node = node.addChild(random_move, temp_board)

            # Simulation phase with defensive strategy
            while not temp_board.gameOver2():
                possible_moves = temp_board.getPossibleMoves()

                # Implement a more strategic simulation, prioritize blocking opponent's wins
                best_defensive_move = self.getBestDefensiveMove(temp_board)
                if best_defensive_move:
                    temp_board.makeMove(best_defensive_move, 'X')
                else:
                    random_move = random.choice(possible_moves)
                    temp_board.makeMove(random_move[1], 'X')

            # Backpropagation phase
            while node:
                node.update(temp_board.gameOver1(), temp_board.heuristicEval())
                node = node.parent

        best_child = root.getBestChild()
        return best_child.move[1]

    def getBestDefensiveMove(self, board):
        possible_moves = board.getPossibleMoves()

        # Check if any move can block the opponent from winning
        for _, col in possible_moves:
            temp_board = copy.deepcopy(board)
            temp_board.makeMove(col, 'X')
            if temp_board.gameOver1():
                return col

        return None
    

    def computerTurn(self):
        col = self.MinimaxAlphaBetaPruning(self.board, 5, float('-inf'), float('inf'), False)
        self.board.makeMove(col, 'O')
        socketio.emit('player2Move', {'col': col})
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
                self.CarlosTurn()
            else:
                print('robot turn')
                self.computerTurn()

            if self.board.gameOver():
                break    
    

    # def set_clicked_column(self, col):
    #     self.clicked_column = col

    # def play_turn(self):
    #     # Use the stored clicked column
    #     while True:
    #         if self.clicked_column is not None:
    #             col = self.clicked_column
    #             if self.current_player == 1:
    #                 self.humanTurn(col)
    #             else:
    #                 print("computer turn")
    #                 self.computerTurn()

    #             if self.board.gameOver():
    #                 break

    #             self.clicked_column = None  # Reset clicked column for the next move
    #             break  # Exit the loop for the next turn
play = Play()
@socketio.on('positionClicked')
def handle_position_clicked(data):
    col = data['col']  # Extract the column index from the event data
    print('Received column:', col)
    #play.set_clicked_column(col)
    play.humanTurn(col)



@socketio.on('refreshServer')
def handle_refresh_server():
     # Perform actions to refresh the server or execute specific tasks
     print("Received refreshServer event. Refreshing server...")
     #subprocess.run(["python", "serverMARALMALYON.py"])
     play.board.resetBoard()

@socketio.on('startComputerVsMonteCarlo')
def handle_start_computer_vs_monte_carlo():
    print('Starting Computer vs Monte Carlo game...')
    play.board.resetBoard()  # You may need to add a reset_game function in your Play class
    play.playGame()  # Start with the computer's turn


# @app.route('/reset_game', methods=['POST'])
# def reset_game():
#     # Reset game state or perform necessary actions here
#     return "Game reset successfully"

if __name__ == "__main__":
    socketio.run(app, debug=True, port=8080)
