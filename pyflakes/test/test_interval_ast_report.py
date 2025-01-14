"""
Tests for detecting redefinition of builtins.
"""
from pyflakes import messages as m
from pyflakes.test.harness import TestCase


class TestIntervalASTReport(TestCase):
    def test_divide_by_zero(self):
        self.flakes('''
        def foo():
            y = 0
            x = 7
            y = x // y
        ''', m.DivisionByZero)

    def test_divide_by_zero_addition(self):
        self.flakes('''
        def foo():
            x = -5
            y = 5
            y = 5 // (x + y)
        ''', m.DivisionByZero)

    def test_divide_by_zero_computed(self):
        self.flakes('''
        def foo():
            y = 1
            x = 1
            y = x // (y - x)
        ''', m.DivisionByZero)

    def test_divide_by_zero_multiplication(self):
        self.flakes('''
        def foo():
            x = 2
            x = x // (x * 0)
        ''', m.DivisionByZero)

    def test_divide_by_zero_floor(self):
        self.flakes('''
        def foo():
            y = 1
            x = 2
            y = x // (y // x)
        ''', m.DivisionByZero)

    def test_no_divide_by_zero(self):
        self.flakes('''
        def foo(arg: int):
            1 // arg
        ''')

    def test_dead_code_if(self):
        self.flakes('''
        def foo():
            a = False
            b = 1
            if a:
                b = b + b
        ''', m.DeadCode)

    def test_dead_code_elif(self):
        self.flakes('''
        def foo(arg: bool):
            a = False
            b = 1
            if arg:
                b = b + b
            elif a:
                b = b + b
        ''', m.DeadCode)

    def test_dead_code_else(self):
        self.flakes('''
        def foo():
            a = True
            b = 1
            if a:
                b = b + b
            else:
                b = b + b
        ''', m.DeadCode)

    def test_dead_code_and(self):
        self.flakes('''
        def foo():
            a = True
            c = False
            b = 1
            if a and c:
                b = b + b
        ''', m.DeadCode)

    def test_dead_code_or(self):
        self.flakes('''
        def foo():
            a = True
            c = False
            b = 1
            if c or c or c or c or a:
                b = b + b
        ''', m.DeadCode)

    def test_dead_code_equals(self):
        self.flakes('''
        def foo():
            a = True
            c = False
            b = 1
            if c == a:
                b = b + b
        ''', m.DeadCode)

    def test_dead_code_and2(self):
        self.flakes('''
        def foo():
            a = True
            c = False
            c = a and c
            b = 1
            if c:
                b = b + b
        ''', m.DeadCode)

    def test_dead_code_or2(self):
        self.flakes('''
        def foo():
            a = True
            c = False
            c = c or c or c or c or a
            b = 1
            if c:
                b = b + b
        ''', m.DeadCode)

    def test_dead_code_equals2(self):
        self.flakes('''
        def foo():
            a = True
            c = False
            c = c == a
            b = 1
            if c:
                b = b + b
        ''', m.DeadCode)

    def test_dead_code_if_if(self):
        self.flakes('''
        def foo():
            a = True
            c = False
            b = 1
            if a:
                if a:
                    if c:
                        b = b + b
        ''', m.DeadCode, m.DeadCode, m.DeadCode)

    def test_dead_code_if_elif(self):
        self.flakes('''
        def foo():
            a = True
            c = False
            b = 1
            if a:
                if a:
                    b = b + b
                elif c:
                    b = b + b
        ''', m.DeadCode, m.DeadCode, m.DeadCode)

    def test_dead_code_if_elif_alt(self):
        self.flakes('''
        def foo():
            a = True
            c = False
            b = 1
            if a:
                if a:
                    b = b + b
                elif a and c:
                    b = b + b
        ''', m.DeadCode, m.DeadCode, m.DeadCode)

    def test_dead_code_i_smaller(self):
        self.flakes('''
        def foo():
            a = 5
            b = 6
            if b < a:
                b = b + b
            if a < b:
                b = b + b                        
        ''', m.DeadCode, m.DeadCode)

    def test_dead_code_i_greater(self):
        self.flakes('''
        def foo():
            a = 5
            b = 6
            if b > a:
                b = b + b
            if a > b:
                b = b + b                        
        ''', m.DeadCode, m.DeadCode)

    def test_dead_code_i_greater(self):
        self.flakes('''
        def foo():
            a = 5
            b = 6
            if a == a:
                b = b + b
            if a == b:
                b = b + b                        
        ''', m.DeadCode, m.DeadCode)

    def test_dead_code_i_greater(self):
        self.flakes('''
        def foo():
            a = 5
            b = 6
            if a != a:
                b = b + b
            if a != b:
                b = b + b                        
        ''', m.DeadCode, m.DeadCode)

    def test_no_dead_code_if(self):
        self.flakes('''
        def foo():
            a = True
            b = 1
            if a:
                b = b + b                     
        ''', m.DeadCode)

    def test_no_dead_code_if_else(self):
        self.flakes('''
        def foo(arg:bool):
            b = 1
            if arg:
                b = b + b
            else:
                b = b + b                     
        ''')

    def test_dead_code_ifif(self):
        self.flakes('''
        def foo():
            a = True
            c = False
            b = 1
            if a:
                b = b + b
            if c:
                b = b + b                        
        ''', m.DeadCode, m.DeadCode)
