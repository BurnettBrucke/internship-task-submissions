'''Task 1: Advanced Functions and Decorators
Create task_1_advanced_functions.py.
• Create a function that accepts employee details using **kwargs.
• Create a function that accepts any number of salaries using *args and returns total, average, highest
and lowest salary.
• Create a closure that maintains a running total.
• Create a decorator named execution_logger that displays the function name, start message, completion
message and execution time.
• Apply the decorator to at least three functions'''


#  Create a function that accepts employee details using **kwargs.
def employee(**kwargs):
    print("\nemployee detail")
    for keys,value in kwargs.items():
        print(f"{keys}:{value}")

employee(name="vikas",age=23,dept='it')

#  Create a function that accepts any number of salaries using *args and returns total, average, highest
# and lowest salary
def salary(*args):
    total=0
    for i in args:
        total+=i
    print("\nsalary detail")
    print(f"Total:{total}")
    print(f"avg:{total/len(args)}")
    print(f"highest:{max(args)}")
    print(f"lowest:{min(args)}")

salary(100,300,400)

# Create a closure that maintains a running total.
def running_total():
    total=0

    def add(amount):
        nonlocal total
        total+=amount
        return total
    
    return add

x=running_total()
print(x(10)\
      ,x(20)\
        ,x(100))
print('\n')

# Create a decorator named execution_logger that displays the function name, start message, completion
# message and execution time.

import time
def execution_logger(func):
    def wrapper(*args, **kwargs):
        print(f"starting fuction :{func.__name__}")
        start=time.time()
        result=func(*args, **kwargs)
        end=time.time()
        print(f"completed fuction :{func.__name__}")
        print(f'execution time:{end-start:.4f} sec')
        return result
    return wrapper

@execution_logger
def greet():
    print("hello")
greet()
print('\n')

#  Apply the decorator to at least three functions


def deco(func):
    def wrapper(*args):
        print(f"before function : {func.__name__}")
        result=func(*args)
        print(f"after function :{func.__name__}")
        return result
    return wrapper

@deco
def add(a,b):
    print(f" addition :{a+b}")
@deco
def sq(a):
    print(f"square :{a**2}")
@deco
def sqrt(a):
    print(f"squre root: {a**0.5}")

add(2,4)
sq(4)
sqrt(9)