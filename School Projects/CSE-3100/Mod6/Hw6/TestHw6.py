import unittest, random
from hw6 import cocktail_sort, bs_sublist, opt_insertion_sort, insertion_sort


# TODO: implement unittests below. Use docstrings, whitespace, and comments.
# Hint 1 - start by defining a function that checks if a list is sorted
# Hint 2 - fix the random seed to make your bugs consistent (makes debugging easier)


class TestCocktailSort(unittest.TestCase):
    def test_Sorted(self):
        L = [1, 2, 3, 4, 5]
        cocktail_sort(L)
        #checking the previous element is smaller than the next one for all elements
        for i in range(len(L) - 1):
            self.assertFalse(L[i] > L[i + 1])

    def test_Reverse(self):
        L = [1, 2, 3, 4, 5]
        L.reverse()
        cocktail_sort(L)
        #checking the previous element is smaller than the next one for all elements
        for i in range(len(L) - 1):
            self.assertFalse(L[i] > L[i + 1])

    def test_Random(self):
        L = [1, 2, 3, 4, 5]
        random.shuffle(L)
        cocktail_sort(L)
        #checking the previous element is smaller than the next one for all elements
        for i in range(len(L) - 1):
            self.assertFalse(L[i] > L[i + 1])

    def test_ArbitrarySize(self):
        mynum = random.randint(10, 100)
        L = [i for i in range(mynum)]
        #creating a randomized list of random size
        random.shuffle(L)
        cocktail_sort(L)
        #checking the previous element is smaller than the next one for all elements
        for i in range(len(L) - 1):
            self.assertFalse(L[i] > L[i + 1])


class TestOptInsertionSort(unittest.TestCase):
    def test_Sorted(self):
        L = [1, 2, 3, 4, 5]
        L = opt_insertion_sort(L)
        #checking the previous element is smaller than the next one for all elements
        self.assertTrue(self.verifySorted(L))

    def test_Reverse(self):
        L = [1, 2, 3, 4, 5]
        L.reverse()
        L = opt_insertion_sort(L)
        #checking the previous element is smaller than the next one for all elements
        self.assertTrue(self.verifySorted(L))

    def test_Random(self):
        L = [1, 2, 3, 4, 5]
        random.shuffle(L)
        L = opt_insertion_sort(L)
        #checking the previous element is smaller than the next one for all elements
        self.assertTrue(self.verifySorted(L))

    def test_ArbitrarySize(self):
        mynum = random.randint(10, 100)
        L = [i for i in range(mynum)]
        random.shuffle(L)
        #creating randomized list of random size
        L = opt_insertion_sort(L)
        #checking the previous element is smaller than the next one for all elements
        self.assertTrue(self.verifySorted(L))

    def verifySorted(self, L):
        for i in range(len(L) - 1):
            if L[i] > L[i+1]:
                print(F"Not sorted i={i} Li={L[i]} > {L[i+1]} in L={L}")
                return False
        return True

# bs_sublist tests are provided for you.
class TestBinarySearchSublist(unittest.TestCase):
    def testExtremes(self):
        """Tests binary search on items less than min or greater than max of sublist"""
        # id:  0    1    2    3    4    5    6    7
        L = ['a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        #         |--------sorted sublist---------|
        self.assertEqual(bs_sublist(L, left=1, right=7, item='a'), 0)

        # id:  0    1    2    3    4    5    6    7
        L = ['i', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
        #         |--------sorted sublist---------|
        self.assertEqual(bs_sublist(L, left=1, right=7, item='i'), 7)

    def testWithinUnique(self):
        """Tests binary search on items within the bounds of a sublist, but does not appear in that sublist"""
        # id:  0    1    2    3    4    5    6    7
        L = ['?', 'a', 'c', 'e', 'g', 'i', 'k', 'm']
        #         |--------sorted sublist---------|
        for i, char in enumerate('bdfhjl'):
            L[0] = char
            self.assertEqual(bs_sublist(L, left=1, right=7, item=char), 1 + i)

    def testWithinDuplicate(self):
        """Tests binary search on item within the bounds of a sublist, that do appear in that sublist. Should return the minimum index."""
        # id:  0    1    2    3    4    5    6    7
        L = ['?', 'a', 'b', 'c', 'd', 'e', 'f', 'g']
        #         |--------sorted sublist---------|

        for i, char in enumerate('abcdefgh'):
            n = bs_sublist(L, left=1, right=7, item=char)
            #print(F"testWithinDuplicate n={n}, char={char}")
            self.assertEqual(n, i)

    def testArbitrarySize(self):
        """Tests binary search on sublists of arbitrary size"""
        lower = 'abcdefghijklmnopqrstuvwxyz'

        for n in range(2, 27):
            L = [lower[i] for i in range(n)]
            #print(L)
            j = bs_sublist(L, left=1, right=n - 1, item='a')
            #print(f"line111 j={j} n={n}, L={L}, item=a")
            self.assertEqual(j, 0)  # ['a', 'b', ...] returns 0

            for i, char in enumerate(lower[1:n]):
                L[0] = char
                j = bs_sublist(L, left=1, right=n - 1, item=char)
                #print(f"line116 j={j} n={n} i={i} char={char}, L={L}")
                self.assertEqual(j, i)  # ['?', b', ...] returns i

        # n = 2
        # id:  0    1    2    3    4    5    6    7
        # L = ['a', 'b',]   # pos = 0
        # L = ['b', 'b',]   # pos = 0
        # L = ['c', 'b',]   # pos = 1
        #           |--------sorted sublist---------|
        # n = 3
        # L = ['a', 'b', 'c']  # pos = 0
        # L = ['b', 'b', 'c']  # pos = 0
        # L = ['c', 'b', 'c']  # pos = 1
        # L = ['d', 'b', 'c']  # pos = 2

        # n = 4
        # L = ['a', 'b', 'c', 'd']   # pos = 0
        # L = ['b', 'b', 'c', 'd']   # pos = 0
        # L = ['c', 'b', 'c', 'd']   # pos = 1
        # L = ['d', 'b', 'c', 'd']   # pos = 2
        # L = ['e', 'b', 'c', 'd']   # pos = 3

        # n = 5
        # L = ['a', 'b', 'c', 'd', 'e']   # pos = 0
        # L = ['b', 'b', 'c', 'd', 'e']   # pos = 0
        # L = ['c', 'b', 'c', 'd', 'e']   # pos = 1
        # L = ['d', 'b', 'c', 'd', 'e']   # pos = 2
        # L = ['e', 'b', 'c', 'd', 'e']   # pos = 3
        # L = ['f', 'b', 'c', 'd', 'e']   # pos = 4


unittest.main()