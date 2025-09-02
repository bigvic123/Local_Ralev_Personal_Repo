from WordCompare import word_compare #importing function to find anagrams from WordCompare

words =  ["star", "rats", "arts", "eat", "ate", "tea", "orange", "port", "mate", "pool", "pile", "punt"]
expected_result = [['star', 'rats', 'arts'], ['rats', 'star', 'arts'], ['arts', 'star', 'rats'], ['eat', 'ate', 'tea'], ['ate', 'eat', 'tea'], ['tea', 'eat', 'ate'], ['orange'], ['port'], ['mate'], ['pool'], ['pile'], ['punt']]
def ListToString(t):
    str1 = ''
    for ele in t:
        str1 += ele

    return str1

def find_anagrams(words):
    anagrams = []#creating empty list to store anagrams
    for a in words:
        #adding anagrams, formatting
        mylist = [a + ": ['"] 
        my_num = 0
        for b in words:
            if(word_compare(a, b)=="Anagram" and (a !=b)): #checking if its a anagram
                mylist.append(b) #adding to list if an anagram
                my_num + 1
                if(my_num != 1):#adding comma or paranthasee
                    mylist.append("', '")
                elif(my_num == 1):
                    mylist.append("']")
        anagrams.append(mylist)

    #formatting the anagrams so they fit the requirement
    mystring = ''
    #appending line breaks and turning list into string
    for c in anagrams:
        mystring = mystring + ListToString(c) + "\n"
    
    return mystring #returns all anagrams

#tests the function
#assert find_anagrams(words) == expected_result
print(find_anagrams(words))
