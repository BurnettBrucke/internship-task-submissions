# Task 6: Functions
# Create separate functions for:
#  Checking whether a number is prime.
#  Calculating the factorial of a number.
#  Checking whether a number is even or odd.
#  Finding the largest number from a list.
#  Calculating the average of a list of numbers.
# Use type hints and docstrings in every function.

#Checking whether a number is prime.
def check_prime(n:int)-> bool:
    """
    Check whether a number is prime.

    Args:
        number (int): The number to check.

    Returns:
        bool: True if the number is prime, otherwise False.
    """
    if n<=1:
        return False
    for i in range(2,int(n**0.5)+1):
        if n % i == 0:
            return False
    return True

#Calculating the factorial of a number.
def cal_fact(n:int) -> int:
    """
    Calculate the factorial of a number.

    Args:
        number (int): A non-negative integer.

    Returns:
        int: The factorial of the number.

    Raises:
        ValueError: If the number is negative.
    """
    if n < 0:
        raise ValueError("Factorial is not defined for negative numbers.")
    fact=1
    for i in range(1,n+1):
        fact = fact * i
    return fact

# Checking whether a number is even or odd.

def check_even_odd(n:int)->str:
    """
    Check whether a number is even or odd.

    Args:
        number (int): The number to check.

    Returns:
        str: "Even" if the number is even, otherwise "Odd".
    """
    if n % 2 == 0:
        return "even"
    else:
        return "odd"

#  Finding the largest number from a list.
def find_largest(lst:list[int])->int:
    """
    Find the largest number in a list.

    Args:
        numbers (list[int]): List of integers.

    Returns:
        int: The largest number.

    Raises:
        ValueError: If the list is empty.
    """
    if len(lst) == 0:
        raise ValueError("The list is empty.")
    largest=lst[0]
    for i in lst:
        if i>largest:
            largest=i
    return i

#Calculating the average of a list of numbers.
def avg(lst:list[int])->float:
    """
    Calculate the average of a list of numbers.

    Args:
        numbers (list[int]): List of integers.

    Returns:
        float: The average of the numbers.

    Raises:
        ValueError: If the list is empty.
    """
    if len(lst) == 0:
        raise ValueError("The list is empty.")
    total=0
    n=len(lst)
    for i in lst:
        total+=i
    
    return total/n




print(f"check number is prime or not = {check_prime(13)}")

print(f"calculate factorial = {cal_fact(5)}")

print(f"check even or odd = {check_even_odd(5)}")

print(f"find largest = {find_largest([12,5,2,7,19])}")

print(f"Average of list = {avg([1,2,3,4,5])}")




