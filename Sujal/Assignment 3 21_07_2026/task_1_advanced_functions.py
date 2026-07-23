import time

def execution_logger(func):
    def wrapper(*args, **kwargs):
        print("Function started...")

        start = time.time()

        result = func(*args, **kwargs)

        end = time.time()

        print(f"Execution Time: {end - start:.6f} seconds")
        print("Function completed.")
        return result

    return wrapper

def validate_salaries(*args):
    if not args:
        raise ValueError("At least one salary must be provided.")

    for salary in args:
        if not isinstance(salary, (int, float)):
            raise TypeError("Salary must be a number.")

        if salary < 0:
            raise ValueError("Salary cannot be negative.")

@execution_logger
def details(**data: str) -> None:
    print(data)

@execution_logger
def salaries(*args: float) -> tuple[float, float, float, float]:
    """
    Calculate total, average, highest and lowest salary.

    Args:
        *args: Variable number of salary values.

    Returns:
        tuple:
            total salary,
            average salary,
            highest salary,
            lowest salary.
    """
    validate_salaries(*args)
    total = sum(args)
    average = total / len(args)
    highest = max(args)
    lowest = min(args)

    return total, average, highest, lowest


@execution_logger
def running_total():
    total=0
    
    def add(num:int)->int:
        nonlocal total
        total+=num
        return total
    
    return add


    

details(name="Sujal",age=28,city="Mumbai",mob=987562)
# salaries = list(map(int, input("Enter numbers: ").split()))

total, average, highest, lowest = salaries(1000, 2000, 4000, 5000, 5600, 123, 4214)
print(f"Total Salary   : {total}")
print(f"Average Salary : {average:.2f}")
print(f"Highest Salary : {highest}")
print(f"Lowest Salary  : {lowest}")

total =running_total()
print(total(10))
print(total(20))
print(total(30))
print(total(40))
print(total(50))



    
    
