from Board import Board


class Engine(object):
    """
    Takes a board position and returns the best move
    """

    INF = 1000000

    def __init__(self, board, depth=5):
        super(Engine, self).__init__()
        self.board = board
        self.depth = depth
        self.best_move = None

    def evaluate(self, depth=0):
        """
        Returns a numeric evaluation of the position
        Written from the perspective of Tiger
        """
        winner = self.board.winner
        if not winner:
            return 300 * self.board.movable_tigers() + 700 * self.board.deadGoats\
                   - 700 * self.board.no_of_closed_spaces - depth

        if winner == Board.Player.G:
            return -Engine.INF
        elif winner == Board.Player.T:
            return Engine.INF

    def minmax(self, is_max=True, depth=0, alpha=-INF, beta=INF):
        score = self.evaluate(depth)

        # if a leaf node is reached, return the score
        if depth == self.depth or abs(score) == Engine.INF:
            return score

        # find the minimum attainable value for the minimizer
        if not is_max:
            value = 100000000
            for move in self.board.generate_move_list():
                # first make the move
                self.board.make_move(move)

                # go deeper in the search tree recursively
                value_t = self.minmax(True, depth + 1, alpha, beta)

                beta = min(beta, value_t)


                if value_t < value:
                    value = value_t
                    beta = min(beta, value)
                    if depth == 0:
                        self.best_move = move

                # then revert the move
                self.board.revert_move(move)

                if alpha >= beta:
                    break

            return value

        # find the maximum attainable value for the maximizer
        else:
            value = -100000000
            for move in self.board.generate_move_list():
                # first make the move
                self.board.make_move(move)

                # go deeper in the search tree recursively
                value_t = self.minmax(False, depth + 1, alpha, beta)

                if value_t > value:
                    value = value_t
                    alpha = max(alpha, value)
                    if depth == 0:
                        self.best_move = move



                # then revert the move
                self.board.revert_move(move)

                if alpha >= beta:
                    break

            return value

    def best_tiger_move(self):
        self.minmax()
        assert self.best_move is not None, "best_tiger_move is None."
        return self.best_move

    def best_goat_move(self):
        self.minmax(is_max=False)
        assert self.best_move is not None, "best_goat_move is None."
        return self.best_move

    def make_best_move(self):
        if self.board.turn == Board.Player.G:
            move = self.best_goat_move()
        else:
            move = self.best_tiger_move()
        self.board.make_move(move)

    def get_best_move(self):
        if self.board.turn == Board.Player.G:
            move = self.best_goat_move()
        else:
            move = self.best_tiger_move()
        return move
