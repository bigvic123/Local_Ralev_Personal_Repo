class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        pass

        #calculates the distance from origin
    def dist_from_origin(a):
        return (a.x**2+a.y**2)**.5

        #checks if the distances are equal
    def __eq__(self, p2):
        return(self.dist_from_origin()==p2.dist_from_origin())

        #checks if the distance is greater than the other distance
    def __gt__(self, p2):
        return(self.dist_from_origin()>p2.dist_from_origin())
    
        #checks if the distance is less than the other distance
    def __lt__(self, p2):
        return(self.dist_from_origin()<p2.dist_from_origin())

        #returns the point as a string
    def __str__(a):
        return "Point(" + str(a.x) + ", "+ str(a.y) + ")"
    

if __name__ == '__main__':
    p1 = Point(3, 4)
    p2 = Point(3, 4)
    p3 = Point(4, 3)
    p4 = Point(0, 1)

        #assertions to check if the program works
    assert p1 > p4
    assert not p4 > p3
    assert p4 < p2
    assert not p1<p4
    assert p1 == p3
    assert not p1 == p4
    assert str(p1) == "Point(3, 4)"
    assert str(p2) == "Point(3, 4)"
    assert p1.dist_from_origin() == 5.0
    assert p2.dist_from_origin() == 5.0

        #Printing functions
    print(str(p1))
    print(p1.dist_from_origin())