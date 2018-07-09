import unittest

from Point import Point
from Board import Board


class PointTestCase(unittest.TestCase):
    def setUp(self):
        self.points = [Point(i) for i in range(25)]

    def test_coord(self):
        self.assertEqual(self.points[0].coord, 'A1')
        self.assertEqual(self.points[12].coord, 'C3')
        self.assertEqual(self.points[24].coord, 'E5')

    def test_index(self):
        self.assertEqual(self.points[0].index, 0)
        self.assertEqual(self.points[12].index, 12)

    def test_get_index(self):
        self.assertEqual(Point.get_index('C3'), 12)
        self.assertEqual(Point.get_index('E4'), 19)

    def test_set_state(self):
        self.points[0].set_state('T')
        self.assertEqual(self.points[0].state, Point.State.T)
        self.assertEqual(self.points[0].get_state(), Point.State.T)

    def test_str(self):
        self.assertEqual(str(self.points[0]), 'A1')


class BoardTestCase(unittest.TestCase):
    def setUp(self):
        self.board = Board()
        self.board2 = Board('1GG1G/1GGGT/GGGGG/1GTGG/GTGTG t g0 c3 mA3')
        self.t_win = Board('G4/GG2T/GG1GG/TG1TG/TGGGG t g0 c5 mC4E4')
        self.g_win = Board('1GG1G/1GGGT/1GGGG/GGTGG/GTGTG t g0 c3 mA3')

    def test_init(self):
        self.assertEqual(self.board.tigerPos, [0, 4, 20, 24])

    def test_reset(self):
        self.assertEqual(len(self.board.points), 25)
        self.assertEqual(self.board.goatsToBePlaced, 20)
        self.assertEqual(self.board.deadGoats, 0)
        self.assertEqual(self.board.turn, Board.Player.G)
        self.assertEqual(self.board.lastMove, "")

    def test_get_full_position(self):
        self.assertEqual(Board._get_full_position('1GG1G/1GGGT/GGGGG/1GTGG/GTGTG'), list('EGGEGEGGGTGGGGGEGTGGGTGTG'))
        self.assertEqual(Board._get_full_position(self.t_win.position.split()[0]), list('GEEEEGGEETGGEGGTGETGTGGGG'))

    def test_position(self):
        self.assertEqual(self.board2.position, '1GG1G/1GGGT/GGGGG/1GTGG/GTGTG t g0 c3 mA3')
        self.assertEqual(self.g_win.position, '1GG1G/1GGGT/1GGGG/GGTGG/GTGTG t g0 c3 mA3')

    def test_winner(self):
        self.assertEqual(self.t_win.winner, Board.Player.T)
        self.assertEqual(self.g_win.winner, Board.Player.G)
        self.assertIsNone(self.board.winner)
        self.assertIsNone(self.board2.winner)

    def test_parse_position(self):
        pass
