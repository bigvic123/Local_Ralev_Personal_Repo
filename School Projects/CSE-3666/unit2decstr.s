# uint2decstr - Convert unsigned number to a decimal string
# a0 = buffer address
# a1 = value

uint2decstr:
# Save the return address and the previous frame pointer
    addi    sp, sp, -12
    sw      s0, 0(sp)
    sw      ra, 4(sp)
    add     s0, x0, a0       # Save the buffer address in s0

    # Check if the value is greater than or equal to 10
    li      t0, 10
    bge     a1, t0, greater_than_10

    # If the value is less than 10, convert it to a character and return
    addi    a0, s0, 1        # Set a0 to point to the second character in the buffer
    addi    t1, a1, '0'      # Convert the value to a character
    sb      t1, 0(a0)        # Store the character in the buffer
    addi    a0, s0, 1        # Set a0 to point to the second character in the buffer
    jr      ra              # Return the address of the second character in the buffer

greater_than_10:
    # Recursively call the function with the value divided by 10
    addi    sp, sp, -8
    sw      s0, 0(sp)
    addi    a1, a1, -10      # Divide the value by 10
    jal     ra, uint2decstr  # Call the function recursively
    lw      s0, 0(sp)
    addi    sp, sp, 8

    # Calculate the remainder and store it in the buffer
    addi    a0, s0, 1        # Set a0 to point to the second character in the buffer
    remu    t2, a1, t0       # Calculate the remainder
    addi    t2, t2, '0'      # Convert the remainder to a character
    sb      t2, 0(a0)        # Store the character in the buffer

    # Null-terminate the string
    addi    a0, s0, 2        # Set a0 to point to the third character in the buffer
    sb      x0, 0(a0)        # Null-terminate the string

    # Return the address of the second character in the buffer
    addi    a0, s0, 1        # Set a0 to point to the second character in the buffer
    jr      ra              # Return the address of the second character in the buffer
