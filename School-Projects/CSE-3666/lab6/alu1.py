from myhdl import block, always_comb

@block
def ALU1bit(a, b, carryin, binvert, operation, result, carryout):

    """ 1-bit ALU

    result and carrayout are output

    all other signals are input

    operation:
    0:  AND
    1:  OR
    2:  ADD/SUB
    3:  0
    """
    # this implementation does not follow the requirements of the alu1 lab. 

    @always_comb 
    def alu1_logic():
        if operation == 0:
            result.next = a and b
        elif operation == 1:
            result.next = a or b
        elif operation == 2:
            if binvert:
                res_add =  a + carryin + (not b)
            else:
                res_add =  a + carryin + b
            result.next = res_add & 1
            carryout.next = bool(res_add & 2)
        else:
            result.next = 0

    # return the logic  
    return alu1_logic
