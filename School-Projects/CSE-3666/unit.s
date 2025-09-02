uint2decstr:
    addi sp, sp, -8     # make room on the stack for saved registers
    sw ra, 4(sp)        # save the return address
    sw s0, 0(sp)        # save the base pointer

    # Initialize variables
    li t0, 10           # t0 = 10
    li t1, 0            # t1 = 0 (counter for the string length)
    mv t2, a0           # t2 = a0 (s pointer)
    mv t3, a1           # t3 = a1 (v value)

check:
    bge t3, t0, recur   # if v >= 10, jump to recursive call

    # Base case: add the last digit to the string
    addi t3, t3, '0'    # convert the last digit to its ASCII value
    sb t3, 0(t2)        # store the last digit at s[0]
    addi t1, t1, 1      # increment the string length
    addi t2, t2, 1      # increment the s pointer
    li t3, 0            # clear t3 (last digit)

    # Null-terminate the string and return
    sb zero, 0(t2)      # null-terminate the string
    addi t2, t2, -1     # move s pointer back to the last digit
    mv a0, t2           # return the address of s[1]
    lw ra, 4(sp)        # restore the return address
    lw s0, 0(sp)        # restore the base pointer
    addi sp, sp, 8      # free the space on the stack
    ret

recur:
    # Recursive case: call the function with v/10
    divu t4, t3, t0     # t4 = v/10
    mv a0, t2           # pass s pointer to the next call
    mv a1, t4           # pass v/10 to the next call
    jal ra, uint2decstr # call uint2decstr
    mv t2, a0           # update s pointer to the new string

    # Add the last digit to the string
    remu t3, t3, t0     # t3 = v%10 (last digit)
    addi t3, t3, '0'    # convert the last digit to its ASCII value
    sb t3, 0(t2)        # store the last digit at s[0]
    addi t1, t1, 1      # increment the string length
    addi t2, t2, 1      # increment the s pointer
    li t3, 0            # clear t3 (last digit)
    j check             # jump back to the check
