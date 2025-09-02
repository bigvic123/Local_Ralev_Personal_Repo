from BSTMap import BSTMap, BSTNode # provided for you

# Inherit from BSTMap, but overload `newnode` to use this one instead
class MyBSTMap(BSTMap):
    
    def newnode(self, key, value = None): 
        return MyBSTNode(key, value)    # overloads the `newnode` method to use MyBSTNode() instead of BSTNode()

    # TODO: implement the three methods below
    def __eq__(self, other):
        """Checks if two trees are equal in shape and kvs"""
        if self.root and other.root:
            for n, o in zip(self.preorder(), other.preorder()):
                if n != o:
                    return False
            return True
        return self.root is None and other.root is None

    @staticmethod
    def _frompreorder(L, i, low, high):
        if i >= len(L):
            return i, None
        key, value = L[i]
        node = None
        if low < key < high:
            node = BSTNode(key, value)
            i += 1
            if i >= 0:
                i, node.left = MyBSTMap._frompreorder(L, i, low, key)
                i, node.right = MyBSTMap._frompreorder(L, i, key, high)
        return i, node

    @staticmethod
    def frompreorder(L):
        """Returns BST using pre-order list"""
        bst1 = BSTMap()
        i, bst1.root = MyBSTMap._frompostorder(L, 0, -2 ** 31, 2 ** 31)
        return bst1

    @staticmethod
    def _frompostorder(L, i, low, high):
        if i < 0:
            return i, None
        key, value = L[i]
        node = None
        if low < key < high:
            node = BSTNode(key, value)
            i -= 1
            if i >= 0:
                i, node.right = MyBSTMap._frompostorder(L, i, key, high)
                i, node.left = MyBSTMap._frompostorder(L, i, low, key)
        return i, node

    @staticmethod
    def frompostorder(L):
        """Returns BST using post-order list"""
        bst1 = BSTMap()
        i, bst1.root = MyBSTMap._frompostorder(L, len(L)-1, -2**31, 2**31)
        return bst1

class MyBSTNode(BSTNode):
    
    newnode = MyBSTMap.newnode  # overloads the `newnode` method to use the correct Node class

    def __eq__(self, other):
        """Checks if two nodes are equal (key and value)"""
        return self.key == other.key and self.value == other.value