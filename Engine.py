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
            return 3 * self.board.movable_tigers() + 50 * self.board.deadGoats - depth

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
            for move in self.board.generate_move_list():
                # first make the move
                self.board.make_move(move)

                # go deeper in the search tree recursively
                value = self.minmax(True, depth + 1, alpha, beta)

                if value < beta:
                    beta = value
                    if depth == 0 and not is_max:
                        self.best_move = move

                # then revert the move
                self.board.revert_move(move)

                # ab pruning
                if alpha >= beta:
                    return beta

            return beta

        # find the maximum attainable value for the maximizer
        else:
            for move in self.board.generate_move_list():
                # first make the move
                self.board.make_move(move)

                # go deeper in the search tree recursively
                value = self.minmax(False, depth + 1, alpha, beta)

                if value > alpha:
                    alpha = value
                    if depth == 0 and is_max:
                        self.best_move = move

                # then revert the move
                self.board.revert_move(move)

                # ab pruning
                if alpha >= beta:
                    return alpha

            return alpha

    def best_tiger_move(self):
        self.minmax()
        return self.best_move

    def best_goat_move(self):
        self.minmax(is_max=False)
        return self.best_move
