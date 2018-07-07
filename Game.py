from Engine import Engine
from Board import Board


class Game(object):
    """Handles the operations of a Game"""

    def __init__(self):
        super(Game, self).__init__()
        self.board = Board()
        self.engine = Engine(self.board, depth=12)

    def input_move(self):
        idx = int(input())
        return idx

    def human_move(self):
        moves = self.engine.generate_move_list()
        self.board.show()
        print("Please choose one move from the list.")
        print('  |  '.join("%d. %s" % (i, str(move)) for i, move in enumerate(moves)))

        self.engine._make_move(moves[self.input_move()])
        self.engine.make_best_move()


game = Game()

while not game.board.winner:
    game.human_move()
