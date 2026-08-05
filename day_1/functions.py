# Task 6: Functions
# Checking whether a number is prime.
def is_prime(num):
    if num == 1:
        return "One is already a prime number"
    if num > 1:
        for i in range(2, num):
            if (num % i) == 0:
                print(num, "is not a prime number")
                break
        else:
            print(num, "is a prime number")
    else:
        print(num, "it is a negative number")

number = int(input("Enter a number : "))
is_prime(number)


# Calculating the factorial of a number.
def factorial(num):
    if num < 0:
        return "Factorial is not defined for negative numbers"  
    if num == 0 or num == 1:
        return 1
    else:
        return num * factorial(num - 1)

number = int(input("Enter a number : "))
fact = factorial(number)
print(fact)


# Checking whether a number is even or odd.
def check_even_or_odd(num):
    if num % 2 == 0:
        print("It is Even number")
    else:
        print("It is Odd number")

number = int(input("Enter a number : "))
check_even_or_odd(number)


# Finding the largest number from a list.
def largest_number_from_list(my_list):
    largest_number = my_list[0]
    for i in my_list:
        if i > largest_number:
            largest_number = i
    return largest_number

lst = [43,65,12,59,32,27,53]
print(largest_number_from_list(lst))


# Calculating the average of a list of numbers.
def average_of_numbers(my_list): 
    sum = 0    
    average = 0
    length = len(my_list)      
    for i in my_list:
        sum = sum + i
        # print(sum)
        average = sum / length
    return average

numbers = [13,64,34,56,78,90,32,18]
print(average_of_numbers(numbers))

# Use type hints and docstrings in every function.

