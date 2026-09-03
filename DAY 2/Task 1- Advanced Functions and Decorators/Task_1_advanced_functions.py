# • Create a function that accepts employee details using **kwargs.
# • Create a function that accepts any number of salaries using *args and returns total, average, highest and lowest salary.
# • Create a closure that maintains a running total.
# • Create a decorator named execution_logger that displays the function name, start message, completion message and execution time.
# • Apply the decorator to at least three functions.

############# Requirements ##################
# • Use type hints and docstrings.
# • Validate empty input and invalid salary values.
# • Avoid repeating the same validation logic

import time


def validate_salaries(salaries):
    """Validate salary values."""

    if len(salaries) == 0:
        raise ValueError("Salary cannot be empty")

    for salary in salaries:
        if salary < 0:
            raise ValueError("Salary cannot be negative")


def employee_details(**kwargs):
    """Accept employee details using kwargs."""

    if len(kwargs) == 0:
        raise ValueError("Employee details cannot be empty")

    return kwargs


def salary_details(*salaries):
    """Calculate salary statistics."""

    validate_salaries(salaries)

    total = sum(salaries)
    average = total / len(salaries)
    highest = max(salaries)
    lowest = min(salaries)

    return total, average, highest, lowest


def running_total():
    """Create a closure that maintains a running total."""

    total = 0

    def add(number):
        nonlocal total
        total = total + number
        return total

    return add


def execution_logger(function):
    """Log function name and execution time."""

    def wrapper():

        print("Starting:", function.__name__)

        start = time.time()

        function()

        end = time.time()

        print("Completed:", function.__name__)
        print("Execution time:", end - start)

    return wrapper


@execution_logger
def function_one():
    """First decorated function."""
    print("Function One")


@execution_logger
def function_two():
    """Second decorated function."""
    print("Function Two")


@execution_logger
def function_three():
    """Third decorated function."""
    print("Function Three")


# Employee details
employee = employee_details(
    name="Deepika",
    department="Python",
    salary=30000
)

print("Employee:", employee)


# Salary details
total, average, highest, lowest = salary_details(
    30000, 40000, 50000, 35000
)

print("Total:", total)
print("Average:", average)
print("Highest:", highest)
print("Lowest:", lowest)


# Closure
total_amount = running_total()

print("Running Total:", total_amount(1000))
print("Running Total:", total_amount(2000))
print("Running Total:", total_amount(500))


# Decorators
function_one()
function_two()
function_three()