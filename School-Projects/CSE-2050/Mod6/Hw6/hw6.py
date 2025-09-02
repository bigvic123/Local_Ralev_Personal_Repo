# TODO: implement the following 3 functions. Use docstrings, whitespace, and comments.

def cocktail_sort(L):
    """Cocktail sort"""
    start = 0
    end = len(L) - 1
    changed = True
    while changed:
        changed = False
        for j in range(start, end):
            #when the previous element is larger than the one after it, swap them
            if L[j+1] < L[j]:
                L[j+1], L[j] = L[j], L[j+1]
                changed = True
        if not changed:
            # it is sorted already
            break
        changed = False  # reset for the new check
        end -= 1
        for k in range (end-1, start-1, -1):
            #check for more swaps
            if L[k]>L[k+1]:
                L[k], L[k+1]=L[k+1], L[k]
                changed = True
        start += 1


def bs_sublist(L, left, right, item):
    """binary search of sublist"""
    while right-left>1:
        median = (right+left)//2
        #check which side the item falls under
        if item<L[median]:
            right = median
        else:
            #the left or right becomes the median depending on the value of item
            left = median
    
    #return the correct index of where item will be depending on size
    if item<= L[left]:
        return left-1
    if item>=L[left] and item<=L[right]:
        return left
    if item >= L[right]:
        return right


def opt_insertion_sort(L):
    """Insertion sort with binary search"""
    for i in range(len(L)):
        #find the index
        index = bs_sublist(L, len(L)-1-i, len(L)-1, L[0])
        #add temporary index
        L.append(-1)
        for j in range(len(L), index+1, -1):
            #move every index down
            L[j-1] = L[j-2]
        L[index+1]=L[0]
        #remove temporary index
        L.pop(0)
    return(L)

def insertion_sort(L):
    """Naive insertion sort. Adaptive, but still slow."""
    n = len(L)
    for j in range(n): # go through every item
        for i in range(n - 1 - j, n - 1): # bubble it into a sorted sublist
            if L[i] > L[i+1]:                 # 1 comparison
                L[i], L[i+1] = L[i+1], L[i]   # 2 writes 
            else:
                break
