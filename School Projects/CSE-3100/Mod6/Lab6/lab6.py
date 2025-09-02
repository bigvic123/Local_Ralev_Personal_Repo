class OrderedList:
    def __init__(self, items=None):
        """Initialize an ordered list. If `items` is specified, the OrderedList starts with the items in that collection"""
        self._L = sorted(list(items)) if items is not None else list()
            
    def add(self, item):
        """adds item to the list"""
        self._L.append(item)
        self._L.sort()

    def remove(self, item):
        """removes the first occurrence of item from the list. Raise a RuntimeError if the item is not present."""
        if not item in self: raise RuntimeError(f"{item} not in OrderedList")

        self._L.remove(item) # O(n) to find, then O(n) to remove

    def __getitem__(self, index):
        """returns the item with the given index in the sorted list. This is also known as selection."""
        return self._L[index]

    def __iter__(self):
        """returns an iterator over the ordered list that yields the items in sorted order. Required for `for` loops."""
        return iter(self._L)

    def __len__(self):
        """returns the length of the ordered list."""
        return len(self._L)

    def __contains__(self, item):
        """returns true if there is an item of the list equal to item."""
        return self._bs(item, 0, len(self)) # You'll have to implement _bs() for this to work

        # The lines below implement contains with different algs.
        # Feel free to try them out, but they are both too slow
        # to pass the tests in gradescope (O(n) instead of O(logn).

        # return self._contains_list(item)  # uses python's default list-search
        # return self._contains_bs_slow(item)    # uses a slow version of binary-search (slicing)

    def _contains_list(self, item):
        """returns True iff there is an item of the list equal to item."""
        return item in self._L # Works, but slow (O(n))

    def _contains_bs_slow(self, item):
        return self.__contains_bs_slow(self._L[:], item)
    
    def __contains_bs_slow(self, L, item):
        """searches L for item. This is slow since it slices L at every level of recursion"""
        # base case - item not in list
        if len(L) == 0: return False            

        median = len(L) // 2

        # base case - we found the item
        if item == L[median]: return True

        # item is in smaller half
        elif item < L[median]: return self.__contains_bs_slow(L[:median], item)
        
        # item is in bigger half
        else: return self.__contains_bs_slow(L[median + 1:], item)



    # TODO: Implement O(logn) binary search
    def _bs(self, item, left, right):
        """searches for item using `left` and `right` indices instead of slicing"""
        # base case - item not in list
        median = (left+right)//2
        if(right-left==0):
            return False
        # base case: found item
        if(self._L[median] == item):
            return True
        # item is in smaller half
        elif(self._L[median] > item):
            return self._bs(item, left, median)
        # item is in bigger half
        else:
            return self._bs(item, median+1, right)
