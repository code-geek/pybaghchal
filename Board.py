from collections import namedtuple
from enum import Enum

from Point import Point


class Board(object):
    """A baghchal board"""

    # possible connections from one point to another
    _move_connections = {
        0: [1, 5, 6], 1: [2, 0, 6], 2: [3, 1, 7, 6, 8], 3: [4, 2, 8], 4: [3, 9, 8],
        5: [6, 10, 0], 6: [7, 5, 11, 1, 10, 2, 12, 0], 7: [8, 6, 12, 2], 8: [9, 7, 13, 3, 12, 4, 14, 2], 9: [8, 14, 4],
        10: [11, 15, 5, 6, 16], 11: [12, 10, 16, 6], 12: [13, 11, 17, 7, 16, 8, 18, 6], 13: [14, 12, 18, 8],
        14: [13, 19, 9, 18, 8],
        15: [16, 20, 10], 16: [17, 15, 21, 11, 20, 12, 22, 10], 17: [18, 16, 22, 12],
        18: [19, 17, 23, 13, 22, 14, 24, 12], 19: [18, 24, 14],
        20: [21, 15, 16], 21: [22, 20, 16], 22: [23, 21, 17, 18, 16], 23: [24, 22, 18], 24: [23, 19, 18]
    }

    _capture_connections = {
        0: [2, 10, 12], 1: [3, 11], 2: [4, 0, 12, 10, 14], 3: [1, 13], 4: [2, 14, 12],
        5: [7, 15], 6: [8, 16, 18], 7: [9, 5, 17], 8: [6, 18, 16], 9: [7, 19],
        10: [12, 20, 0, 2, 22], 11: [13, 21, 1], 12: [14, 10, 22, 2, 20, 4, 24, 0],
        13: [11, 23, 3], 14: [12, 24, 4, 22, 2],
        15: [17, 5], 16: [18, 6, 8], 17: [19, 15, 7], 18: [16, 8, 6], 19: [17, 9],
        20: [22, 10, 12], 21: [23, 11], 22: [24, 20, 12, 14, 10], 23: [21, 13], 24: [22, 14, 12]
    }

    class Player(Enum):
        T = 1
        G = 2

        def __str__(self):
            return "Goats" if self.name == "G" else "Tigers"

    class MoveType(Enum):
        P = 1  # Place
        M = 2  # Move
        C = 3  # Capture

        def __repr__(self):
            if self.name == "P":
                return "Place"
            elif self.name == "M":
                return "Move"
            else:
                return "Capture"

        def __str__(self):
            return self.__repr__()

    # f = from, t = to, mt = MoveType
    nt = namedtuple('Move', ['f', 't', 'mt'])

    class Move(nt):
        def __repr__(self):
            return "%s-%s-%s" % (Point.get_coord(self.f), Point.get_coord(self.t), self.mt.name)

    # horizontal (1, -1) # vertical (5, -5) # diagonal (4, -4, 6, -6)
    directions = [1, -1, 5, -5, 4, -4, 6, -6]

    def __init__(self, position=None):
        super(Board, self).__init__()
        # initialize the board to the starting position
        self.reset()

        # parse the position string, if available
        if position:
            self.parse_position(position)
        else:
            self.tigerPos = [0, 4, 20, 24]

            for i in self.tigerPos:
                self.points[i].set_state("T")

    def reset(self):
        """Resets the board"""

        self.points = [Point(i) for i in range(25)]
        self.tigerPos = []
        self.goatsToBePlaced = 20
        self.deadGoats = 0
        self.turn = self.Player.G
        self.lastMove = ""

    def show(self):
        print("""  a   b   c   d   e
1 %s   %s   %s   %s   %s
  | \\ | / | \\ | / |
2 %s   %s   %s   %s   %s
  | / | \\ | / | \\ |
3 %s   %s   %s   %s   %s
  | \\ | / | \\ | / |
4 %s   %s   %s   %s   %s
  | / | \\ | / | \\ |
5 %s   %s   %s   %s   %s\n""" % tuple(i.print_state() for i in self.points))
        print("Turn: %s" % ("Goat" if self.turn == self.Player.G else "Tiger"))
        print("Remaining Goats: %d" % self.goatsToBePlaced)
        print("Dead Goats: %d\n" % self.deadGoats)

    @staticmethod
    def _get_full_position(pos_string):
        """
        get a full position from a shortened position string:
        eg. 1GG1G/1GGGT/GGGGG/1GTGG/GTGTG gives
        list('EGGEGEGGGTGGGGGEGTGGGTGTG')
        """

        full_pos = []
        pos_string = pos_string.upper().split('/')

        for row in pos_string:
            row_pos = []
            for i in row:
                if i == 'G':
                    row_pos.append('G')
                elif i == 'T':
                    row_pos.append('T')
                elif i.isdigit():
                    for j in range(int(i)):
                        row_pos.append('E')
            # check the validity of each row and print invalid rows here
            assert len(row_pos) % 5 == 0, "Invaild row %s. row_pos: %s" % (row, ''.join(row_pos))
            full_pos.extend(row_pos)
        return full_pos

    def parse_position(self, position):
        parts = position.split()
        full_pos = Board._get_full_position(parts[0])
        assert len(full_pos) == 25

        for idx, p in enumerate(full_pos):
            self.points[idx].set_state(p)

        self.turn = self.Player[parts[1].upper()]

        self.goatsToBePlaced = int(parts[2][1:])
        assert (self.goatsToBePlaced in range(21)), "Invalid goatsToBePlaced: %d" % self.goatsToBePlaced

        self.deadGoats = int(parts[3][1:])
        assert (self.deadGoats in range(6)), "Invalid deadGoats: %d" % self.deadGoats

        self.lastMove = parts[4][1:]

        self._set_tiger_positions()

    def _set_tiger_positions(self):
        """
        Finds the tigers on the board and saves their positions
        """

        self.tigerPos = []
        for idx, p in enumerate(self.points):
            if p.get_state() == Point.State.T:
                self.tigerPos.append(idx)
        assert len(self.tigerPos) == 4

    def change_tiger_position(self, f, t):
        """
        Changes a certain tiger's position in self.tigerPos
        """
        pass

    @property
    def position(self):
        """
        Returns the board's shortened position string
        """

        # I'm sorry for this line, but I love Python!
        pos_string = ''.join(['/' * (n % 5 == 0 and n != 0) + p.get_state().name for n, p in enumerate(self.points)])

        # replacement dict: {'EEEEE: 5, 'EEEE': 4, 'EEE: 3, 'EE': 2, 'E': 1}
        for i in reversed(range(1, 6)):
            pos_string = pos_string.replace(''.join('E' * i), str(i))

        return "%s %s %s %s %s" % (
            ''.join(pos_string),
            self.turn.name.lower(),
            'g%d' % self.goatsToBePlaced,
            'c%d' % self.deadGoats,
            'm%s' % self.lastMove
        )

    @staticmethod
    def valid(index):
        """
        Returns whether a given point index is valid.
        """

        return 0 <= index < 25

    def is_movable(self, from_point, to_point):
        """
        Is a piece movable from one particular point to another?
        eg. 'A1' to 'B2'
        """

        # check if both points are valid
        if not (Board.valid(from_point) and Board.valid(to_point)):
            return False

        return (
            # connection must exist
            to_point in Board._move_connections[from_point] and
            # to_point must be empty
            self.points[to_point].get_state() == Point.State.E
        )

    def can_capture(self, from_point, to_point):
        """
        Can a tiger capture from one particular point to another?
        eg. 'C1' to 'E1'
        """

        # check if both points are valid
        if not (Board.valid(from_point) and Board.valid(to_point)):
            return False

        # check for a valid midpoint
        if (from_point + to_point) % 2 != 0:
            return False

        mid_point = int((from_point + to_point) / 2)

        return (
            # connection must exist
            to_point in Board._capture_connections[from_point] and
            # from_point must be a tiger
            self.points[from_point].get_state() == Point.State.T and
            # mid_point must be a goat
            self.points[mid_point].get_state() == Point.State.G and
            # to_point must be empty
            self.points[to_point].get_state() == Point.State.E
        )

    def _tiger_moves(self):
        """
        Returns a generator that loops through the possible moves for each tiger
        """

        return (
            self.is_movable(f, f + d) or self.can_capture(f, f + 2 * d)
            for f in self.tigerPos
            for d in Board.directions
        )

    def _all_tigers_trapped(self):
        """
        Returns True if there is a valid move for a tiger remaining on the board
        """

        return not any(self._tiger_moves())

    @property
    def winner(self):
        """
        Return the winner if the game is over, else return None
        """

        if self.deadGoats == 5:
            return self.Player.T

        if self._all_tigers_trapped():
            return self.Player.G

        return None


# move related
    def _placements(self):
        return [
            Board.Move(point.index, point.index, Board.MoveType.P)
            for point in self.points
            if point.get_state() == Point.State.E
        ]

    def _movements(self):
        """
        Returns the possible movements (excluding captures)
        for the board and the turn
        """

        # since we don't have goat positions, we just loop to find the goats
        if self.turn == Board.Player.G:
            pieces = [p.index for p in self.points if p.get_state() == Point.State.G]
        else:
            pieces = self.tigerPos

        return [
            Board.Move(p, p + d, Board.MoveType.M)
            for p in pieces
            for d in Board.directions
            if self.is_movable(p, p + d)
        ]

    def _captures(self):
        return [
            Board.Move(t, t + 2 * d, Board.MoveType.C)
            for t in self.tigerPos
            for d in Board.directions
            if self.can_capture(t, t + 2 * d)
        ]

    def _movable(self, t_pos):
        """
        Returns whether a particular tiger is movable
        """

        return any(
            self.is_movable(t_pos, t_pos + d) or self.can_capture(t_pos, t_pos + 2 * d)
            for d in Board.directions
        )

    def make_move(self, move):
        """
        Makes the given move on the board
        """

        # placement
        if move.mt == Board.MoveType.P:
            self.points[move.t].set_state("G")
            self.turn = Board.Player.T
            self.goatsToBePlaced -= 1

        # movement
        elif move.mt == Board.MoveType.M:
            if self.turn == Board.Player.G:
                self.points[move.t].set_state("G")
                self.points[move.f].set_state("E")
                self.turn = Board.Player.T
            else:
                self.points[move.t].set_state("T")
                self.points[move.f].set_state("E")
                self.turn = Board.Player.G
                try:
                    self._set_tiger_positions()
                except:
                    print("-------------------ERROR-------------------")
                    self.show()
                    print(self.tigerPos)
                    raise

        # capture
        elif move.mt == Board.MoveType.C:
            self.points[move.f].set_state("E")
            self.points[(move.t + move.f) // 2].set_state("E")
            self.points[move.t].set_state("T")
            self.turn = Board.Player.G
            self.deadGoats += 1

            try:
                self._set_tiger_positions()
            except:
                print("-------------------ERROR-------------------")
                self.show()
                print(self.tigerPos)
                raise
            # self._set_tiger_positions()

    def revert_move(self, move):
        """
        Reverts the given move on the board
        """

        # placement
        if move.mt == Board.MoveType.P:
            self.points[move.t].set_state("E")
            self.turn = Board.Player.G
            self.goatsToBePlaced += 1

        # movement
        elif move.mt == Board.MoveType.M:
            if self.turn == Board.Player.G:
                self.points[move.f].set_state("T")
                self.points[move.t].set_state("E")
                self.turn = Board.Player.T
                self._set_tiger_positions()
            else:
                self.points[move.f].set_state("G")
                self.points[move.t].set_state("E")
                self.turn = Board.Player.G

        # capture
        elif move.mt == Board.MoveType.C:
            self.points[move.f].set_state("T")
            self.points[(move.t + move.f) // 2].set_state("G")
            self.points[move.t].set_state("E")
            self.turn = Board.Player.T
            self.deadGoats -= 1
            self._set_tiger_positions()

    def movable_tigers(self):
        """
        Returns the number of movable tigers on the board
        """
        return sum(int(self._movable(t)) for t in self.tigerPos)

    def generate_move_list(self, rdm=True):
        """
        Generate a list of all moves for the board and turn
        """

        move_list = []

        # turn = Goat
        if self.turn == Board.Player.G:
            # placement phase
            if self.goatsToBePlaced > 0:
                move_list.extend(self._placements())
            # movement phase
            else:
                move_list.extend(self._movements())

        # turn = Tiger
        else:
            # captures
            # captures are kept before movements
            # to improve the efficiency of ab pruning
            move_list.extend(self._captures())

            # movements
            move_list.extend(self._movements())

        return move_list

    def _get_empty_positions(self):
        """
        Returns all the empty positions(points) in the board.
        """
        return [i.get_index(i.coord) for i in self.points if i.state.name == 'E']

    def _is_closed(self, position):
        """
        Returns True if the position is closed else False.
        --------------------------------------------------
        Closed means that the position is empty and surrounded
        by all the neighbouring goats.  In addition, no tigers
        can access the empty position by capturing.
        """

        all_goat_neighbours = any([not self.points[i].state.name in {'T', 'E'} for i in self._move_connections[position]])

        capture_tiger_present = any([self.points[i].state.name == 'T' for i in self._capture_connections[position]])

        return all_goat_neighbours and not capture_tiger_present

    @property
    def no_of_closed_spaces(self):
        """
        Return the number of closed spaces in the board.
        """
        return len([True for i in self._get_empty_positions() if self._is_closed(i)])

    def copy(self):
        board = Board()
        board.points = self.points
        board.turn = self.turn
        board.deadGoats = self.deadGoats
        board.goatsToBePlaced = self.goatsToBePlaced
        return board
