'''Task 8: Exception Handling
Create a program that accepts two numbers and performs division.
Handle:

Division by zero
Invalid number input
Empty input
Create one custom exception for negative numbers.'''

n1=int(input("enter a no: "))
n2=int(input("enter second no: "))
try:
    if n1<0 or n2<0:
        raise ValueError
    
    print("result:",n1/n2)
except ZeroDivisionError:
    print("division by zrero not allowed")

except ValueError:
    print("negative are not allowed")

finally :
    print("done")