#Task 8: Exception Handling
#Create a program that accepts two numbers and performs division.
#Handle:

#Division by zero
#Invalid number input
#Empty input
#Create one custom exception for negative numbers.

class NegativeNumberError(Exception):
    pass

try:
    num1 = (input("enter first number"))
    num2 = (input("enter second number"))

    if num1 == "" or num2 == "":
        raise ValueError("Empty input is not allowed")

    num1 = int(num1)
    num2 = int(num2)

    if num1 <0 and num2 < 0:
        raise NegativeNumberError("Negative numbers are not allowed")
    div = num1/num2

except (ZeroDivisionError):
    print("cannot divide by zero")

except ValueError:
    print("Invalid input. Please enter valid numbers.")

except NegativeNumberError as e:
    print(e)
else:
    print(f"division of {num1} and {num2} is {div}")