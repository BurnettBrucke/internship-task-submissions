# Comprehensions, Lambda, Map and Filter

# Task 3: Comprehensions, Lambda, Map and Filter

employees = [
    {"name": "Aman", "department": "Development", "salary": 45000},
    {"name": "Riya", "department": "HR", "salary": 38000},
    {"name": "Neha", "department": "Development", "salary": 55000},
    {"name": "Rahul", "department": "Testing", "salary": 42000},
    {"name": "Priya", "department": "Development", "salary": 60000}
]

def process_employees(employee_list):
    """Process employee data using comprehensions, map, filter and lambda."""

    if not employee_list:
        print("Employee list is empty.")
        return

    # 1. Get all employee names using list comprehension.
    names = [employee["name"] for employee in employee_list]

    print("\nEmployee Names:")
    print(names)

    # 2. Get employees earning more than 45,000.
    high_salary_employees = [
        employee
        for employee in employee_list
        if employee["salary"] > 45000
    ]

    print("\nEmployees earning more than 45,000:")
    print(high_salary_employees)

    # 3. Get Development department employees.
    development_employees = [
        employee
        for employee in employee_list
        if employee["department"] == "Development"
    ]

    print("\nDevelopment Employees:")
    print(development_employees)

    # 4. Create dictionary of employee names and salaries.
    employee_salaries = {
        employee["name"]: employee["salary"]
        for employee in employee_list
    }

    print("\nEmployee Names and Salaries:")
    print(employee_salaries)

    # 5. Calculate yearly salaries using map().
    yearly_salaries = list(
        map(lambda employee: employee["salary"] * 12, employee_list)
    )

    print("\nYearly Salaries:")
    print(yearly_salaries)

    # 6. Find employees earning more than 50,000 using filter().
    high_earners = list(
        filter(
            lambda employee: employee["salary"] > 50000,
            employee_list
        )
    )
    print("\nEmployees earning more than 50,000:")
    print(high_earners)

    # 7. Sort employees by salary using lambda and sorted().
    sorted_employees = sorted(
        employee_list,
        key=lambda employee: employee["salary"]
    )

    print("\nEmployees sorted by salary:")
    print(sorted_employees)

    # 8. Group employees by department.
    grouped_employees = {}

    for employee in employee_list:
        department = employee["department"]

        if department not in grouped_employees:
            grouped_employees[department] = []

        grouped_employees[department].append(employee)

    print("\nEmployees grouped by department:")
    print(grouped_employees)

    # 9. Calculate average salary for each department.
    average_salary = {}

    for department, department_employees in grouped_employees.items():

        total_salary = sum(
            employee["salary"]
            for employee in department_employees
        )

        average = total_salary / len(department_employees)

        average_salary[department] = average

    print("\nAverage Salary by Department:")
    print(average_salary)

    # 10. Find second-highest distinct salary.
    distinct_salaries = sorted(
        {employee["salary"] for employee in employee_list},
        reverse=True
    )

    if len(distinct_salaries) >= 2:
        second_highest = distinct_salaries[1]

        print("\nSecond-highest distinct salary:")
        print(second_highest)

    else:
        print("\nSecond-highest distinct salary is not available.")

def main():
    """Run employee data processing."""

    process_employees(employees)

if __name__ == "__main__":
    main()