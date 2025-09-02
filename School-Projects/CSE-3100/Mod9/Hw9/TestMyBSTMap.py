import unittest, random
from MyBSTMap import MyBSTMap

class TestMyBSTMap(unittest.TestCase):
    def test_equal_empty(self):
        """Tests that two empty trees are equal"""
        bst1 = MyBSTMap()
        bst2 = MyBSTMap()
        self.assertTrue(bst1 == bst2)

    def test_equal_multiplenodes(self):
        """Tests that two multiple node trees are equal"""
        bst1 = MyBSTMap()
        bst2 = MyBSTMap()
        for i in [0, 1, 2, 3]: 
            bst1.put(i)
            bst2.put(i)
        self.assertTrue(bst1 == bst2)

    def test_notequal_multiplenodes_difshapes(self):
        """Tests that two trees same shape different key value pairs are not equal"""
        bst1 = MyBSTMap()
        bst2 = MyBSTMap()
        for i in [4, 2, 6, 1]: 
            bst1.put(i)
        for i in [4, 1, 2, 6]: 
            bst2.put(i)
        self.assertFalse(bst1 == bst2)
    
    def test_notequal_multiplenodes_difkvs(self):
        """Tests that two trees different shape are not equal"""
        bst1 = MyBSTMap()
        bst2 = MyBSTMap()
        for i in [0, 1, 2, 3]: 
            bst1.put(i)
        for i in [2, 3, 4, 5]: 
            bst2.put(i)
        self.assertFalse(bst1 == bst2)

    def test_frompreorder_small(self):
        """Tests frompreorder for small list"""
        bst1 = MyBSTMap()
        for i in (4, 1, 2, 3):
            bst1.put(i)
        bst2 = MyBSTMap()
        myL = [j for j in bst1.preorder()]
        bst2 = MyBSTMap.frompreorder(myL) 
        self.assertTrue(bst1 == bst2)

    def test_frompreorder_large(self):
        """Tests frompreorder for large list"""
        bst1 = MyBSTMap()
        myL = [i for i in range(1,100)]
        random.shuffle(myL)
        for j in myL:
            bst1.put(j, str(j))
        bst2 = MyBSTMap()
        myL = [k for k in bst1.preorder()]
        bst2 = MyBSTMap.frompreorder(myL) 
        self.assertTrue(bst1 == bst2)

    def test_frompostorder_small(self):
        """Tests frompostorder for small list"""
        bst1 = MyBSTMap()
        for i in (4, 1, 2, 3):
            bst1.put(i, str(i))
        bst2 = MyBSTMap()
        myL = [j for j in bst1.postorder()]
        bst2 = MyBSTMap.frompostorder(myL)
        self.assertTrue(bst1 == bst2)

    def test_frompostorder_large(self):
        """Tests frompostorder for large list"""
        bst1 = MyBSTMap()
        myL = [i for i in range(1,100)]
        random.shuffle(myL)
        for j in myL:
            bst1.put(j, str(j))
        bst2 = MyBSTMap()
        myL = [k for k in bst1.postorder()]
        bst2 = MyBSTMap.frompostorder(myL) 
        self.assertTrue(bst1 == bst2)

unittest.main()