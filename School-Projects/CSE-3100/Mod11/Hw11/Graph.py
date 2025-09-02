from collections import defaultdict
import heapq

class Graph:
    def __init__(self, V=(), E=()):
        """Initializing Graph"""
        self._V = set()
        self._nbrs = dict()
        
        for i in V:
            self.add_vertex(i)
        for j in E:
            self.add_edge(j[0], j[1], j[2])

    def add_vertex(self, v):
        """Adds a vertex"""
        self._V.add(v)
        self._nbrs[v] = {}

    def remove_vertex(self, v):
        """Removes a vertex"""
        self._V.remove(v)

    def add_edge(self, u, v, wt):
        """Adds an edge"""
        self._nbrs[u][v] = wt
        self._nbrs[v][u] = wt
        
    def remove_edge(self, u, v):
        """Removes an edge"""
        del self._nbrs[u][v]
        del self._nbrs[v][u]

    def __iter__(self):
        """Magic method for iterating the vertices"""
        return iter(self._V)

    def nbrs(self, v):
        """Returns iterator over all neighbors"""
        return iter(self._nbrs[v])

    def get_wt(self, u, v):
        """Returns the weight between two nodes"""
        return self._nbrs[v][u]

    def fewest_flights(self, city):
        """Returns the smallest number of hops from city to all other nodes"""
        return self.breadth_first_search(city)

    def shortest_path(self, city):
        """Returns the shortest path from city to all other nodes"""
        return self.dijkstra(city)

    def minimum_salt(self, city):
        """Returns the shortest path to walk ove all nodes from city using the Prim's algorithm"""
        return self.min_spanning_tree(city)

    def min_spanning_tree(self, starting_node):
        """Returns the min spanning tree using the Prim's algorithm"""
        mst = defaultdict(set)
        visited = set([starting_node])
        edges = [
            (dist, starting_node, to)
            for to, dist in self._nbrs[starting_node].items()
        ]
        #heapify edges
        heapq.heapify(edges)
        total_dist = 0
        #go through all edges
        while edges:
            dist, frm, to = heapq.heappop(edges)
            if to not in visited:
                visited.add(to)
                mst[frm].add(to)
                total_dist += dist
                #if not visited, heappush the edge
                for to_next, dist in self._nbrs[to].items():
                    if to_next not in visited:
                        heapq.heappush(edges, (dist, to, to_next))
        return mst, total_dist

    def breadth_first_search(self, vertex):
        """returns BFS tree of the graph, i.e. fewest hops from node to node"""
        tree = {}
        hops = {}  # node -> how many hops to reach the node from vertex
        to_visit = [(None, vertex)]
        while to_visit:
            a, b = to_visit.pop(0)
            #cycle through tovisit until correct node is found
            if b not in tree:
                tree[b] = a
                hops[b] = hops[a] + 1 if a else 0
                for n in self.nbrs(b):
                    to_visit.append((b, n))

        return tree, hops

    def dijkstra(self, v):
        """Implements dijkstra alg. Returns the shortest path from v to all other nodes"""
        total = 0
        tree = {v: None}
        D = {u: float('inf') for u in self._V}  # changes all vertices to infinity
        D[v] = 0
        tovisit = PQ_OL(entries = [(u, D[u]) for u in self._V])
        for i in tovisit:
            #go through all nodes
            u = i.item
            for j in self._nbrs[u]:
                if D[u] + self.get_wt(u, j) < D[j]:
                    D[j] = D[u] + self.get_wt(u, j)
                    tree[j] = u
                    #Sort through all, change priority
                    tovisit.changepriority(j, D[j])
                    total += self.get_wt(u, j)
        return tree, D, total


# Priority Queue for Dijkstras algorithm
class Entry:
    def __init__(self, item, priority):
        self.priority = priority
        self.item = item

    def __lt__(self, other):
        return self.priority < other.priority

    def __eq__(self, other):
        return self.item == other.item and self.priority == other.priority


class PQ_OL:
    def __init__(self, entries):
        self._L = []
        for i in entries:
            self.insert(i[0], i[1])
        
    def __len__(self):
        return len(self._L)
        
    def insert(self, item, priority):
        self._L.append(Entry(item, priority))
        self._L.sort(reverse=True)

    def find_min(self):
        return self._L[-1]

    def remove_min(self):
        return self._L.pop()

    def changepriority(self, item, priority):
        for i in self._L:
            if i.item == item:
                i.priority = priority
        self._L.sort(reverse=True)

    def __iter__(self):
        yield from self._L