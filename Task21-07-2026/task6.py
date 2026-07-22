'''Task 6: Functions
Create separate functions for:

Checking whether a number is prime.
Calculating the factorial of a number.
Checking whether a number is even or odd.
Finding the largest number from a list.
Calculating the average of a list of numbers.
Use type hints and docstrings in every function.'''

def is_prime(number):

    if number <= 1:
        return False

    for i in range(2, int(number ** 0.5) + 1):
        if number % i == 0:
            return False

    return True


def factorial(number):

    if number < 0:
        print("Factorial is not defined for negative numbers.")
        return

    result = 1

    for i in range(1, number + 1):
        result *= i

    return result


def even_or_odd(number):

    if number % 2 == 0:
        return "Even"
    else:
        return "Odd"


def largest_number(numbers):

    if len(numbers) == 0:
        print("List cannot be empty.")
        return

    return max(numbers)


def average(numbers):

    if len(numbers) == 0:
        print("List cannot be empty.")
        return

    return sum(numbers) / len(numbers)

num = int(input("Enter a number: "))

print("\nPrime Number :", is_prime(num))
print("Factorial :", factorial(num))
print("Even/Odd :", even_or_odd(num))

numbers = list(map(int, input("\nEnter numbers separated by space: ").split()))

print("Largest Number :", largest_number(numbers))
print("Average :", average(numbers))