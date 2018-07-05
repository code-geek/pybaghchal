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

    def point(self, coord):
        file = coord[0]
        rank = coord[1]
        assert len(coord) == 2 and not file.isdigit() and rank.isdigit(), "Invalid Coordinates"

        # Top left point on the board is A1
        # A1 = point[0], E5 = point[24]
        return self.points[(Point.File[file].value - 1) + (int(rank) - 1) * 5]

    def reset(self):
        """Resets the board to its initial position"""

        self.points = [Point(i, j) for i in range(1, 6) for j in range(1, 6)]
        self.tigerPos = [0, 4, 20, 24]

        for i in self.tigerPos:
            self.points[i].set_state("T")

        self.goatsToBePlaced = 20
        self.deadGoats = 0
        self.turn = self.Player.G

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

    def _get_full_position(self, pos_string):
        full_pos = []
        for i in pos_string.upper():
            if i == 'G':
                full_pos.append('G')
            elif i == 'T':
                full_pos.append('T')
            elif i.isdigit():
                for j in range(int(i)):
                    full_pos.append('E')
        return full_pos

    def parse_position(self, position):
        parts = position.split()
        full_pos = self._get_full_position(parts[0])
        assert len(full_pos) == 25

        for idx, p in enumerate(full_pos):
            self.points[idx].set_state(p)


b = Board("1GG1G/1GGGT/GGGGG/1GTGG/GTGTG t g0 c3 mA3")
# print(b)

b.point('E5').set_state("T")
b.show()
