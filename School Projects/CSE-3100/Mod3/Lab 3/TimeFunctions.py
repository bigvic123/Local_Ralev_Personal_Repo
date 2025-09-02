import time
def time_function(func, args, n_trials = 10):
    mytime = [] #storing multiple trials in an array
    for i in range (n_trials):
        start = time.time()
        func(args)
        end = time.time() - start # subtracting time before from total time to get the time of the function
        mytime.append(end)

    mytime.sort() #find out the smallest time by sorting
    return mytime[0]
    
def time_function_flexible(f, args, n_trials = 10):
    mytime = [] #storing multiple trials in an array
    for i in range (n_trials):
        start = time.time()
        foo(f, args)
        end = time.time() - start # subtracting time before from total time to get the time of the function
        mytime.append(end)

    mytime.sort() #find out the smallest time by sorting
    return mytime[0]

def foo(f, args):
    #this function unpacks the tuple
    return f(*args)

if __name__ == '__main__':
    # Some tests to see if time_function works
    def test_func(L):
        for item in L:
            item *= 2

    L1 = [i for i in range(10**5)]
    t1 = time_function(test_func, L1)

    L2 = [i for i in range(10**6)] # should be 10x slower to operate on every item
    t2 = time_function(test_func, L2)

    print("t(L1) = {:.3g} ms".format(t1*1000))
    print("t(L2) = {:.3g} ms".format(t2*1000))