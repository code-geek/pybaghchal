from enum import Enum


class Point(object):
    """A point on the board"""

    # A1 = top left, E5 = bottom right
    # A1 = point[0], B1 = point[1], E5 = point[24]
    #   A   B   C   D   E
    # 1 T               T
    #   | \ | / | \ | / |
    # 2
    #   | / | \ | / | \ |
    # 3
    #   | \ | / | \ | / |
    # 4
    #   | / | \ | / | \ |
    # 5 T               T

    _coord_to_index = {'%s%s' % (chr(i + 65), j + 1): (i + j * 5) for i in range(5) for j in range(5)}
    _index_to_coord = {v: k for k, v in _coord_to_index.items()}

    class State(Enum):
        """What's on a point"""
        E = None  # Empty
        T = 1  # Tiger
        G = 2  # Goat

    def __init__(self, idx, state=None):
        super(Point, self).__init__()
        self.index = idx
        self.state = self.State(state)

    def set_state(self, state):
        self.state = self.State[state]

    def get_state(self):
        return self.state

    def print_state(self):
        return " " if self.state.name == "E" else self.state.name

    @property
    def coord(self):
        return self._index_to_coord[self.index]

    def __str__(self):
        return self.coord

    def __repr__(self):
        return self.__str__()
