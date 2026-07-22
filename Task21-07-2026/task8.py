'''Task 8: Exception Handling
Create a program that accepts two numbers and performs division.
Handle:

Division by zero
Invalid number input mean value error 
Empty input
Create one custom exception for negative numbers.'''


try:
    a=int(input("Enter first number:"))
    b=int(input("Enter second number:"))
    result=a/b
except ZeroDivisionError:
    print("Not Divided by zero")
except ValueError:
    print("Enter only number")


