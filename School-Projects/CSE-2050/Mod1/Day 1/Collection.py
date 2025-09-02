int_1 = 3345465
float_1 = 3.4
bool_1 = True
############
#Collection
#set
set_1 = set()
set_2 = {1, 2, 3, 4, 'a'}
#Dict
dict_1 = dict()
dict_2 = {'a': 1, 'b': 'bb'}
print(dict_2['a'])
#str
str1_1 = ' '
str_2 = 'CSE2050'
#List
list_1 = []
list_2 = [1, 2, 3, 5, 7, 'abc', [7,8, 9]]
print(list_2)
#Tuples
tup_1 = tuple() #or ()
tup_2 = (2,3, 4,'a', (3, 4, 5))
#opperations on coll
#iteration
for elements in list_2:
    print(elements)
for key,values in dict_2.items():
    print(key,values)
for ele in tup_2:
    print("Tuples", ele)
#Slice
#[start:end]
list_3 = ["John", "Ava", "Bill", "Nancy"]
'''
print(list_3[0:3])
print(list_3[:2])
print(list_3[1:])
print("last element", list_3[-1])
print("kast three elemets : " list_3[-3])
print(list_3[1:-1])
'''
#Len
print(len(list_3))
#if statements
x=2
y=4
if x<y :
    print(str(x)+ ' is greater than '+ str(y))
elif x==y:
    print(str(x) + ' is equal to ' + str(y))
else :
    print(str(y)+ ' is greater than'+ str(x))

#Range
#range(start, stop, step)
#range(stop)
#range(start, stop)
list_5 = []
for w in range(0, 4, 2):
    list_5.append(w)
print(list_5)
list_6 = [ ]
for r in range(11):
    list_6.append(r)
print(list_6)

##########################
#Functions
def addition():
    x = 2
    y = 4
    print(x + y)


addition()

def adding(x, y=10):
    print("Addition")