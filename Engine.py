from collections import namedtuple
from Point import Point
from Board import Board


class Engine(object):
    """
    Takes a board position and returns the best move
    """

    Move = namedtuple('Move', ['f', 't'])

    def __init__(self, position=None):
        super(Engine, self).__init__()
        self.board = Board(position)

    def _placements(self):
        return [
            Engine.Move(point.index, point.index)
            for point in self.board.points
            if point.get_state() == Point.State.E
        ]

    def _movements(self):
        """
        Returns the possible movements (excluding captures)
        for the board and the turn
        """

        # since we don't have goat positions, we just loop to find the goats
        if self.board.turn == Board.Player.G:
            pieces = [p.index for p in self.board.points if p.get_state() == Point.State.G]
        else:
            pieces = self.board.tigerPos

        return [
            Engine.Move(p, p + d)
            for p in pieces
            for d in Board.directions
            if self.board.is_movable(p, p + d)
        ]

    def _captures(self):
        return [
            Engine.Move(t, t + 2 * d)
            for t in self.board.tigerPos
            for d in Board.directions
            if self.board.can_capture(t, t + 2 * d)
        ]

    def movable_tigers(self):
        """
        Returns the number of movable tigers on the board
        """

        return sum(self.board._tiger_moves())

    def generate_move_list(self):
        """
        Generate a list of all moves for the board and turn
        """

        move_list = []

        # turn = Goat
        if self.board.turn == Board.Player.G:
            # placement phase
            if self.board.goatsToBePlaced > 0:
                move_list.extend(self._placements())
            # movement phase
            else:
                move_list.extend(self._movements())

        # turn = Tiger
        else:
            # moves
            move_list.extend(self._movements())
            # captures
            move_list.extend(self._captures())

        return move_list

    def minmax():
        pass

    def best_move():
        pass
