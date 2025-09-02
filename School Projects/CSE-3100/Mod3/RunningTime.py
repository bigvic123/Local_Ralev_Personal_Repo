
import time
import matplotlib.pyplot as plt

def dup1(L):
    for i in range(len(L)):               #run n times
        for j in range(len(L)):           #n
            if i != j and L[i] == L[j]:   #3
                return True               #1
    return False                          #1
                    #n(n(3+1))+1 = 4n^2 + 1 = O(n^2)
                                            # drop constant, pick largest term, put O  

def dup2(L):
    """for i in range(1, len(L)):            #run n times
        for j in range(i):                #n
            if L[i] == L[j]:              #1
                return True               #1
    return False """                         #1
                    #n(n(1+1))+1 = 4n^2 + 1 = O(n^2)
                                # drop constant, pick largest term, put O  
    return any (L[i] == L[j] for i in range(1, len(L)) for j in range(i))

def dup3(L):
    L.sort()                 #nlogn
    for i in range(len(L)):  #n
        if L[i]==L[i+1]:     #1
            return True      #1
    return False             #1
    #nlogn + n(1+1)+1 = nlogn
    sumx = 0
    for x in range(10000):
        sumx = sumx + x

def dup4(L):
    setL = set(L)           #n
    if len(setL) != len(L): #3
        return True         #1
    return False            #1
    #0(n)

def time_func(func, args):
    minVal = float('inf')
    for i in range(10):
        start = time.time()
        func(args)
        if time.time() - start < minVal :
            minVal = time.time() - start
    return minVal

if __name__ == "__main__":
    L1, L2, L3, L4 = [], [], [], []
    input = [10, 20, 49, 100, 150, 200]
    for n in input:

        L = [i for i in range (n)]
        L1.append(time_func(dup1, L)*1000)
        L2.append(time_func(dup2, L)*1000)
        L3.append(time_func(dup3, L)*1000)
        L4.append(time_func(dup4, L)*1000)

    plt.xlabel('input')
    plt.ylabel('Time')
    plt.plot(input, L1)
    plt.plot(input, L2)
    plt.plot(input, L3)
    plt.plot(input, L4)
    plt.legend(['O(n^2)', 'O(n^2) improved', 'O(nlogn)', 'O(n)'])