def o1():
    #function with cost O(1)
    return("1 ")      #Cost O(1)

def on(mynum):
    #function with cost O(n)
    mystr = ""
    for i in range (mynum):         #Cost O(n)
        mystr.append("2 ")          #Cost O(1)
    return mystr                    #Cost O(1)

def on2(mynum):
    #function with cost O(n^2)
    mystr = ""
    for i in range (mynum^2):         #cost O(n^2)
        mystr.append("3 ")            #cost O(1)
    return mystr                      #cost O(1)
print(o1)
print(on(4))
print(on2(3))