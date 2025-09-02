#dictionaries cannot have lists
d = {8:"John", "id":4565, "grades":[90,98]}
#set element
#d["Dob"] = 2002 ---> same as -->
d.__setitem__("Dob", 2002)

#get element
#print(d["id"])  --> same as -->
print(d.__getitem__("id"))

#keys
print(d.keys()) #--> same as -->
for keys in d.keys():
    print(keys)

#values
print(d.values())
for v in d.values():
    print(v)

#items
print(d.items())
for k, v in d.items():
    print(k, v)


#Notes
#Dictionaries have a Hash table with elements called buckets
#Make a hash function  
#use these functions to add or get from the hash function
#h(k) = k 
#if k1!=k2 but h(k1)=h(k2) is hash collision 
#sperate chaining = have the buckets be many short lists instead of one long one
#using % you can store elements sorted by list
#time complexity of O(1)