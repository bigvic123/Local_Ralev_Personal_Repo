from WordCompare import word_compare #importing function to find anagrams from WordCompare

words =  ["star", "rats", "arts", "eat", "ate", "tea", "orange", "port", "mate", "pool", "pile", "punt"]
expected_result = [['star', 'rats', 'arts'], ['rats', 'star', 'arts'], ['arts', 'star', 'rats'], ['eat', 'ate', 'tea'], ['ate', 'eat', 'tea'], ['tea', 'eat', 'ate'], ['orange'], ['port'], ['mate'], ['pool'], ['pile'], ['punt']]
def find_anagrams(words):
    anagrams = []#creating empty list to store anagrams
    for a in words:
        mylist = [a] 
        for b in words:
            if(word_compare(a, b)=="Anagram" and (a !=b)): #checking if its a anagram
                mylist.append(b) #adding to list if an anagram
        anagrams.append(mylist)

    return anagrams #returns all anagrams

#tests the function
assert find_anagrams(words) == expected_result
