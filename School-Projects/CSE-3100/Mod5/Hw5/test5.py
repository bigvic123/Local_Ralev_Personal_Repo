from hw5 import solveable, valid_moves
import unittest

class TestValidMoves(unittest.TestCase):
        def testValidMoves(self):
                """Tests that valid_moves returns correct positions"""
                # 'k' denotes a knight
                # 'x' denotes possible moves
                # Positions should be given in (row, column) tuples
                #  0 1 2 3 4 5 6 7
                #0 - - - - - - - -
                #1 - - - - - - - --
                #2 - - - - - - - -
                #3 - - - - - - - -
                #4 - - - - - - - -
                #5 - x - - - - - -
                #6 - - x - - - - -
                #7 k - - - - - - -
                # TODO: Fill in the data to test valid_moves on the board above
                k_idx = (7, 0)
                expected_valid_moves = {(5, 1), (6, 2)}
                self.assertEqual(valid_moves(k_idx), expected_valid_moves)

                # TODO: Write tests for valid_moves for the following boards
                #  0 1 2 3 4 5 6 7
                #0 k - - - - - - -
                #1 - - x - - - - -
                #2 - x - - - - - -
                #3 - - - - - - - -
                #4 - - - - - - - -
                #5 - - - - - - - -
                #6 - - - - - - - -
                #7 - - - - - - - -
                
                k_idx = (0, 0)
                expected_valid_moves = {(2, 1), (1, 2)}
                self.assertEqual(valid_moves(k_idx), expected_valid_moves)

                #  0 1 2 3 4 5 6 7
                #0 - - - - - - - k
                #1 - - - - - x - -
                #2 - - - - - - x -
                #3 - - - - - - - -
                #4 - - - - - - - -
                #5 - - - - - - - -
                #6 - - - - - - - -
                #7 - - - - - - - -
                
                k_idx = (0, 7)
                expected_valid_moves = {(1, 5), (2, 6)}
                self.assertEqual(valid_moves(k_idx), expected_valid_moves)

                #  0 1 2 3 4 5 6 7
                #0 - - - - - - - -
                #1 - - - - - - - -
                #2 - - - - - - - -
                #3 - - - - - - - -
                #4 - - - - - - - -
                #5 - - - - - - x -
                #6 - - - - - x - -
                #7 - - - - - - - k
                
                k_idx = (7, 7)
                expected_valid_moves = {(6, 5), (5, 6)}
                self.assertEqual(valid_moves(k_idx), expected_valid_moves)

                #  0 1 2 3 4 5 6 7
                #0 - - - - - - - -
                #1 - - x - x - - -
                #2 - x - - - x - -
                #3 - - - k - - - -
                #4 - x - - - x - -
                #5 - - x - x - - -
                #6 - - - - - - - -
                #7 - - - - - - - -

                k_idx = (3, 3)
                expected_valid_moves = {(1, 2), (1, 4), (2, 1), (2, 5), (4, 1), (4, 5), (5, 2), (5, 4)}
                self.assertEqual(valid_moves(k_idx), expected_valid_moves)
                print("valid_moves tests are done");

class TestSolveable(unittest.TestCase):
        def testUnsolveable(self):
                """Test a few unsolveable puzzles"""
                p_idxs = {(7, 7), (0, 0)}
                k_idx = (3, 3)
                expected_result = False
                self.assertEqual(solveable(p_idxs, k_idx), expected_result)

                p_idxs = {(5, 3), (6, 3), (7, 3)}
                k_idx = (4, 3)
                expected_result = False
                self.assertEqual(solveable(p_idxs, k_idx), expected_result)

                p_idxs = {(1, 1), (1, 2)}
                k_idx = (0, 0)
                expected_result = False
                self.assertEqual(solveable(p_idxs, k_idx), expected_result)

        def testSolveableSimple(self):
                """Test a simple solveable puzzle"""
                p_idxs = {(4, 5), (5, 7)}
                k_idx = (3, 3)
                expected_result = True
                self.assertEqual(solveable(p_idxs, k_idx), expected_result)

                p_idxs = {(4, 5), (5, 7)}
                k_idx = (3, 3)
                expected_result = True
                self.assertEqual(solveable(p_idxs, k_idx), expected_result)

                p_idxs = {(2, 1), (4, 2)}
                k_idx = (3, 3)
                expected_result = True
                self.assertEqual(solveable(p_idxs, k_idx), expected_result)

        def testSolveableHard(self):
                """Test a few more complex solveable puzzles - try to break your recursive algorithm to help you catch any mistakes"""
                p_idxs = {(4, 5), (5, 7), (6, 5), (4, 4), (2, 3), (1, 1), (3, 2)}
                k_idx = (3, 3)
                expected_result = True
                self.assertEqual(solveable(p_idxs, k_idx), expected_result)

                p_idxs = {(1, 2), (2, 4), (4, 5), (3, 3), (5, 2), (7, 1), (5, 3)}
                k_idx = (0, 0)
                expected_result = True
                self.assertEqual(solveable(p_idxs, k_idx), expected_result)

                p_idxs = {(2, 3), (3, 1), (5, 0), (7, 1), (6, 3), (7, 5), (5, 6)}
                k_idx = (1, 1)
                expected_result = True
                self.assertEqual(solveable(p_idxs, k_idx), expected_result)

unittest.main()