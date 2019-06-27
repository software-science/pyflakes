from pyflakes.interval import Interval, INFINITY, NEG_INFINITY, TOP
from pyflakes.test.harness import TestCase


class TestInterval(TestCase):
    def test_plus_integers(self):
        #  1 + 2 = 3
        self.assertEqual(Interval(1) + Interval(2), Interval(3))
        #  -1 + 1 = 0
        self.assertEqual(Interval(-1) + Interval(1), Interval(0))
        #  0 + 1 = 1
        self.assertEqual(Interval(0) + Interval(1), Interval(1))
        #  1 + -1 = 0
        self.assertEqual(Interval(1) + Interval(-1), Interval(0))

    def test_plus_intervals(self):
        # [-10,1] + [-1,2] = [-11,3]
        self.assertEqual(Interval(-10, 1) + Interval(-1, 2), Interval(-11, 3))
        # [-1,1] + [1,2] = [0,3]
        self.assertEqual(Interval(-1, 1) + Interval(1, 2), Interval(0, 3))
        # [-1,0] + [1,1] = [0,1]
        self.assertEqual(Interval(-1, 0) + Interval(1), Interval(0, 1))
        # [0,1] + [-1,-1] = [-1,0]
        self.assertEqual(Interval(0, 1) + Interval(-1), Interval(-1, 0))

    def test_plus_infinity(self):
        # [-inf,1] + [-1,2] = [-inf, 3]
        self.assertEqual(Interval(NEG_INFINITY, 1) + Interval(-1, 2), Interval(NEG_INFINITY, 3))
        # [-10, inf] + [-1,2] = [-11, inf]
        self.assertEqual(Interval(-10, INFINITY) + Interval(-1, 2), Interval(-11, INFINITY))
        # [-10,1] + [-inf,2] = [-inf,3]
        self.assertEqual(Interval(-10, 1) + Interval(NEG_INFINITY, 2), Interval(NEG_INFINITY, 3))
        # [-10,1] + [-1,inf] = [-11,inf]
        self.assertEqual(Interval(-10, 1) + Interval(-1, INFINITY), Interval(-11, INFINITY))
        # [0,inf] + 2 = [2, inf]
        self.assertEqual(Interval(0, INFINITY) + Interval(2), Interval(2, INFINITY))
        # [-inf,0] + 2 = [-inf, 2]
        self.assertEqual(Interval(NEG_INFINITY, 0) + Interval(2), Interval(NEG_INFINITY, 2))
        # 1 + [0, inf] = [1,inf]
        self.assertEqual(Interval(1) + Interval(0, INFINITY), Interval(1, INFINITY))
        # 1 + [-inf, 0] = [-inf,1]
        self.assertEqual(Interval(1) + Interval(NEG_INFINITY, 0), Interval(NEG_INFINITY, 1))
        # 0 + [-inf,inf] = [-inf,inf]
        self.assertEqual(Interval(0) + Interval(NEG_INFINITY, INFINITY), Interval(NEG_INFINITY, INFINITY))
        # [-inf,inf] + [-inf,inf] = [-inf,inf]
        self.assertEqual(Interval(NEG_INFINITY, INFINITY) + Interval(NEG_INFINITY, INFINITY), Interval(NEG_INFINITY, INFINITY))

    def test_plus_top(self):
        # TOP + TOP = TOP
        self.assertEqual(TOP + TOP, TOP)
        # 0 + TOP = TOP
        self.assertEqual(Interval(0) + TOP, TOP)
        # TOP + 0 = TOP
        self.assertEqual(TOP + Interval(0), TOP)
        # TOP + -1 = TOP
        self.assertEqual(TOP + Interval(-1), TOP)

    def test_minus_integer(self):
        # 1 - 2 = -1
        self.assertEqual(Interval(1) - Interval(2), Interval(-1))
        # -1 - -1 = 0
        self.assertEqual(Interval(-1) - Interval(-1), Interval(0))
        # 1 - 1 = 0
        self.assertEqual(Interval(1) - Interval(1), Interval(0))
        # 0 - -1 = 1
        self.assertEqual(Interval(0) - Interval(-1), Interval(1))
        # 0 - 1 = -1
        self.assertEqual(Interval(0) - Interval(1), Interval(-1))

    def test_minus_interval(self):
        # [-10,1] - [-1,2] = [-12,2]
        self.assertEqual(Interval(-10, 1) - Interval(-1, 2), Interval(-12, 2))
        # [1,2] - [1,2] = [0,0]
        self.assertEqual(Interval(1, 2) - Interval(1, 2), Interval(-1, 1))
        # [1,2] - 1 = [0,1]
        self.assertEqual(Interval(1, 2) - Interval(1, 1), Interval(0, 1))
        # [-1,1] - [-1,1] = [-2,2]
        self.assertEqual(Interval(-1, 1) - Interval(-1, 1), Interval(-2, 2))
        # [2,3] - [3,4] = [-2,0]
        self.assertEqual(Interval(2, 3) - Interval(3, 4), Interval(-2, 0))
        # [0,1] - [-1,0] = [0,2]
        self.assertEqual(Interval(0, 1) - Interval(-1, 0), Interval(0, 2))
        # [0,1] - [-5,-4] = [4,6]
        self.assertEqual(Interval(0, 1) - Interval(-5, -4), Interval(4, 6))

    def test_minus_infinity_simple(self):
        # [-inf,1] - [-1,2] = [-inf, 2]
        self.assertEqual(Interval(NEG_INFINITY, 1) - Interval(-1, 2), Interval(NEG_INFINITY, 2))
        # [-10,inf] - [-1,2] = [-12,inf]
        self.assertEqual(Interval(-10, INFINITY) - Interval(-1, 2), Interval(-12, INFINITY))
        # [0,inf] - 2 = [-2,inf]
        self.assertEqual(Interval(0, INFINITY) - Interval(2), Interval(-2, INFINITY))
        # [-inf,0] - 2 = [-inf, -2]
        self.assertEqual(Interval(NEG_INFINITY, 0) - Interval(2), Interval(NEG_INFINITY, -2))
        # 2 - [0,inf] = [-inf,2]
        self.assertEqual(Interval(2) - Interval(0, INFINITY), Interval(NEG_INFINITY, 2))
        # 2 - [-inf,0] = [2,inf]
        self.assertEqual(Interval(2) - Interval(NEG_INFINITY, 0), Interval(2, INFINITY))

    def test_minus_infinity(self):
        # [-10,1] - [-inf,2] = [-12,inf]
        self.assertEqual(Interval(-10, 1) - Interval(NEG_INFINITY, 2), Interval(-12, INFINITY))
        # [-10,1] - [-1,inf] = [-inf,2]
        self.assertEqual(Interval(-10, 1) - Interval(-1, INFINITY), Interval(NEG_INFINITY, 2))
        # [0,inf] - [-inf,0] = [0,inf]
        self.assertEqual(Interval(0, INFINITY) - Interval(NEG_INFINITY, 0), Interval(0, INFINITY))
        # 2 - TOP = TOP
        self.assertEqual(Interval(2) - TOP, TOP)
        # TOP - 2 = TOP
        self.assertEqual(TOP - Interval(2), TOP)
        # 1 - [0, inf] = [-inf,1]
        self.assertEqual(Interval(1) - Interval(0, INFINITY), Interval(NEG_INFINITY, 1))
        # 1 - [-inf,0] = [1,inf]
        self.assertEqual(Interval(1) - Interval(NEG_INFINITY, 0), Interval(1, INFINITY))
        # [-inf,inf] - [-inf,inf] = [-inf,inf]
        self.assertEqual(Interval(NEG_INFINITY, INFINITY) - Interval(NEG_INFINITY, INFINITY), Interval(NEG_INFINITY, INFINITY))

    def test_minus_infinity_top(self):
        self.assertEqual(TOP - TOP, TOP)

    def test_mul(self):
        self.assertEqual(Interval(-10, 1) * Interval(-1, 2), Interval(-20, 10))
        self.assertEqual(Interval(1) * Interval(2), Interval(2))

    def test_mul_infinity_simple(self):
        self.assertEqual(Interval(NEG_INFINITY, 1) * Interval(-1, 2), TOP)
        self.assertEqual(Interval(-10, INFINITY) * Interval(-1, 2), TOP)
        self.assertEqual(Interval(0, INFINITY) * Interval(2), Interval(0, INFINITY))
        self.assertEqual(Interval(NEG_INFINITY, 0) * Interval(2), Interval(NEG_INFINITY, 0))
        self.assertEqual(Interval(NEG_INFINITY, 0) * Interval(0), Interval(0))
        self.assertEqual(Interval(0, INFINITY) * Interval(0), Interval(0))
        self.assertEqual(Interval(0) * Interval(0, INFINITY), Interval(0))
        self.assertEqual(Interval(0) * Interval(NEG_INFINITY, 0), Interval(0))

    def test_mul_infinity(self):
        self.assertEqual(Interval(-10, 1) * Interval(NEG_INFINITY, 2), TOP)
        self.assertEqual(Interval(-10, 1) * Interval(-1, INFINITY), TOP)
        self.assertEqual(Interval(0, INFINITY) * Interval(NEG_INFINITY, 0), Interval(NEG_INFINITY, 0))
        self.assertEqual(Interval(2) * TOP, TOP)
        self.assertEqual(TOP * Interval(2), TOP)
        self.assertEqual(Interval(1) * Interval(0, INFINITY), Interval(0, INFINITY))
        self.assertEqual(Interval(1) * Interval(NEG_INFINITY, 0), Interval(NEG_INFINITY, 0))

    def test_mul_infinity_top(self):
        self.assertEqual(TOP * TOP, TOP)

    def test_div(self):
        self.assertEqual(Interval(-10, 1) // Interval(1, 2), Interval(-10, 1))
        self.assertEqual(Interval(-10, 1) // Interval(-2, -1), Interval(-1, 10))
        self.assertEqual(Interval(1) // Interval(2), Interval(0))

    def test_div_zero(self):
        with self.assertRaises(ZeroDivisionError):
            Interval(10, 20) // Interval(0)
        with self.assertRaises(ZeroDivisionError):
            Interval(10, 20) // Interval(0, 0)

    def test_div_around_zero(self):
        self.assertEqual(Interval(1, 10) // Interval(-2, 2), Interval(-10, 10))
        self.assertEqual(Interval(-10, 1) // Interval(-2, 2), Interval(-10, 10))
        self.assertEqual(Interval(-10, 1) // Interval(0, 2), Interval(-10, 1))
        self.assertEqual(Interval(-10, 1) // Interval(-2, 0), Interval(-1, 10))

    def test_div_infinity(self):
        self.assertEqual(TOP // Interval(1, 5), TOP)
        self.assertEqual(TOP // Interval(1), TOP)
        self.assertEqual(Interval(0, INFINITY) // TOP, TOP)
        self.assertEqual(Interval(NEG_INFINITY, 0) // TOP, TOP)