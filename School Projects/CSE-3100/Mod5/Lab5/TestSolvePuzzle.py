from solve_puzzle import solve_puzzle as puzzle
import unittest

class TestSolvePuzzle(unittest.TestCase):
        def testClockwise(self):
                """Tests a board solveable using only CW moves"""
                mylist = [1, 3, 0, 2, 4]
                self.assertTrue(puzzle(mylist))
                
        def testCounterClockwise(self):
                """Tests a board solveable using only CCW moves"""
                mylist = [2, 1, 3, 4, 0]
                self.assertTrue(puzzle(mylist))
                
        def testMixed(self):
                """Tests a board solveable using only a combination of CW and CCW moves"""
                mylist = [3, 6, 4, 1, 3, 4, 2, 0]
                self.assertTrue(puzzle(mylist))
                
        def testUnsolveable(self):
                """Tests an unsolveable board"""
                mylist = [3, 4, 1, 2, 0]
                self.assertFalse(puzzle(mylist))
                
unittest.main()