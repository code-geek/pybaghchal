from Board import Board
from Engine import Engine

from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()


class Position(BaseModel):
    position: str


def get_board(position):
    """
    Return True if the board position is valid.
    """

    # given a FEN create a board
    try:
        board = Board(position=position)
    except:
        return False

    return board


def is_winner(board):
    """
    Return True if the board position already has a winner.
    """

    # check if the board position is a winner
    if board.winner:
        return board.winner.name

    return False


def board_position_after_best_move(board):
    """
    Return the best move for the current player given the board position.
    """

    # find the best move
    engine = Engine(board)
    move = engine.get_best_move()

    # make the best move on the board
    board.make_move(move)

    # return FEN from the board
    return board.position


@app.post("/api/v1/position/")
def play(position: Position):
    board = get_board(position.position)
    if not board:
        return {"error": "Invalid position"}

    if is_winner(board):
        return {"winner": is_winner(board), "new_position": None}

    new_position = board_position_after_best_move(board)
    return {"new_position": new_position}
