"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY],
        [EMPTY, EMPTY, EMPTY],
    ]


def player(board):
    """
    Returns player who has the next turn on a board.
    X starts first. Players alternate.
    """
    count_x = sum(cell == X for row in board for cell in row)
    count_o = sum(cell == O for row in board for cell in row)
    return X if count_x == count_o else O


def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    An action is any EMPTY cell.
    """
    return {(i, j) for i in range(3) for j in range(3) if board[i][j] is EMPTY}


def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    Does NOT modify the original board (deep copy).
    Raises an exception if action is invalid.
    """
    if action is None or len(action) != 2:
        raise ValueError("Invalid action")

    i, j = action

    if not (0 <= i < 3 and 0 <= j < 3):
        raise ValueError("Action out of bounds")

    if board[i][j] is not EMPTY:
        raise ValueError("Cell is not empty")

    new_board = copy.deepcopy(board)
    new_board[i][j] = player(board)
    return new_board


def winner(board):
    """
    Returns the winner of the game, if there is one (X, O, or None).
    """
    # rows
    for i in range(3):
        if board[i][0] is not EMPTY and board[i][0] == board[i][1] == board[i][2]:
            return board[i][0]

    # columns
    for j in range(3):
        if board[0][j] is not EMPTY and board[0][j] == board[1][j] == board[2][j]:
            return board[0][j]

    # diagonals
    if board[0][0] is not EMPTY and board[0][0] == board[1][1] == board[2][2]:
        return board[0][0]

    if board[0][2] is not EMPTY and board[0][2] == board[1][1] == board[2][0]:
        return board[0][2]

    return None


def terminal(board):
    """
    Returns True if game is over, False otherwise.
    Game is over if someone won or if no EMPTY cells remain (tie).
    """
    if winner(board) is not None:
        return True

    return all(cell is not EMPTY for row in board for cell in row)


def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    Assumes it will be called only on a terminal board.
    """
    w = winner(board)
    if w == X:
        return 1
    if w == O:
        return -1
    return 0


def minimax(board):
    """
    Returns the optimal action for the current player on the board
    using Minimax with Alpha-Beta Pruning.
    """
    if terminal(board):
        return None

    turn = player(board)

    def max_value(b, alpha, beta):
        if terminal(b):
            return utility(b)
        v = -math.inf
        for a in actions(b):
            v = max(v, min_value(result(b, a), alpha, beta))
            alpha = max(alpha, v)
            if beta <= alpha:
                break  # Beta cut-off
        return v

    def min_value(b, alpha, beta):
        if terminal(b):
            return utility(b)
        v = math.inf
        for a in actions(b):
            v = min(v, max_value(result(b, a), alpha, beta))
            beta = min(beta, v)
            if beta <= alpha:
                break  # Alpha cut-off
        return v

    best_action = None

    if turn == X:
        best_score = -math.inf
        alpha = -math.inf
        beta = math.inf
        for a in actions(board):
            score = min_value(result(board, a), alpha, beta)
            if score > best_score:
                best_score = score
                best_action = a
            alpha = max(alpha, best_score)
    else:
        best_score = math.inf
        alpha = -math.inf
        beta = math.inf
        for a in actions(board):
            score = max_value(result(board, a), alpha, beta)
            if score < best_score:
                best_score = score
                best_action = a
            beta = min(beta, best_score)

    return best_action
