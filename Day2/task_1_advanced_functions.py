def validate_salary(salary: float) -> None:
    """Validate an Employees Salary
    raise error
    value error : if salary is empty,negative or invalid
    type error: if salary is not a number

    """
    if salary is None:
        raise ValueError("Salary can not be Empty")
    if not isinstance(salary, (int, float)) or isinstance(salary, bool):
        raise TypeError("Salary must be a integer")
    if salary < 0:
        raise ValueError("Salary cannot be empty")


def create_employess(**emp_detail: object) -> dict[str, object]:
    """create an employee containing the employee info such as name ,designation,salary
    returns the details as a dictionary
    raises error if
    Valuerror: when employee details are empty
    TypeError:When salary has a invalid type

    """
    if not emp_detail:
        raise ValueError("Employee details cannot be empty")
    if "salary" not in emp_detail:
        raise ValueError("Salary is necessary")
    validate_salary(emp_detail["salary"])
    return emp_detail


def main() -> None:
    employee = create_employess(
        name="aditya",
        age=23,
        department="AI/ML",
        designation="Python intern",
        salary=5000,
    )
    print("Employee Details:")
    for key, value in employee.items():
        print(f"{key.title()}: {value}")


# if __name__=="__main__":
#     main()


def salary_statistics(*salaries: float) -> dict[str, float]:
    """
    Calculate the salary statistics
    arg:the salaries of employees
    returns:
     it returns the highest,lowest and average salary
    raises : valueError-> when the salary is not provided
    typeError: when the salary type is not numeric

    """
    if not salaries:
        raise ValueError("Salary is mandatory")
    for salary in salaries:
        validate_salary(salary)
    total = sum(salaries)
    average = total / (len(salaries))
    highest = max(salaries)
    lowest = min(salaries)

    return {
        "total": total,
        "average": average,
        "highest": highest,
        "lowest": lowest,
    }


salaries = salary_statistics(50000, 60000, 45000, 70000)

# print(f"Total of all salaries is {salaries['total']} ,The average of salaries is {salaries['average']} , the highest salary is {salaries['highest']} ,the lowest salary is {salaries['lowest']}")


def create_running_total() -> callable:
    total = 0.0

    def add_amount(amount: float):
        """
        amount that needs to be added
        take the amount as the argument
        returns the total
        show typeerror when the amount is not integer
        """
        nonlocal total
        total += amount
        return total

    return add_amount


# runningtotal=create_running_total()
# print(runningtotal(1000))
# print(runningtotal(2000))
# print(runningtotal(3000))

import time
from time import perf_counter
from functools import wraps


def execution_logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):

        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        execution = end - start
        print(execution)
        return result

    return wrapper


@execution_logger
def calculate_sum(a, b):
    print(a + b)


calculate_sum(5, 10)
