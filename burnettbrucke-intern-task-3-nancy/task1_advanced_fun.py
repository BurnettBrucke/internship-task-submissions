"""
Task 1: Advanced Functions and Decorators
Create task_1_advanced_functions.py.
• Create a function that accepts employee details using **kwargs.
• Create a function that accepts any number of salaries using *args and returns total, average, highest
and lowest salary.
• Create a closure that maintains a running total.
• Create a decorator named execution_logger that displays the function name, start message, completion
message and execution time.
• Apply the decorator to at least three functions.

"""
#1.Create a function that accepts employee details using **kwargs.
def Employee_details(**kwargs):
    for key,value in kwargs.items():
        print(f"{key} : {value}")


#2.Create a function that accepts any number of salaries using *args and returns total, average, highest
#and lowest salary.
def salary_details(*args):
    total = sum(args)
    average = total / len(args)
    highest = max(args)
    lowest = min(args)

    return total, average, highest, lowest

#3.Create a closure that maintains a running total.
def running_total():
    total = 0

    def add(number):
        nonlocal total
        total += number
        return total

    return add



# Create a decorator named execution_logger that displays the function name, start message, completion
# message and execution time
import time
def execution_logger(func):
    def wrapper(*args, **kwargs):
        print(f"Function Name: {func.__name__}")
        print("Execution started...")

        start_time = time.time()

        result = func(*args, **kwargs)

        end_time = time.time()

        print("Execution completed.")
        print(f"Execution Time: {end_time - start_time:.6f} seconds")

        return result

    return wrapper


@execution_logger
def display_message():
    print("Hello, Welcome to Python!")

#Apply the decorator to at least three functions.

# Function 1
@execution_logger
def add(a, b):
    print("Sum:", a + b)


# Function 2
@execution_logger
def greet(name):
    print(f"Hello, {name}!")


# Function 3
@execution_logger
def square(num):
    print("Square:", num * num)

#calling function 1
print("-------Employee Details------")
Employee_details(
    Name="Nancy",
    Age=24,
    Department="Python"
)
print("-----------------------------")

# calling function 2
total, average, highest, lowest = salary_details(25000, 30000, 45000, 28000)

print("Total Salary:", total)
print("Average Salary:", average)
print("Highest Salary:", highest)
print("Lowest Salary:", lowest)

print("-----------------------------")

#calling function 3
total = running_total()

print(total(10))   # 10
print(total(20))   # 30
print(total(15))   # 45
print(total(5))    # 50

print("-----------------------------")

#calling function 4
display_message()

print("-----------------------------")


# Calling the functions 5
add(10, 20)
print("------------------------------")
greet("Nancy")
print("------------------------------")
square(5)

print("------------------------------")

