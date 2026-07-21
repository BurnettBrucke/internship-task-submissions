'''Task 6: Functions
Create separate functions for:

Checking whether a number is prime.
Calculating the factorial of a number.
Checking whether a number is even or odd.
Finding the largest number from a list.
Calculating the average of a list of numbers.
Use type hints and docstrings in every function.'''

# check prime no 
n=int(input("enter a number :"))
def is_prime(n):
    if n<=1:
        print("not prime")
    else:
        for i in range(2,n):
            if n%i==0:
                print("not prime")
                break
        else:
            print("prime")

is_prime(n)

# factorial of number 
def factorial(n):
    fact=1
    for i in range(1,n+1):
        fact=fact*i
    print(f"factoraol : {fact}")

factorial(n)

# check even or odd 
def is_even_odd(n):
    print("even" if n%2==0 else "odd")
is_even_odd(n)

# largest from the list 
def largest(list):
    max=list[0]
    for i in range(len(list)):
        if max<list[i]:
            max=list[i]
    print(f"largest element:{max}")

l=[9,4,5,88,7,8,56]
largest(l)

# avrage of list 
def avg_list(list):
    sum=0
    for i in range(len(list)):
        sum=sum+list[i]
    avg=sum/len(list)
    print(f"avrage:{avg}")

l=[1,2,3,4,5]
avg_list(l)




