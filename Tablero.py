from collections import defaultdict
import math

infinity = math.inf
expansiones = 0

class Game:
    def actions(self, state):
        raise NotImplementedError

    def result(self, state, move):
        raise NotImplementedError

    def is_terminal(self, state):
        return not self.actions(state)

    def utility(self, state, player):
        raise NotImplementedError

class Board(defaultdict):
    empty = '.'
    off = '#'

    def __init__(self, width=8, height=8, to_move=None, squares=None, **kwds):
        self.__dict__.update(width=width, height=height, to_move=to_move, squares=squares or {}, **kwds)

    def new(self, changes: dict, **kwds) -> 'Board':
        board = Board(width=self.width, height=self.height, squares=self.squares.copy(), **kwds)
        board.update(self)
        board.update(changes)
        return board

    def __missing__(self, loc):
        x, y = loc
        if 0 <= x < self.width and 0 <= y < self.height:
            return Board.empty
        else:
            return Board.off

    def __hash__(self):
        return hash(tuple(sorted(self.items()))) + hash(self.to_move)

    def __repr__(self):
        def row(y): return ' '.join(self[x, y] for x in range(self.width))
        return '\n'.join(map(row, range(self.height))) + '\n'

class Chess(Game):
    def __init__(self):
        self.squares = {(x, y) for x in range(8) for y in range(8)}
        self.initial = Board(width=8, height=8, to_move='W', squares=self.squares, utility=0)
        self.initial.update({
            (0, 0): 'R', (1, 0): 'N', (2, 0): 'B', (3, 0): 'Q', (4, 0): 'K', (5, 0): 'B', (6, 0): 'N', (7, 0): 'R',
            (0, 1): 'P', (1, 1): 'P', (2, 1): 'P', (3, 1): 'P', (4, 1): 'P', (5, 1): 'P', (6, 1): 'P', (7, 1): 'P',
            (0, 6): 'p', (1, 6): 'p', (2, 6): 'p', (3, 6): 'p', (4, 6): 'p', (5, 6): 'p', (6, 6): 'p', (7, 6): 'p',
            (0, 7): 'r', (1, 7): 'n', (2, 7): 'b', (3, 7): 'q', (4, 7): 'k', (5, 7): 'b', (6, 7): 'n', (7, 7): 'r'
        })

    def actions(self, board):
        moves = []
        for (x, y), piece in board.items():
            if piece.isupper() and board.to_move == 'W' or piece.islower() and board.to_move == 'B':
                if piece.lower() == 'p':
                    moves.extend(self.pawn_moves(board, x, y, piece))
                elif piece.lower() == 'r':
                    moves.extend(self.rook_moves(board, x, y, piece))
                elif piece.lower() == 'n':
                    moves.extend(self.knight_moves(board, x, y, piece))
                elif piece.lower() == 'b':
                    moves.extend(self.bishop_moves(board, x, y, piece))
                elif piece.lower() == 'q':
                    moves.extend(self.queen_moves(board, x, y, piece))
                elif piece.lower() == 'k':
                    moves.extend(self.king_moves(board, x, y, piece))
        return moves

    def pawn_moves(self, board, x, y, piece):
        moves = []
        direction = -1 if piece.isupper() else 1
        start_row = 6 if piece.isupper() else 1
        new_x, new_y = x, y + direction
        if (new_x, new_y) in board.squares and board[(new_x, new_y)] == board.empty:
            moves.append(((x, y), (new_x, new_y)))
            if y == start_row:
                new_y += direction
                if (new_x, new_y) in board.squares and board[(new_x, new_y)] == board.empty:
                    moves.append(((x, y), (new_x, new_y)))
        for dx in [-1, 1]:
            capture_x, capture_y = x + dx, y + direction
            if (capture_x, capture_y) in board.squares and board[(capture_x, capture_y)] != board.empty and (board[(capture_x, capture_y)].islower() if piece.isupper() else board[(capture_x, capture_y)].isupper()):
                moves.append(((x, y), (capture_x, capture_y)))
        return moves

    def rook_moves(self, board, x, y, piece):
        moves = []
        for dx, dy in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            for i in range(1, 8):
                new_x, new_y = x + i * dx, y + i * dy
                if (new_x, new_y) not in board.squares:
                    break
                if board[(new_x, new_y)] == board.empty:
                    moves.append(((x, y), (new_x, new_y)))
                elif board[(new_x, new_y)].islower() if piece.isupper() else board[(new_x, new_y)].isupper():
                    moves.append(((x, y), (new_x, new_y)))
                    break
                else:
                    break
        return moves

    def knight_moves(self, board, x, y, piece):
        moves = []
        knight_moves = [(2, 1), (1, 2), (-1, 2), (-2, 1), (-2, -1), (-1, -2), (1, -2), (2, -1)]
        for dx, dy in knight_moves:
            new_x, new_y = x + dx, y + dy
            if (new_x, new_y) in board.squares and (board[(new_x, new_y)] == board.empty or (board[(new_x, new_y)].islower() if piece.isupper() else board[(new_x, new_y)].isupper())):
                moves.append(((x, y), (new_x, new_y)))
        return moves

    def bishop_moves(self, board, x, y, piece):
        moves = []
        for dx, dy in [(1, 1), (-1, -1), (1, -1), (-1, 1)]:
            for i in range(1, 8):
                new_x, new_y = x + i * dx, y + i * dy
                if (new_x, new_y) not in board.squares:
                    break
                if board[(new_x, new_y)] == board.empty:
                    moves.append(((x, y), (new_x, new_y)))
                elif board[(new_x, new_y)].islower() if piece.isupper() else board[(new_x, new_y)].isupper():
                    moves.append(((x, y), (new_x, new_y)))
                    break
                else:
                    break
        return moves

    def queen_moves(self, board, x, y, piece):
        return self.rook_moves(board, x, y, piece) + self.bishop_moves(board, x, y, piece)

    def king_moves(self, board, x, y, piece):
        moves = []
        king_moves = [(1, 0), (0, 1), (-1, 0), (0, -1), (1, 1), (-1, -1), (1, -1), (-1, 1)]
        for dx, dy in king_moves:
            new_x, new_y = x + dx, y + dy
            if (new_x, new_y) in board.squares and (board[(new_x, new_y)] == board.empty or (board[(new_x, new_y)].islower() if piece.isupper() else board[(new_x, new_y)].isupper())):
                moves.append(((x, y), (new_x, new_y)))
        return moves

    def result(self, board, move):
        (start_x, start_y), (end_x, end_y) = move
        new_board = board.new({}, to_move=('B' if board.to_move == 'W' else 'W'))
        piece = board[(start_x, start_y)]
        new_board[(end_x, end_y)] = piece
        new_board[(start_x, start_y)] = board.empty
        return new_board

    def utility(self, board, player):
        if self.is_checkmate(board, 'W'):
            return -1 if player == 'W' else 1
        if self.is_checkmate(board, 'B'):
            return 1 if player == 'W' else -1
        return 0

    def is_terminal(self, board):
        return self.is_checkmate(board, 'W') or self.is_checkmate(board, 'B')

    def is_checkmate(self, board, player):
        king_pos = None
        for (x, y), piece in board.items():
            if piece == ('K' if player == 'W' else 'k'):
                king_pos = (x, y)
                break
        if king_pos is None:
            return True
        for move in self.actions(board):
            new_board = self.result(board, move)
            if not self.is_in_check(new_board, player):
                return False
        return True

    def is_in_check(self, board, player):
        king_pos = None
        for (x, y), piece in board.items():
            if piece == ('K' if player == 'W' else 'k'):
                king_pos = (x, y)
                break
        if king_pos is None:
            return True
        opponent = 'B' if player == 'W' else 'W'
        for move in self.actions(board):
            (start, end) = move
            if end == king_pos and (board[start].isupper() if opponent == 'W' else board[start].islower()):
                return True
        return False

    def display(self, board):
        print("  A B C D E F G H")
        for y in range(8):
            row = [board.get((x, y), '.') for x in range(8)]
            print(f"{8 - y} {' '.join(row)}")
        print("  A B C D E F G H")


def play_game(game):
    state = game.initial
    while not game.is_terminal(state):
        game.display(state)
        player = state.to_move
        move = None
        while move not in game.actions(state):
            try:
                start_input = input(f"Jugador {player}, ingrese la coordenada de la pieza (e.g., 'e2'): ")
                end_input = input(f"Jugador {player}, ingrese la coordenada de destino (e.g., 'e4'): ")


                if not (len(start_input) == 2 and len(end_input) == 2 and
                        'a' <= start_input[0] <= 'h' and '1' <= start_input[1] <= '8' and
                        'a' <= end_input[0] <= 'h' and '1' <= end_input[1] <= '8'):
                    print("Coordenadas inválidas. Intente de nuevo.")
                    continue

                start_x, start_y = ord(start_input[0]) - ord('a'), 8 - int(start_input[1])
                end_x, end_y = ord(end_input[0]) - ord('a'), 8 - int(end_input[1])
                move = ((start_x, start_y), (end_x, end_y))

                if move not in game.actions(state):
                    print("Movimiento inválido. Intente de nuevo.")
                    move = None
            except ValueError:
                print("Entrada inválida. Por favor, ingrese el movimiento en el formato 'e2 e4'.")

        state = game.result(state, move)
        game.display(state)
    game.display(state)
    print("GG WP")
play_game(Chess())