from Point import Point
from enum import Enum


class Board(object):
    """A baghchal board"""

    class Player(Enum):
        T = 1
        G = 2

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

    def point_index(self, coord):
        # if an integer is passed, check if it's valid and return it
        if type(coord) == int:
            return coord

        file, rank = coord

        # check if the coordinates are valid
        assert len(coord) == 2 and file in list('ABCDE') and int(
            rank) in range(1, 6), "Invalid Coordinates: %s" % str(coord)

        # Top left point on the board is A1
        # A1 = point[0], E5 = point[24]
        return (Point.File[file].value - 1) + (int(rank) - 1) * 5

    def reset(self):
        """Resets the board"""

        self.points = [Point(i, j) for i in range(1, 6) for j in range(1, 6)]
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

    def _get_full_position(self, pos_string):
        """
        get a full position from a shortened position string:
        eg. 1GG1G/1GGGT/GGGGG/1GTGG/GTGTG gives
        EGGEGEGGGTGGGGGEGTGGGTGTG
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
        full_pos = self._get_full_position(parts[0])
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
        for idx, p in enumerate(self.points):
            if p.get_state() == Point.State.T:
                self.tigerPos.append(idx)

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

    def is_movable(self, from_point, to_point):
        """
        Is a piece movable from one particular point to another?
        eg. 'A1' to 'B2'
        """

        # point_index checks if the points are valid points on the board
        from_point = self.point_index(from_point)
        to_point = self.point_index(to_point)

        # check if both points are on the board
        if from_point not in range(25) or to_point not in range(25):
            return False

        return (
            # to_point must be empty
            self.points[to_point].get_state() == Point.State.E and
            # the points must be traversable
            (
                # horizontal and vertical
                abs(from_point - to_point) in [1, 5] or\
                # diagonal (allowed only from even points)
                ((from_point % 2 == 0) and abs(from_point - to_point) in [4, 6])
            )
        )

    def can_capture(self, from_point, to_point):
        """
        Can a tiger capture from one particular point to another?
        eg. 'C1' to 'E1'
        """

        # point_index checks if the points are valid points on the board
        from_point = self.point_index(from_point)
        to_point = self.point_index(to_point)

        # check if both points are on the board
        if from_point not in range(25) or to_point not in range(25):
            return False

        # check for a valid midpoint
        if (from_point + to_point) % 2 != 0:
            return False

        mid_point = int((from_point + to_point) / 2)

        return (
            # from_point must be a tiger
            self.points[from_point].get_state() == Point.State.T and
            # mid_point must be a goat
            self.points[mid_point].get_state() == Point.State.G and
            # to_point must be empty
            self.points[to_point].get_state() == Point.State.E and
            # the points must be one point apart
            (
                # horizontal and vertical
                abs(from_point - to_point) in [2, 10] or\
                # diagonal (allowed only from even points)
                ((from_point % 2 == 0) and abs(from_point - to_point) in [8, 12])
            )
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

    def movable_tigers(self):
        """
        Returns the number of movable tigers
        """

        return sum(self._tiger_moves())

    def all_tigers_trapped(self):
        """
        Are all tigers trapped?
        """

        return not any(self._tiger_moves())

    @property
    def winner(self):
        """
        Return the winner if the game is over, else return None
        """

        if self.deadGoats == 5:
            return self.Player.T

        if self.all_tigers_trapped():
            return self.Player.G

        return None
