import sys

from Engine import Engine
from Board import Board


class Game(object):
    """Handles the operations of a Game"""

    def __init__(self, position=None):
        super(Game, self).__init__()
        self.board = Board(position)
        self.engine = Engine(self.board, depth=7)

    def input_move(self):
        idx = None
        while True:
            try:
                idx = int(input())
            except:
                print("Invalid Move")
                continue
            else:
                break
        if idx == 99:
            sys.exit()
        return idx

    def human_move(self):
        moves = self.engine.generate_move_list()
        self.board.show()
        print("Please choose one move from the list.")
        print('\n'.join("%d. %s" % (i, str(move)) for i, move in enumerate(moves)))

        self.engine._make_move(moves[self.input_move()])


def play():
    game = Game()

    while not game.board.winner:
        game.human_move()
        if game.board.winner:
            break
        game.engine.make_best_move()

    game.board.show()
    print(game.board.winner)


def ai_vs_ai():
    game = Game()
    # move_num = 1
    while not game.board.winner:
        # print(move_num)
        # move_num += 1
        game.engine.make_best_move()
        game.board.show()

    return game.board.winner


play()
