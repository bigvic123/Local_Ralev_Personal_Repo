def _add(x, y):
    c = x+y
    return c

def subtract(x, y):
    c = x-y
    return c

def multi(x, y):
    c = x*y
    return c

def div(x, y):
    c = x/y
    return c

if __name__ == "__main__":
    x = 5
    y = 8
    res = _add(x, y)
    #print("Results: ", res)
    #print(sub(x, y))
    assert(subtract(10, 5)==5)
    assert (_add(6, 6) == 12)
    print(res)