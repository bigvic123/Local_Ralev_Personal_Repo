def word_compare(x, y = "steal"):
    #checks if at least one is an int
    if ((isinstance(x, int) or isinstance(y, int))):
        return("Those aren't strings!")
    #sorts x and y, checking for anagrams
    elif(sorted(x) == sorted(y)):
        return("Anagram")
    #since they are strings but not anagrams, it prints the tuple
    else:
        mytuple = (x, y)
        return(mytuple)
    