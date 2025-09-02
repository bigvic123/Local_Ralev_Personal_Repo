import calc as cl
import math

print(cl._add(10, 10))
print(math.ceil(4.5))
while True:
    try:
        x = int(input("Enter a number "))
        print(cl.add(2, x))
        break
    except:
        print("Enter a valid number")
