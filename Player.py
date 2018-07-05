class Player(object):
    """
    Abstract class for a generic Player.
    Tiger and Goat inherit from this.
    """

    def __init__(self, arg):
        super(Player, self).__init__()
        self.arg = arg
