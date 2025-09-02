import time

def time_f(func, args, num_trials):
    #Function for calculating time by subtracting the end time with the original
    mytime = [] 
    for i in range (num_trials):
        start = time.time()
        func(args)
        end = time.time() - start
        mytime.append(end)
    mytime.sort()
    return mytime[0]

def contains(myinput):
    for i in (myinput):
        if i == "100001":
            return True
    return False

def time_cont(myinput, num_trials):
    mytime = [] 
    for i in range (num_trials):
        start = time.time()
        contains(myinput)
        end = time.time() - start
        mytime.append(end)
    mytime.sort()
    return mytime[0]