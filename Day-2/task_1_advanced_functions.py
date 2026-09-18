import time

def get_details() -> dict:
    """
    Get and validate employee details from user input.
    """
    name = input("Enter employee name: ").strip()
    age_input = input("Enter employee age: ").strip()
    position = input("Enter employee position: ").strip()
    department = input("Enter employee department: ").strip()

    if not name:
        raise ValueError("Name cannot be empty.")

    if not position:
        raise ValueError("Position cannot be empty.")

    try:
        age = int(age_input)
    except ValueError:
        raise ValueError("Age must be an integer.")

    if age < 0:
        raise ValueError("Age cannot be negative.")

    if not department:
        department = None

    return {
        "name": name,
        "age": age,
        "position": position,
        "department": department
    }
def emp_details(**kwargs):
    """
    Function to print employee details passed as keyword arguments.
    """
    if not kwargs:
        print("No employee details provided.")
    else:
        for key, value in kwargs.items():
            print(f"{key}: {value}")

def salary_statistics(*salaries):
    try:
        for salary in salaries:
            if salary <= 0:
                raise ValueError(f"Invalid salary value: {salary}. Salary cannot be negative.")
        total_salary = sum(salaries)
        average_salary = total_salary / len(salaries)
        highest_salary = max(salaries)
        Lowest_salary = min(salaries)
        print(f"Total Salary: {total_salary}")
        print(f"Average Salary: {average_salary}")
        print(f"Highest Salary: {highest_salary}")
        print(f"Lowest Salary: {Lowest_salary}")
    except Exception as e:
            print(f"Error: {e}")


def running_total():
    total = 0
    def add(amount):
        nonlocal total
        total += amount
        return total
    return add



def execution_logger(func):
    """"
    Decorator to log the execution time of a function.
    """
    def wrapper(*args , **kwargs):
        start_time = time.time()
        print("welcome to the execution logger")
        print(f"Name of the function is : {func.__name__} and the arguments are : {args} and the keyword arguments are : {kwargs}")
        result = func(*args , **kwargs)
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"Execution time of {func.__name__}: {execution_time:.6f} seconds")
        return result
    return wrapper



def main():
    print("=============Employee Details=============")
    emp_details(name="Alice", age=28, position="Data Scientist", department="AI Research")
    emp_details()
    try:
        details = get_details()
        emp_details(**details)
    except (ValueError, TypeError) as e:
        print(f"Error: {e}")
    emp_details(name="mayank", age=35, position="Project Manager", department = None)
    emp_details(name="shiva", age=40, position="HR Manager", department= "Human Resources")

    print("\n=============Salary Statistics=============") 
    salary_statistics(50000, 60000, 75000, 80000, 90000)
    salary_statistics(50000, "salary" ,75000, 80000, 90000)
    salary_statistics()
    salary_statistics(45000, 55000, 0 , -10000)

    print("\n=============Running Total=============")
    running_total_func = running_total()
    print(running_total_func(1000))  # Output: 1000
    print(running_total_func(500))   # Output: 1500
    print(running_total_func(200))   # Output: 1700
    print(running_total_func(-300))  # Output: 1400

    print("\n=============Execution Logger=============")
    execution_logger(emp_details)(name="John Doe", age=30, position="Software Engineer")
    execution_logger(salary_statistics)(50000, 60000, 75000, 80000, 90000)
    execution_logger(running_total_func)
        
if __name__ == "__main__":
    main()