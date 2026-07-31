# Sample Data
employees = [
    {"name": "Aman", "department": "Development", "salary": 45000},
    {"name": "Riya", "department": "HR", "salary": 38000},
    {"name": "Neha", "department": "Development", "salary": 55000},
    {"name": "Rahul", "department": "Testing", "salary": 42000},
    {"name": "Priya", "department": "Development", "salary": 60000}
]


def process_employees(employee_list):
    """Process employee data using comprehensions, lambda, map and filter."""

    if not employee_list:
        print("Employee list is empty.")
        return

    # 1. List comprehension to get employee names
    names = [emp["name"] for emp in employee_list]
    print("Employee Names:")
    print(names)

    # 2. Employees earning more than 45000
    high_salary = [emp for emp in employee_list if emp["salary"] > 45000]
    print("\nEmployees earning more than 45000:")
    for emp in high_salary:
        print(emp)

    # 3. Development department employees
    development = [
        emp for emp in employee_list
        if emp["department"] == "Development"
    ]
    print("\nDevelopment Department Employees:")
    for emp in development:
        print(emp)

    # 4. Dictionary of employee names and salaries
    salary_dict = {emp["name"]: emp["salary"] for emp in employee_list}
    print("\nName and Salary Dictionary:")
    print(salary_dict)

    # 5. Yearly salaries using map()
    yearly_salary = list(map(lambda emp: emp["salary"] * 12, employee_list))
    print("\nYearly Salaries:")
    print(yearly_salary)

    # 6. Employees earning more than 50000 using filter()
    above_50000 = list(filter(lambda emp: emp["salary"] > 50000, employee_list))
    print("\nEmployees earning more than 50000:")
    for emp in above_50000:
        print(emp)

    # 7. Sort employees by salary
    sorted_employees = sorted(employee_list, key=lambda emp: emp["salary"])
    print("\nEmployees Sorted by Salary:")
    for emp in sorted_employees:
        print(emp)

    # 8. Group employees by department
    grouped = {}

    for emp in employee_list:
        dept = emp["department"]

        if dept not in grouped:
            grouped[dept] = []

        grouped[dept].append(emp)

    print("\nEmployees Grouped by Department:")
    for dept, emp_list in grouped.items():
        print(f"{dept}:")
        for emp in emp_list:
            print(" ", emp)

    # 9. Average salary for each department
    print("\nAverage Salary by Department:")

    for dept, emp_list in grouped.items():
        total = sum(emp["salary"] for emp in emp_list)
        average = total / len(emp_list)
        print(f"{dept}: {average:.2f}")

    # 10. Second-highest distinct salary
    salaries = sorted(set(emp["salary"] for emp in employee_list), reverse=True)

    if len(salaries) >= 2:
        print("\nSecond Highest Distinct Salary:", salaries[1])
    else:
        print("\nSecond Highest Distinct Salary not found.")


process_employees(employees)

print("\nOriginal Employee List (Unchanged):")
for employee in employees:
    print(employee)

print("\nWhen is comprehension better than a normal loop?")
print("- It is shorter and easier to read.")
print("- It creates a new list, dictionary, or set in one line.")
print("- It is usually faster than writing a normal for loop.")
print("- Use a normal loop when the logic is complex or has many conditions.")