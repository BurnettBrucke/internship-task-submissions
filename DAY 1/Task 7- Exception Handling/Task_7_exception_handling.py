# Create a program that accepts two numbers and performs division

# Handle:
# Division by zero
# Invalid number input
# Empty input
# Create one custom exception for negative numbers.

# Custom exception
class NegativeNumberError(Exception):
    pass
class EmptyInput(Exception):
    pass

try:
    num1 = input("Enter first number: ")
    num2 = input("Enter second number: ")

    # Check empty input
    if num1 == "" or num2 == "":
        raise EmptyInput("Input cannot be empty")

    # Convert input into numbers
    num1 = float(num1)
    num2 = float(num2)

    # Check negative numbers
    if num1 < 0 or num2 < 0:
        raise NegativeNumberError("Negative numbers are not allowed")

    # Division
    result = num1 / num2

    print("Result: ", result)


except ZeroDivisionError:
    print("Error: Cannot divide by zero")

except EmptyInput:
    print("Error: Input cannot be empty")

except ValueError:
    print("Error: Please enter valid numbers")

except NegativeNumberError:
    print("Error: Negative numbers are not allowed")
