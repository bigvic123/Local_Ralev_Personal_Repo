class BSTNode:
    def __init__(self, key, left=None, right=None):
        self.key = key
        self.left = left
        self.right = right
    
    # classical iteration (correct but slow)
    def __iter__(self): return BSTNode_Iterator(self)

    # generator based iteration (fast)
    def in_order(self):
        if self.left is not None: yield from self.left.in_order()   # recursively go left
        yield self.key                                              # return this key
        if self.right is not None: yield from self.right.in_order() # recursively go right

    # TODO: Uncomment this, so Python knows how to print out Nodes
    def __repr__(self):
        return f"BSTNode(key={self.key})"

    # TODO: implement the below methods
    def put(self, key): 
        if self.key == key:
            return
        elif self.key > key:
            if self.left: self.left.put(key)
            else: self.left = BSTNode(key)
        elif self.key < key:
            if self.right: self.right.put(key)
            else: self.right = BSTNode(key)
    
    def pre_order(self):
        yield self.key
        if self.left is not None: yield from self.left.pre_order()
        if self.right is not None: yield from self.right.pre_order()

        
    def post_order(self):
        if self.left is not None: yield from self.left.post_order()
        if self.right is not None: yield from self.right.post_order()
        yield self.key
    

# This technique is slow. We have to queue up the ENTIRE tree before we start 
# returning nodes. See above BSTNode.in_order() for an example that yields
# nodes one at a time without queueing up the whole tree.
class BSTNode_Iterator:
    def __init__(self, node):
        self.queue = []
        self.in_order(node) # Queues up the entire tree
        self.counter = 0

    # in_order traversal/queueing
    def in_order(self, node):
        if node.left is not None: self.in_order(node.left)
        self.queue.append(node)
        if node.right is not None: self.in_order(node.right)

    # Update counter, return item, repeat
    def __next__(self):
        if self.counter < len(self.queue):
            self.counter += 1
            return self.queue[self.counter-1].key
        
        raise StopIteration

