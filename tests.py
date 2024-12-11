from typing import Callable
import unittest

from wires import evaluate_function, get_board

class TestEvaluateFunction(unittest.TestCase):
    def _test_two_inputs(self, board: str, fun: Callable[[bool, bool], bool]):
        for v1 in (True, False):
            for v2 in (True, False):
                try:
                    assert evaluate_function(board, v1, v2) == fun(v1, v2)
                except AssertionError:
                    print(v1, v2, evaluate_function(board, v1, v2), fun(v1, v2))
                    raise

    def test_not(self):
        board = get_board('not')
        assert evaluate_function(board, True) == False
        assert evaluate_function(board, False) == True

    def test_and(self):
        board = get_board('and')
        self._test_two_inputs(board, lambda a, b: a and b)
    
    def test_or(self):
        board = get_board('or')
        self._test_two_inputs(board, lambda a, b: a or b)
    
    def test_nor(self):
        board = get_board('nor')
        self._test_two_inputs(board, lambda a, b: not(a or b))
    
    def test_xor(self):
        board = get_board('xor')
        self._test_two_inputs(board, lambda a, b: a != b)
    
    def test_nand(self):
        board = get_board('nand')
        self._test_two_inputs(board, lambda a, b: not (a and b))

if __name__ == "__main__":
    unittest.main()
