#       CSE 3666 Lab 3: remove spaces

        .data
        # allocating space for both strings
str:    .space  128
res:    .space  128

        .globl  main

        .text
main:   
        # load address of strings 
        la      s0, str
        la      s1, res

        # we do not need LA pseudoinstructions from now on

        # read a string into str
        addi    a0, s0, 0 
        addi    a1, x0, 120  
        addi    a7, x0, 8
        ecall

        # str's addres is already in s0
        # copy res's address to a1
        addi    a1, s1, 0
        
        #copying adress to a1
        
        addi t2, x0, ' '
        
        loop:
        lb t0, 0(a0)
	addi a0, a0, 1
	#initialize counter t1 with value 0
	
	#check if space
	beq t0, t2, skip
	sb t0, 0(a1)
	addi a1, a1, 1
	#adding one to counter
	addi t1, t1, 1
	skip:
	bne t0, x0, loop
	
	addi a7, x0, 4
	sub a0, a1, t1
	ecall

        # TODO
	# remove spaces in str
	# print res
        # your code assumes str's address is in a0 and res's address is in a1
               
exit:   addi    a7, x0, 10
        ecall 
