def employee_details(**kwargs):

    if not kwargs:
        print("No employee details provided.")
        return

    print("Employee Details")
    print("----------------")

    for key, value in kwargs.items():
        print(f"{key} : {value}")
'''
employee_details(
            name="Jaya",
            age=22,
            department="Python",
            salary=35000
)'''
employee_details()



def salary_details(*args):

    if not args:
        print("No salary provided.")
        return
  
    for salary in args:
        if not isinstance(salary, (int, float)):
            print("Invalid salary value.")
            return
    for salary in args:
        if salary < 0:
            print("Salary cannot be negative.")
            return
    total = sum(args)
    average = total / len(args)
    highest = max(args)
    lowest = min(args)

    print("Total Salary:", total)
    print("Average Salary:", average)
    print("Highest Salary:", highest)
    print("Lowest Salary:", lowest)


# salary_details(25000, 30000, 45000, 50000)
# salary_details()
# salary_details(1000,5000,-8000,100)
salary_details(25000, "30000", 45000)

'''
def running_total():
    total = 0

    def add(number):
        nonlocal total
        total += number
        return total

    return add
# Create the closure
total = running_total()
print(total(10))
print(total(20))
print(total(5))
print(total(15))
'''

import time
def execution_logger(func):

    def wrapper():
        print("Function Name:", func.__name__)
        print("Function Started")

        start = time.time()

        func()

        end = time.time()

        print("Function Completed")
        print("Execution Time:", end - start, "seconds")

    return wrapper
@execution_logger
def display():
    print("Welcome to Python")
display()
