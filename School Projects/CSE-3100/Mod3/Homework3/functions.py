import time
from tabulate import tabulate
from time_functions import time_f, time_cont
#Time functions in seperate file
def o1(mynum):
    #function with cost O(1)
    return(str(mynum))      #Cost O(1)

def on(mynum):
    #function with cost O(n)
    mylist = []
    for i in range (mynum):         #Cost O(n)
        mylist.append("2 ")          #Cost O(1)
    return mylist                    #Cost O(1)

def on2(mynum):
    #function with cost O(n^2)
    mylist = []
    for i in range (mynum^2):         #cost O(n^2)
        mylist.append("3 ")            #cost O(1)
    return mylist                      #cost O(1)

#Setting Up five trials
trial1 = ["100", str(1000*time_f(o1, 10, 100)), str(1000*time_f(on, 10, 100)), str(1000*time_f(on2, 10, 100))]
trial2 = ["200", str(1000*time_f(o1, 10, 200)), str(1000*time_f(on, 10, 200)), str(1000*time_f(on2, 10, 200))]
trial3 = ["400", str(1000*time_f(o1, 10, 400)), str(1000*time_f(on, 10, 400)), str(1000*time_f(on2, 10, 400))]
trial4 = ["600", str(1000*time_f(o1, 10, 600)), str(1000*time_f(on, 10, 600)), str(1000*time_f(on2, 10, 600))]
trial5 = ["800", str(1000*time_f(o1, 10, 800)), str(1000*time_f(on, 10, 800)), str(1000*time_f(on2, 10, 800))]

#Organizing data from five trials using table
myList = ["n", "t_const (ms)", "t_lin (ms)", "t_quad (ms)"]
print(tabulate([trial1, trial2, trial3, trial4, trial5], myList))

#Part 3
#Making Collections number 1-100000
list1 = []
tuple1 = ()
string1 = ""
set1 = {}
for i in range (100000):
    list1.append(i)
    myvalue = (i,)
    tuple1 = tuple1 + myvalue
    string1 = string1 + str(i)
    set1[i] = i

#Creating the second table
myList2 = ["n", "t_list", "t_tup", "t_str", "t_set"]
mytrial1 = ["10", str(1000*time_cont(list1, 10)), str(1000*time_cont(tuple1, 10)), str(1000*time_cont(string1, 10)), str(1000*time_cont(set1, 10))]

print(tabulate([mytrial1], myList2))