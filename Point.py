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

    # hardcoding these so they're more readable and don't need to be computed every time
    _coord_to_index = {'A1': 0, 'A2': 5, 'A3': 10, 'A4': 15, 'A5': 20,
                       'B1': 1, 'B2': 6, 'B3': 11, 'B4': 16, 'B5': 21,
                       'C1': 2, 'C2': 7, 'C3': 12, 'C4': 17, 'C5': 22,
                       'D1': 3, 'D2': 8, 'D3': 13, 'D4': 18, 'D5': 23,
                       'E1': 4, 'E2': 9, 'E3': 14, 'E4': 19, 'E5': 24}

    _index_to_coord = {0: 'A1', 1: 'B1', 2: 'C1', 3: 'D1', 4: 'E1',
                       5: 'A2', 6: 'B2', 7: 'C2', 8: 'D2', 9: 'E2',
                       10: 'A3', 11: 'B3', 12: 'C3', 13: 'D3', 14: 'E3',
                       15: 'A4', 16: 'B4', 17: 'C4', 18: 'D4', 19: 'E4',
                       20: 'A5', 21: 'B5', 22: 'C5', 23: 'D5', 24: 'E5'}

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

    @classmethod
    def get_index(cls, coord):
        assert (
            len(coord) == 2 and coord[0] in list('ABCDE') and int(coord[1]) in range(1, 6)
        ), "Invalid Coordinates: %s" % str(coord)
        return cls._coord_to_index[coord]

    @classmethod
    def get_coord(cls, index):
        assert 0 <= index < 25, "Invalid index: %d" % index
        return cls._index_to_coord[index]

    @property
    def coord(self):
        return Point.get_coord(self.index)

    def __str__(self):
        return self.coord

    def __repr__(self):
        return self.__str__()
