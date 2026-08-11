#Task 6: Functions
#Create separate functions for:

#Checking whether a number is prime.
#Calculating the factorial of a number.
#Checking whether a number is even or odd.
#Finding the largest number from a list.
#Calculating the average of a list of numbers.
#Use type hints and docstrings in every function.

def is_prime(num:int)-> bool:
    if num <2:
        return False
    for i in range(num*0.5)+1:
        if num % i == 0:
            return False
    return True

def factorial(num:int)->int:
    if num <0:
        raise ValueError("factorial is not defined for negative numbers")
    if num == 0:
        return 1
    fact = 1
    for i in range(1,num+1):
        fact *=i
    return fact

def even_odd(num:int)->str:
    if num %2 ==0:
        return "even"
    return "odd"

def largest_from_list(list_int : list)->int: 
    maxi = list_int[0]
    for i in range (len(list_int)):
        if list_int[i] > maxi:
            maxi = list_int[i]
    return maxi
    
def largest_from_list(list_int : list)->int: 
    sum = 0
    for i in range (len(list_int)):
        sum += list_int[i]
    return sum/len(list_int)
 