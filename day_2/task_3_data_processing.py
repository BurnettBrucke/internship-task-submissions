# Create task_3_data_processing.py and use this sample data:

# Do not modify the original employee list. Handle an empty list and explain when
# comprehension is better than a normal loop.

employees = [
    {"name": "Aman", "department": "Development", "salary": 45000},
    {"name": "Riya","department": "HR", "salary": 38000}, 
    {"name": "Neha", "department": "Development", "salary":55000}, 
    {"name": "Rahul", "department": "Testing", "salary": 42000}, 
    {"name": "Priya", "department":"Development", "salary": 60000}
    ]


# • Use list comprehension to get all employee names.
get_all_employee_names = [i['name'] for i in employees]
print(get_all_employee_names)


# • Get employees earning more than 45,000.
get_employees_earning = [i['name'] for i in employees if i['salary'] > 45000]
print(get_employees_earning)


# • Get only Development department employees.
get_development_employees = [i['name'] for i in employees if i['department']['Development']]
print(get_development_employees)
for i in employees:
    # print(i['department'])
    if i['department'] == ['Development']:
        print(i.get('name'))
        
# -----------------------------------------------------------------------------------------------

# • Create a dictionary of employee names and salaries.
employees_2 = [
    {"name": "Aman", "salary": 45000},
    {"name": "Riya", "salary": 38000}, 
    {"name": "Neha", "salary": 55000}, 
    {"name": "Rahul", "salary": 42000}, 
    {"name": "Priya", "salary": 60000}
    ]

employees_2 = {}
employees_2['name'] = 'Arush'
employees_2['salary'] = 45000
employees_2['name'] = 'Riya'
employees_2['salary'] = 38000
print(employees_2)

# -----------------------------------------------------------------------------------------------

# • Use map() to calculate yearly salaries.
employees_2 = [
    {"name": "Aman", "salary": 45000},
    {"name": "Riya", "salary": 38000}, 
    {"name": "Neha", "salary": 55000}, 
    {"name": "Rahul", "salary": 42000}, 
    {"name": "Priya", "salary": 60000}
    ]
yearly_salaries = lambda emp: {
    "name": emp["name"], 
    "yearly_salary": emp["salary"] * 12
    }
yearly_salaries = list(map(yearly_salaries, employees_2))
print(yearly_salaries)

# -----------------------------------------------------------------------------------------------

# • Use lambda and sorted() to sort employees by salary.
# Sort employees by salary (ascending)
employees_2 = [
    {"name": "Aman", "salary": 45000},
    {"name": "Riya", "salary": 38000}, 
    {"name": "Neha", "salary": 55000}, 
    {"name": "Rahul", "salary": 42000}, 
    {"name": "Priya", "salary": 60000}
    ]

# sorted(iterable, key=None, reverse=False)
sorted_salaries = sorted(employees_2, key=lambda i: i["salary"])
print(sorted_salaries)

# ----------------------------------------------------------------------------------------------

# • Group employees by department.
employees = [
    {"name": "Aman", "department": "Development", "salary": 45000},
    {"name": "Riya","department": "HR", "salary": 38000}, 
    {"name": "Neha", "department": "Development", "salary":55000}, 
    {"name": "Rahul", "department": "Testing", "salary": 42000}, 
    {"name": "Priya", "department":"Development", "salary": 60000}
    ]
# Group employees by department
grouped = {}

for emp in employees:
    dept = emp["department"]
    if dept not in grouped:
        grouped[dept] = []
    grouped[dept].append(emp)

# Print grouped employees
for dept, emp_list in grouped.items():
    print(f"{dept}:")
    for emp in emp_list:
        print(f"  {emp['name']} - {emp['salary']}")

# --------------------------------------------------------------------------------------------------

# • Calculate average salary for each department.
employees = [
    {"name": "Aman", "department": "Development", "salary": 45000},
    {"name": "Riya","department": "HR", "salary": 38000}, 
    {"name": "Neha", "department": "Development", "salary":55000}, 
    {"name": "Rahul", "department": "Testing", "salary": 42000}, 
    {"name": "Priya", "department":"Development", "salary": 60000}
    ]

# assign an empty dict
dept_data = {}

for emp in employees:
    dept = emp["department"]
    salary = emp["salary"]

    if dept not in dept_data:
        dept_data[dept] = {"total": 0, "count": 0}

    dept_data[dept]["total"] += salary
    dept_data[dept]["count"] += 1

# Calculate and print average salary
for dept, data in dept_data.items():
    average = data["total"] / data["count"]
    print(f"{dept}: Average Salary = {average}")

# ----------------------------------------------------------------------------------------------

# • Find the second-highest distinct salary.
salaries = sorted({emp["salary"] for emp in employees}, reverse=True)

if len(salaries) >= 2:
    print("Second-highest distinct salary:", salaries[1])
else:
    print("There is no second-highest distinct salary.")
