from MaxHeap import Entry, MaxHeap
import unittest, random, time
random.seed(658)

#TODO: Fill out any empty tests below
class TestEntry(unittest.TestCase):

    def test_gt_onepriority(self):
        """Tests Entry's with 1 priority"""
        self.e1 = Entry([0], "bob")
        self.e2 = Entry([1], "chris")
        self.assertTrue(self.e2 > self.e1)

    def test_gt_threepriorities(self):
        """Tests Entries with with 3 priorities"""
        self.e1 = Entry([1, "b", 1.56], "bob")
        self.e2 = Entry([1, "b", 2.46], "chris")
        self.assertTrue(self.e2 > self.e1)

    def test_gt_mismatchedpriorities(self):
        """Test comparisons b/w entries with different numbers of priorities"""
        self.e1 = Entry([2, "c"], "bob")
        self.e2 = Entry([1, "c", 1.4], "chris")
        self.assertTrue(self.e2 > self.e1)

    def test_eq(self):
        """Test that items w/ exact same priorities are seen as equal"""
        self.e1 = Entry([0, "d", 2], "bob")
        self.e2 = Entry([0, "d", 2], "chris")
        self.assertTrue(self.e2 == self.e1)

class TestMaxHeap(unittest.TestCase):
    def test_add_remove_single(self):
        """Add a single item to the max heap, then remove it. This test is provided for you as an example."""
        e1 = Entry(priority=[0], item="jake")
        mh = MaxHeap()
        self.assertEqual(len(mh), 0)
        mh.put(e1)
        self.assertEqual(len(mh), 1)
        self.assertEqual(mh.remove_max(), "jake")

    def test_add_remove_random(self):
        """Add and remove many random items w/ same number of priorities"""
        mheap = MaxHeap()
        mylist = [i for i in range(100)]
        random.shuffle(mylist)
        for i in mylist:
            temp = Entry([1], str(i))
            mheap.put(temp)
        for i in range(100):
            mheap.remove_max()

    def test_add_remove_several(self):
        """Add and remove several items with different numbers of priorities"""
        mheap = MaxHeap()
        e1 = Entry([1], "abe")
        e2 = Entry([2], "bob")
        e3 = Entry([3], "chris")
        e4 = Entry([4], "dan")
        e5 = Entry([5], "elle")
        mheap.put(e1)
        mheap.put(e2)
        mheap.put(e3)
        mheap.put(e4)
        mheap.put(e5)
        self.assertEqual("elle", mheap.remove_max())
        self.assertEqual("dan", mheap.remove_max())
        self.assertEqual("chris", mheap.remove_max())
        self.assertEqual("bob", mheap.remove_max())
        self.assertEqual("abe", mheap.remove_max())

    def test_removefromempty(self):
        """Test Runtime error when removiung from empty"""
        mheap = MaxHeap()
        self.assertEqual(None, mheap.remove_max())

    # NOTE: This times heapify_up and _down, but does not test their functionality
    def test_heapify(self):
        """Times heapify up and heapify down approaches. This 'test' provided for you"""
        print() # an extra blank line at the top
        
        # table header
        print('='*40)
        print(f"{'n':<10}{'t_h_up (ms)':<15}{'t_h_down (ms)':<15}"   )
        print('-'*40)

        # table body
        scalar = int(1E3)
        for n in [i*scalar for i in [1, 2, 3, 4, 5]]:
            t_h_up = 1000*time_f(MaxHeap, (list(range(n)), 'up'))
            t_h_down = 1000*time_f(MaxHeap, (list(range(n)), 'down'))
            print(f"{n:<10}{t_h_up:<15.2g}{t_h_down:<15.2g}")

        # table footer
        print("-"*40)

def time_f(func, args, trials=5):
    """Returns minimum time trial of func(args)"""
    t_min = float('inf')

    for i in range(trials):
        start = time.time()
        func(*args)
        end = time.time()
        if end-start < t_min: t_min = end - start

    return t_min

unittest.main()