
from typing import Any, Dict
import time
from functools import wraps


def validate_salaries(salaries: tuple[float, ...]) -> None:
    if not salaries:
        raise ValueError("At least one salary must be provided.")

    for salary in salaries:
        if not isinstance(salary, (int, float)):
            raise ValueError(f"Invalid salary: {salary}")

        if salary < 0:
            raise ValueError("Salary cannot be negative.")


def execution_logger(func):
    # Decorator that logs execution details.
    @wraps(func)
    def wrapper(*args, **kwargs):
        print(f"\nStarting '{func.__name__}'...")

        start_time = time.perf_counter()

        result = func(*args, **kwargs)

        end_time = time.perf_counter()

        print(f"Completed '{func.__name__}'")
        print(f"Execution Time: {end_time - start_time:.6f} seconds")

        return result
    return wrapper


@execution_logger
def employee_details(**kwargs: Any) -> Dict[str, Any]:
    # Accept employee details using **kwargs.
    if not kwargs:
        raise ValueError("Employee details cannot be empty.")
    return kwargs


@execution_logger
def salary_statistics(*salaries: float) -> Dict[str, float]:
    # Calculate salary statistics.
    validate_salaries(salaries)

    total = sum(salaries)
    average = total / len(salaries)

    return {
        "Total": total,
        "Average": average,
        "Highest": max(salaries),
        "Lowest": min(salaries),
    }


def running_total():
    # Create a closure that maintains a running total.
    total = 0

    @execution_logger
    def add(value: float) -> float:
        nonlocal total

        if value < 0:
            raise ValueError("Value cannot be negative.")

        total += value
        return total
    return add


@execution_logger
def display_statistics(*salaries: float) -> None:
    # Display salary statistics
    stats = salary_statistics(*salaries)

    print("\nSalary Statistics")
    print("-----------------")

    for key, value in stats.items():
        print(f"{key}: {value}")

if __name__ == "__main__":
    print("Employee Details")
    employee = employee_details(
        id=101,
        name="Rahul",
        department="IT",
        city="Delhi"
    )

    print(employee)
    print("\nSalary Report")
    display_statistics(45000, 52000, 61000, 48000)
    print("\nClosure Example")
    total = running_total()
    print(total(100))
    print(total(250))
    print(total(400))


# # 1. Create a function that accept employee details using ** kwargs
# def employee_details(**kwargs):

#     # Accessing specific keys safely using .get()
#     name = kwargs.get("name")
#     print(f"Name : {name}")

#     # Iterating through all passed keyword arguments
#     for key, values in kwargs.items():
#             print(f"{key} : {values}")

# # Calling the function with varying named parameters
# employee_details(name='rahul', age=25, city='Shajapur')
# # -----------------------------------------------------------------------------------------------------------

# # 2. Create a function that accepts any number of salaries using *args and returns 
# # total, average, highest and lowest salary.
# def any_number_of_salaries(*args):
#     if args:
#         count = 0
#         total = 0
#         highest = args[0]
#         lowest = args[0] 
#         for i in args:
#             total = total + i
#             count = count +1 
#             average = total/count
#             # First of all we will assign args[0] to highest value then 
#             # we will check which one is highest, if we found one, then 
#             # we will assign those value to highest.
#             if i > highest :
#                 highest = i
#             if i < lowest :
#                 lowest = i
#         print("Lowest Value is : ", lowest)    
#         print("Highest Value is : ", highest)
#         print("Total Salary is : ", total)  
#         print("Average is : ", average)

#     elif args != float(args) :
#         print("Invalid Salary Values !")
#     else:
#         print("Please Input some salary !")


# any_number_of_salaries(2345.45, 24354, 'rahul')

# # 3. Create a closure that maintains a running total.
# # 4. Create a decorator named execution_logger that displays the function name,
# #    start message, completion message and execution time.
# # 5. Apply the decorator to at least three functions.

# def execution_logger():
#     pass

# execution_logger()

