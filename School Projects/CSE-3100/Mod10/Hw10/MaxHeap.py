class Entry:
    def __init__(self, priority, item):
        """Initializing Variables"""
        self.priority = priority 
        self.item = item

    def __gt__(self, other):
        """Returns which of two items is greater"""
        #multiple data types needs more checks
        if len(self.priority) == len(other.priority):
            for i in range(len(self.priority)):
                if self.priority[i] > other.priority[i]:
                    return True
        if len(self.priority) > len(other.priority):
            return True
        if len(self.priority) < len(other.priority):
            return False
        return False

    def __eq__(self, other):
        """Returnd if two items are equal"""
        if len(self.priority) != len(other.priority):
            return False
        for i in range(len(self.priority)):
            if self.priority[i] != other.priority[i]:
                return False
        return True

    # repr is provided for you
    def __repr__(self):
        """Returns string representation of an Entry """
        return f"Entry(priority={self.priority}, item={self.item})"



# TODO: _heapify_up, _heapify_down, put, remove_max
class MaxHeap:
    # init is provided for you, but you should modify the default `heapify_direction` value
    def __init__(self, items=None, heapify_direction=None):
        """Initializes a new MaxHeap with optional collection of items"""
        self._L = []

        # if a collection of items is passed in, heapify it
        if items is not None:
            self._L = list(items)
            if heapify_direction == 'up': self._heapify_up()

            elif heapify_direction == 'down': self._heapify_down()

            else: raise RuntimeError("Replace `heapify_direction` default with 'up' or 'down' instead of `None`")

    def _heapify_up(self):
        """Heapifies self._L in-place using only upheap"""
        #start from bottom, check with parrent, if it is larger
        #switch the two nodes
        for i in range(len(self._L) // 2):
            self._upheap(len(self._L) - i - 1)

    def _heapify_down(self):
        """Heapifies self._L in-place using only downheap"""
        #start from root, check with child, if is smaller, swap with
        #largest of the children
        for i in range(len(self._L) // 2):
            self._downheap(i)

    def put(self, entry):
        """Used to put an entry into PQ and then upheaps into the BST"""
        #add item, upheap to align list
        self._L.append(entry)
        self._upheap(len(self._L) - 1)

    def remove_max(self):
        """Used to remove the node with highest priority"""
        if len(self._L) == 0:
            return None
        #find max, move to index zero, pop index zero, downheap and return
        item = self._L[0]
        self._L[0] = self._L[-1]
        self._L.pop()
        self._downheap(0)
        return item.item

    # len is number of items in PQo
    def __len__(self):
        """Number of items in PQ"""
        return len(self._L)

    def _swap(self, a, b):
        """swaps indices"""
        self._L[a], self._L[b] = self._L[b], self._L[a]

    def _upheap(self, i):
        """sorts item bottom to top into MaxHeap"""
        self._parent(i)
        #if child larger than parent, must swap, upheap
        if i > 0 and self._L[i] > self._L[self._parent(i)]:
            self._swap(i, self._parent(i))
            self._upheap(self._parent(i))

    def _downheap(self, i):
        """sorts item top to bottom into MaxHeap"""
        if self._children(i):
            #if any children exist, take largest one for comparison
            child = max(self._children(i), key = lambda x: self._L[x])
            #if parent smaller than child, must swap, upheap
            if self._L[child] > self._L[i]:
                self._swap(i, child)
                self._downheap(child)

    def _parent(self, i):
        """returns the index of the parent"""
        return (i - 1) // 2
    
    def _children(self, i):
        """returns the range of the children of the parent"""
        #to find child, multiply parent index by 2, add one for left, 2 for right
        left = 2 * i + 1
        right = 2 * i + 2
        return range(left, min(len(self._L), right + 1))

    