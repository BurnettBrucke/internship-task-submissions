# Task 8: Exception Handling
# Create a program that accepts two numbers and performs division.
# Handle:
# Division by zero
# Invalid number input
# Empty input
# Create one custom exception for negative numbers.

# Custom Exception
class NegativeNumberError(Exception):
    pass

try:
    num1 = input("Enter first number: ")
    num2 = input("Enter second number: ")

    # Check for empty input
    if num1 == "" or num2 == "":
        raise ValueError("Input cannot be empty.")

    # Convert to float
    num1 = float(num1)
    num2 = float(num2)

    # Check for negative numbers
    if num1 < 0 or num2 < 0:
        raise NegativeNumberError("Negative numbers are not allowed.")

    # Perform division
    result = num1 / num2

# handle Invalid number input
except ValueError: 
    print("Invalid Input: Please write only Integer Value")

# handle division by zero

except ZeroDivisionError:
    print("Division by zero is not allowed.")

# Custom Exception
except NegativeNumberError as e:
    print("Custom Exception:", e)

else:
    print("Result =", result)
