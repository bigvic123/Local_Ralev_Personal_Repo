import sys

def price_to_profit(L):
    """Convert prices to profits"""
    mylist = [0]
    #for all items subtracting element with previous element
    for i in range(len(L)-1):
        mylist.append(L[i+1]-L[i])
    return mylist


# brute force solution
def max_profit_brute(L):
    """Finds maximum profit. Assumes L is a list of profits (i.e. change in price every day), not raw prices"""
    n = len(L)
    max_sum = 0 # assume we can at least break even - buy and sell on the same day

    # outer loop finds the max profit for each buy day
    for i in range(n):
        # total profit if we bought on day i and sold on day j
        total = L[i]
        if total > max_sum: max_sum = total
        
        for j in range(i+1, n): 
            total += L[j] # total profit if we sell on day j
                          # we assume L[j] is the profit if we bought on day j-1 and sold on day j
                          # i.e., L is the change in value each day, relative to the day before
            if total > max_sum: max_sum = total

    return max_sum

def max_profit(L):  # O(nlogn)
    """Return the max profit"""
    # profits = price_to_profit(L)
    r = max_profit_helper(L, 0, len(L))
    print(f"profit={r[0]}, buy={r[1]}, sell={r[2]}")
    return r[0]

# you'll need a helper function or default parameters here
def max_profit_helper(L, left: int, right: int):  # O(nlogn)
    """Helper function to find the max profit recursively, L is profits"""
    # BASE CASE
    #    Only 1 item? Max profit is easy - it's the profit if we bought the day before and sold today
    if left >= right:
        return [0, left - 1, left]
        #raise Exception (f"left={left} >= right={right}")
    if right-left == 1:
        return [L[left], left, right]

    # DIVIDE and CONQUER:
    midpoint = (left + right)//2
    # find the max profit if we buy and sell in the left (recursive call)
    p1 = max_profit_helper(L, left, midpoint)
    # find the max profit if we buy and sell in the right (recursive call)
    p2 = max_profit_helper(L, midpoint + 1, right)
    # find the max profit if we buy in the left and sell in the right (requires a separate function)
    p3 = max_profit_crossing(L, left, right, midpoint)

    # COMBINE subproblems into the solution for this level of recursion
    #return largest profit
    if p1[0] >= p2[0]:
        if p1[0] >= p3[0]:
            # p1 is max
            return p1
        else:
            return p3
    else:
        if p2[0] >= p3[0]:
            return p2
        else:
            return p3

def max_profit_crossing(L, left, right, median):
    '''Returns a triple (max profit, buy index, sell index)'''
    # L is already profit
    # O(n): Max profit if we sell on the median?
    
    pa = -sys.float_info.max
    i_left = median - 1
    sum = 0
    #add all items before the medium, move index if over pa
    for i in range(median-1, left-1, -1):
        sum += L[i]
        if sum > pa:
            pa = sum
            i_left = i
    # O(n): Max profit if we buy on the median?
    pb = -sys.float_info.max
    i_right = median
    sum = 0
    #add all items after the medium, move index if over pb 
    for i in range(median, right):
        #print(f"i={i}, len={len(L)}, midpoint={median} rigth={right}")
        sum += L[i]
        if sum > pb:
            pb = sum
            i_right = i
    # O(1): Max profit if we buy before and sell after?
    # since pa >=0 and pb >=0 (the way it is written), then pa + pb is always the max profit 
    p = pa
    #fixing the indecese
    r_left = i_left
    r_right = median-1
    #correct value for return
    if pb>p:
        p = pb
        r_left = median
        r_right = i_right
    if (pb+pa)>p:
        p = pa+pb
        r_left = i_left
        r_right = i_right   
    return [p, r_left, r_right]


