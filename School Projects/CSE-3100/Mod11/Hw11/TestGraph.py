from Graph import Graph, PQ_OL, Entry
import unittest

#My Cities:
#San Francisco ---2873 mi--- Philadelphia --- 215 mi --- Hartford-|
#|                                                                |
#| 458 mi                                                         | 306 mi
#|                                                                |
#San Diego --------- 2630 mi ------ Baltimore --------------------|

class test_Graph(unittest.TestCase):
    # Create a graph `self.g` that you can use in your other unittests. Include ASCII art.
    def setUp(self):
        """Setting up the graph"""
        V = {'San Francisco', 'Philadelphia', 'Hartford', 'Baltimore', 'San Diego'}
        E = {('San Francisco', 'Philadelphia', 2873), ('Philadelphia', 'Hartford', 215), ('Hartford', 'Baltimore', 306), ('Baltimore', 'San Diego', 2630), ('San Diego', 'San Francisco', 458)}
        self.g = Graph(V, E)
    # TODO: Add unittests for public interface of Graph class (except traversal algs)
        
    def test_add_vertex(self):
        self.setUp()
        c = 'city'
        self.g.add_vertex(c)
        self.assertTrue(c in self.g._V)

    def test_remove_vertex(self):
        self.setUp()
        c = 'city'
        self.g.add_vertex(c)
        self.assertTrue(c in self.g._V)
        self.g.remove_vertex(c)
        self.assertTrue(c not in self.g._V)

    def test_add_remove_edge(self):
        self.setUp()
        c1 = 'city1'
        c2 = "city2"
        self.g.add_vertex(c1)
        self.g.add_vertex(c2)
        self.g.add_edge(c1, c2, 100)
        self.assertEqual(self.g.get_wt(c1, c2), 100)
        self.g.remove_edge(c1, c2)
        try:
            wt = self.g.get_wt(c1, c2)
            self.assertTrue(False)
        except KeyError:
            self.assertTrue(True)

    def test_iter(self):
        self.setUp()
        for n in self.g.nbrs("Philadelphia"):
            self.assertTrue(n == "Hartford" or n == "San Francisco")

class test_GraphTraversal(unittest.TestCase):
    # Create a graph `self.g` that you can use in your other unittests. Include ASCII art.
       
    def setUp(self):
        """Setting up the graph"""
        V = {'San Francisco', 'Philadelphia', 'Hartford', 'Baltimore', 'San Diego'}
        E = {('San Francisco', 'Philadelphia', 2873),
             ('Philadelphia', 'Hartford', 215),
             ('Hartford', 'Baltimore', 306),
             ('Baltimore', 'San Diego', 2630),
             ('San Diego', 'San Francisco', 458)}
        self.g = Graph(V, E)

    # TODO: Which alg do you use here, and why?
    # Alg: BFS.
    # Why: BFS walks the nodes with least number of hops (edges).
    def test_fewest_flights(self):
        """Testing fewest flights (the lowest number of hops between vertexes)"""
        self.setUp()
        tree, hops = self.g.fewest_flights('Philadelphia')
        self.assertEqual(hops["Baltimore"], 2)
        
    # TODO: Which alg do you use here, and why?
    # Alg: Djikstras.
    # Why: Finds shortest path between the argument vertex and every other node.
    def test_shortest_path(self):
        """Testing we can find the shortest path"""
        tree, D, dist = self.g.shortest_path("Philadelphia")
        self.assertEqual(D["Hartford"], 215)
        self.assertEqual(D["San Francisco"], 2873)
        self.assertTrue(dist == 3088)

    # TODO: Which alg do you use here, and why?
    # Alg: Prim's Algorithm.
    # Why: It returns a tree that shows how walk all vertexes of the graph minimizing the total distance.
    def test_minimum_salt(self):
        """Testing we can find the minimum salt, i.e. min total miles to walk the graph"""
        self.setUp()
        mst, dist = self.g.minimum_salt('Philadelphia')
        self.assertTrue(dist == 3609)

unittest.main()