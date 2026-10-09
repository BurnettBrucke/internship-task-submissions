# Task 1: Advanced Functions and Decorators

import time
from functools import wraps
from typing import Any, Callable

def validate_salary(salary: Any) -> int | float:
    """Validate salary value."""

    if salary is None or salary == "":
        raise ValueError("Salary cannot be empty.")

    if not isinstance(salary, (int, float)):
        raise ValueError("Salary must be a number.")

    if salary < 0:
        raise ValueError("Salary cannot be negative.")

    return salary


def employee_details(**kwargs: Any) -> dict[str, Any]:
    """Accept employee details using keyword arguments."""

    if not kwargs:
        raise ValueError("Employee details cannot be empty.")

    return kwargs


def salary_details(*salaries: int | float) -> tuple:
    """Calculate total, average, highest and lowest salary."""

    if not salaries:
        raise ValueError("At least one salary is required.")

    valid_salaries = []

    for salary in salaries:
        valid_salary = validate_salary(salary)
        valid_salaries.append(valid_salary)

    total = sum(valid_salaries)
    average = total / len(valid_salaries)
    highest = max(valid_salaries)
    lowest = min(valid_salaries)

    return total, average, highest, lowest


def create_running_total() -> Callable:
    """Create a function that maintains a running total."""

    total = 0

    def add_amount(amount: int | float) -> int | float:
        nonlocal total

        amount = validate_salary(amount)

        total = total + amount

        return total

    return add_amount


def execution_logger(function: Callable) -> Callable:
    """Log function name, start, completion and execution time."""

    @wraps(function)
    def wrapper(*args: Any, **kwargs: Any) -> Any:

        print(f"\nFunction: {function.__name__}")
        print("Execution started...")

        start_time = time.time()

        result = function(*args, **kwargs)

        end_time = time.time()

        print("Execution completed.")
        print(f"Execution time: {end_time - start_time:.6f} seconds")

        return result

    return wrapper

@execution_logger
def show_employee() -> None:
    """Display employee details."""

    employee = employee_details(
        name="Ruby",
        department="Python",
        salary=25000
    )

    print("Employee:", employee)

@execution_logger
def show_salary_details() -> None:
    """Display salary statistics."""

    result = salary_details(
        20000,
        25000,
        30000,
        22000
    )
    print("Total:", result[0])
    print("Average:", result[1])
    print("Highest:", result[2])
    print("Lowest:", result[3])


@execution_logger
def show_running_total() -> None:
    """Display running total."""

    running_total = create_running_total()

    print("Total:", running_total(1000))
    print("Total:", running_total(500))
    print("Total:", running_total(200))


def main() -> None:
    """Run all demonstrations."""

    show_employee()
    show_salary_details()
    show_running_total()

if __name__ == "__main__":
    main()