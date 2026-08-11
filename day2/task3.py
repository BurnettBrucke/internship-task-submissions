employees = [
    {"name": "Aman", "department": "Development", "salary": 45000},
    {"name": "Riya", "department": "HR", "salary": 38000},
    {"name": "Neha", "department": "Development", "salary": 55000},
    {"name": "Rahul", "department": "Testing", "salary": 42000},
    {"name": "Priya", "department": "Development", "salary": 60000}
]

if not employees:
    print("No employees found")

else:
    # 1. Names
    names = [e["name"] for e in employees]
    print("Names:", names)

    # 2. Salary > 45000
    result = [e for e in employees if e["salary"] > 45000]
    print("Salary > 45000:", result)

    # 3. Development employees
    development = [e for e in employees if e["department"] == "Development"]
    print("Development:", development)

    # 4. Name and salary
    name_salary = {e["name"]: e["salary"] for e in employees}
    print("Name-Salary:", name_salary)

    # 5. Yearly salary using map
    yearly = list(map(lambda e: e["salary"] * 12, employees))
    print("Yearly salary:", yearly)

    # 6. Salary > 50000 using filter
    high = list(filter(lambda e: e["salary"] > 50000, employees))
    print("Salary > 50000:", high)

    # 7. Sort by salary
    sorted_employees = sorted(employees, key=lambda e: e["salary"])
    print("Sorted:", sorted_employees)

    # 8. Group by department
    groups = {}

    for e in employees:
        dept = e["department"]

        if dept not in groups:
            groups[dept] = []

        groups[dept].append(e["name"])

    print("Groups:", groups)

    # 9. Average salary
    for dept in groups:
        total = 0
        count = 0

        for e in employees:
            if e["department"] == dept:
                total += e["salary"]
                count += 1

        print(dept, "average:", total / count)

    # 10. Second highest salary
    salaries = []

    for e in employees:
        if e["salary"] not in salaries:
            salaries.append(e["salary"])

    salaries.sort(reverse=True)

    if len(salaries) >= 2:
        print("Second highest:", salaries[1])