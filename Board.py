from Point import Point
from enum import Enum


class Board(object):
    """A baghchal board"""

    class Player(Enum):
        T = 1
        G = 2

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

    def point(self, coord):
        file = coord[0]
        rank = coord[1]
        assert len(coord) == 2 and not file.isdigit() and rank.isdigit(), "Invalid Coordinates"

        # Top left point on the board is A1
        # A1 = point[0], E5 = point[24]
        return self.points[(Point.File[file].value - 1) + (int(rank) - 1) * 5]

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
        print("Dead Goats: %d" % self.deadGoats)
        print("Tiger Pos: %s" % str(self.tigerPos))

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
        # I'm sorry for this line, but I love Python!
        pos_string = ''.join(['/' * (n % 5 == 0 and n != 0) + p.get_state().name for n, p in enumerate(self.points)])

        for i in reversed(range(1, 6)):
            pos_string = pos_string.replace(''.join('E' * i), str(i))

        return "%s %s %s %s %s" % (
            ''.join(pos_string),
            self.turn.name.lower(),
            'g%d' % self.goatsToBePlaced,
            'c%d' % self.deadGoats,
            'm%s' % self.lastMove
        )
