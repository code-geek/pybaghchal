from enum import Enum


class Point(object):
    """A point on the board"""

    class State(Enum):
        """What's on a point"""
        E = None  # Empty
        T = 1  # Tiger
        G = 2  # Goat

    class File(Enum):
        """A file is a column of the board represented as a letter"""
        A = 1
        B = 2
        C = 3
        D = 4
        E = 5

        def __str__(self):
            return str(self.name)

    def __init__(self, file, rank, state=None):
        super(Point, self).__init__()
        self.file = self.File(file)
        self.rank = rank
        self.state = self.State(state)

    def set_state(self, state):
        self.state = self.State[state]

    def get_state(self):
        return self.state

    def print_state(self):
        return " " if self.state.name == "E" else self.state.name

    @property
    def coord(self):
        return "%s%s" % (str(self.file), str(self.rank))

    @property
    def index(self):
        return (self.file.value - 1) + (int(self.rank) - 1) * 5

    def __str__(self):
        return self.coord

    def __repr__(self):
        return self.__str__()
