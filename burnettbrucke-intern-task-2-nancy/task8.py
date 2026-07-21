# Task 8: Exception Handling
# Create a program that accepts two numbers and performs division.
# Handle:
#  Division by zero
#  Invalid number input
#  Empty input
# Create one custom exception for negative numbers.

# Custom Exception
class NegativeNumberError(Exception):
    """Raised when a negative number is entered."""
    pass


try:
    # Take input
    num1 = input("Enter first number: ")
    num2 = input("Enter second number: ")

    # Check for empty input
    if num1 == "" or num2 == "":
        raise ValueError("Input cannot be empty.")

    # Convert input to float
    num1 = float(num1)
    num2 = float(num2)

    # Check for negative numbers
    if num1 < 0 or num2 < 0:
        raise NegativeNumberError("Negative numbers are not allowed.")

    # Perform division
    if num2==0:
        raise ZeroDivisionError("Divivsion by zero is not allowed")
    
    result = num1 / num2

except ValueError as e:
    print("Invalid Input:", e)

except ZeroDivisionError as e:
    print("Cannot divide by zero:",e)

except NegativeNumberError as e:
    print("Custom Exception:", e)

else:
    print("Division Result =", result)

finally:
    print("Program execution completed.")