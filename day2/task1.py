import time


def employee(**details: str) -> None:
    """Store employee details."""
    if not details:
        print("Details cannot be empty")
        return

    print(details)


def salaries(*salary: int) -> tuple:
    """Calculate salary details."""
    if not salary:
        print("Salary cannot be empty")
        return

    for s in salary:
        if s <= 0:
            print("Invalid salary")
            return

    total = sum(salary)
    average = total / len(salary)

    return total, average, max(salary), min(salary)


def running_total():
    """Maintain running total."""
    total = 0

    def add(value: int) -> int:
        nonlocal total
        total += value
        return total

    return add


def execution_logger(func):
    """Show function execution details."""
    def wrapper():
        start = time.time()
        print("Starting:", func.__name__)

        func()

        print("Completed:", func.__name__)
        print("Time:", time.time() - start)

    return wrapper


@execution_logger
def fun1():
    """First function."""
    print("Hello")


@execution_logger
def fun2():
    """Second function."""
    print("Python")


@execution_logger
def fun3():
    """Third function."""
    print("Learning")


employee(name="Subhi", role="Python Developer")

print(salaries(30000, 40000, 50000))

add = running_total()
print(add(100))
print(add(200))
print(add(300))

fun1()
fun2()
fun3()