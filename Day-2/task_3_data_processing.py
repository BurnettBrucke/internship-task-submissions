employees = [{"name": "Aman", "department": "Development", "salary": 45000}, {"name": "Riya",
"department": "HR", "salary": 38000}, {"name": "Neha", "department": "Development", "salary":
55000}, {"name": "Rahul", "department": "Testing", "salary": 42000}, {"name": "Priya", "department":
"Development", "salary": 60000}]


def get_employee_names(employees):
    """Display all employee names."""
    names = [emp["name"] for emp in employees ]
    print(f"Employees names aree : {names}")

def employees_earning_more_then(employees , sal):
    """Display all the employee whose salary is more then the input salary."""
    salaries = [emp["name"] for emp in employees if emp["salary"] > sal]
    print(f"Employees with more then {sal} are {salaries}")

def deparment_specific(employees):
    """Display only Development department employees."""
    employees_list = [emp["name"] for emp in employees if emp["department"] == "Development"]
    print(f"Employees with Development department are {employees_list}")

def create_dic(employees):
    """ Create a dictionary of employee names and salaries."""
    names = [emp["name"] for emp in employees ]
    salaries = [emp["salary"] for emp in employees]
    result = dict(zip(names , salaries))
    print(result)


def calculate_yearly_salary(employees):
    """Calculate yearly salary of all employees."""
    yearly_salary = list(map(lambda employee:employee["salary"]*12 , employees))
    print(yearly_salary)

def salary_more_than(employee):
    """filter function to get salary more then 50k."""
    return employee["salary"] > 50000


def filter_employees(employees):
    filtered_employees = list(filter(salary_more_than, employees))
    print(filtered_employees)

def sort_by_salary(employees):
    return sorted(employees, key=lambda employee: employee["salary"])

def group_by_department(employees):
    grouped = {}
    for employee in employees:
        department = employee["department"]

        if department not in grouped:
            grouped[department] = []

        grouped[department].append(employee)
    print(grouped)


def average_salary_by_department(employees):
    department_salary = {}
    department_count = {}

    for employee in employees:
        department = employee["department"]
        salary = employee["salary"]

        department_salary[department] = department_salary.get(department, 0) + salary
        department_count[department] = department_count.get(department, 0) + 1

    averages = {}

    for department in department_salary:
        averages[department] = department_salary[department] / department_count[department]

    print(averages)

def second_highest_salary(employees):
    salaries = []

    for employee in employees:
        salaries.append(employee["salary"])

    unique_salaries = set(salaries)
    sorted_salaries = sorted(unique_salaries, reverse=True)

    print(sorted_salaries[1])

def main():

    print("Create Dictionary:")
    create_dic(employees)

    print("\nDepartment Specific:")
    deparment_specific(employees)

    print("\nEmployee Names:")
    get_employee_names(employees)

    print("\nEmployees Earning More Than 20000:")
    employees_earning_more_then(employees, 20000)

    print("\nYearly Salary:")
    calculate_yearly_salary(employees)

    print("\nFiltered Employees:")
    filter_employees(employees)

    print("\nGrouped By Department:")
    group_by_department(employees)

    print("\nAverage Salary of each department:")
    average_salary_by_department(employees)

    print("\nSecond highest salary:")
    second_highest_salary(employees)


main()