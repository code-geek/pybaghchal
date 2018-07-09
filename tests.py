import unittest

from Point import Point


class TestPoint(unittest.TestCase):
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
