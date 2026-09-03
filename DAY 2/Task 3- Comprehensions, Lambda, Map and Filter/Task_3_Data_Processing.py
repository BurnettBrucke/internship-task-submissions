# employees = [{"name": "Aman", "department": "Development", "salary": 45000}, {"name": "Riya", "department": "HR", "salary": 38000}, {"name": "Neha", "department": "Development", "salary": 55000}, {"name": "Rahul", "department": "Testing", "salary": 42000}, {"name": "Priya", "department":"Development", "salary": 60000}]
# • Use list comprehension to get all employee names.
# • Get employees earning more than 45,000.
# • Get only Development department employees.
# • Create a dictionary of employee names and salaries.
# • Use map() to calculate yearly salaries.
# • Use filter() to find employees earning more than 50,000.
# • Use lambda and sorted() to sort employees by salary.
# • Group employees by department.
# • Calculate average salary for each department.
# • Find the second-highest distinct salary.
#*** Do not modify the original employee list. Handle an empty list and explain when comprehension is better than a normal loop***

employees = [
    {
        "name": "Aman",
        "department": "Development",
        "salary": 45000
    },
    {
        "name": "Riya",
        "department": "HR",
        "salary": 38000
    },
    {
        "name": "Neha",
        "department": "Development",
        "salary": 55000
    },
    {
        "name": "Rahul",
        "department": "Testing",
        "salary": 42000
    },
    {
        "name": "Priya",
        "department": "Development",
        "salary": 60000
    }
]


# Check empty list
if len(employees) == 0:
    print("Employee list is empty.")

else:

    # 1. Get all employee names
    names = [employee["name"] for employee in employees]

    print("Employee Names:")
    print(names)


    # 2. Employees earning more than 45,000
    high_salary_employees = [
        employee for employee in employees
        if employee["salary"] > 45000
    ]

    print("\nEmployees earning more than 45000:")
    print(high_salary_employees)


    # 3. Development department employees
    development_employees = [
        employee for employee in employees
        if employee["department"] == "Development"
    ]

    print("\nDevelopment Employees:")
    print(development_employees)


    # 4. Dictionary of employee names and salaries
    employee_salary = {
        employee["name"]: employee["salary"]
        for employee in employees
    }

    print("\nEmployee Salaries:")
    print(employee_salary)


    # 5. Calculate yearly salary using map()
    yearly_salaries = list(
        map(
            lambda employee: employee["salary"] * 12,
            employees
        )
    )

    print("\nYearly Salaries:")
    print(yearly_salaries)


    # 6. Employees earning more than 50,000 using filter()
    filtered_employees = list(
        filter(
            lambda employee: employee["salary"] > 50000,
            employees
        )
    )

    print("\nEmployees earning more than 50000:")
    print(filtered_employees)


    # 7. Sort employees by salary
    sorted_employees = sorted(
        employees,
        key=lambda employee: employee["salary"]
    )

    print("\nEmployees sorted by salary:")
    print(sorted_employees)


    # 8. Group employees by department
    departments = {}

    for employee in employees:

        department = employee["department"]

        if department not in departments:
            departments[department] = []

        departments[department].append(employee["name"])

    print("\nEmployees grouped by department:")
    print(departments)


    # 9. Average salary for each department
    department_salary = {}

    for employee in employees:

        department = employee["department"]
        salary = employee["salary"]

        if department not in department_salary:
            department_salary[department] = []

        department_salary[department].append(salary)


    print("\nAverage Salary by Department:")

    for department in department_salary:

        salaries = department_salary[department]

        average = sum(salaries) / len(salaries)

        print(department, ":", average)


    # 10. Second-highest distinct salary

    salaries = []

    for employee in employees:
        salaries.append(employee["salary"])

    unique_salaries = list(set(salaries))

    unique_salaries.sort(reverse=True)

    if len(unique_salaries) >= 2:
        second_highest = unique_salaries[1]
        print("\nSecond Highest Salary:", second_highest)

    else:
        print("\nSecond highest salary does not exist.")

