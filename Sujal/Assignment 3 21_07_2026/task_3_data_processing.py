def print_employees(title, employee_list):
    """Print employee details in a formatted table."""

    print(f"\n{title}")
    print("-" * 45)

    if not employee_list:
        print("No employees found.")
        return

    print(f"{'Name':<10} {'Department':<15} {'Salary':>10}")
    print("-" * 45)

    for employee in employee_list:
        print(
            f"{employee['name']:<10}"
            f"{employee['department']:<15}"
            f"{employee['salary']:>10}"
        )


employees = [
    {"name": "Aman", "department": "Development", "salary": 45000},
    {"name": "Riya", "department": "HR", "salary": 38000},
    {"name": "Neha", "department": "Development", "salary": 55000},
    {"name": "Rahul", "department": "Testing", "salary": 42000},
    {"name": "Priya", "department": "Development", "salary": 60000}
]


names = [employee["name"] for employee in employees]
print("Employee Names:")
print(names)


earning = [
    employee
    for employee in employees
    if employee["salary"] > 45000
]
print_employees("Employees earning more than ₹45000", earning)


department_only = [
    employee
    for employee in employees
    if employee["department"] == "Development"
]
print_employees("Development Department Employees", department_only)


employee_salary = {
    employee["name"]: employee["salary"]
    for employee in employees
}

print("\nEmployee Salary Dictionary:")
print(employee_salary)


yearly_salary = list(
    map(lambda employee: employee["salary"] * 12, employees)
)

print("\nYearly Salaries:")
print(yearly_salary)


filter_salary = list(
    filter(lambda employee: employee["salary"] > 50000, employees)
)

print_employees("Employees with Salary Greater Than ₹50000", filter_salary)

employees.sort(
    key=lambda employee: employee["salary"],
    reverse=True
)

print_employees("Employees Sorted by Salary (Highest to Lowest)", employees)

#Group employees by department.

print("\nGrouped by Department")
grouped = {}

for employee in employees:
    department = employee["department"]

    if department not in grouped:
        grouped[department] = []

    grouped[department].append(employee)

print(grouped)

#Calculate average salary for each department.
print("\nAverage Salary by Department")
print("-" * 35)


for department, employees in grouped.items():
    total_salary = 0

    for employee in employees:
        total_salary += employee["salary"]

    average = total_salary / len(employees)

    print(f"{department:<15} : ₹{average:.2f}")

print("\nSecond Highest Salary")    
salaries = sorted(
    {employee["salary"] for employee in employees},
    reverse=True
)

print(salaries)