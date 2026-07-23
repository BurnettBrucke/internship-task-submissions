"""
Task 3: Comprehensions, Lambda, Map and Filter
Create task_3_data_processing.py and use this sample data:
employees = [{"name": "Aman", "department": "Development", "salary": 45000}, {"name": "Riya",
"department": "HR", "salary": 38000}, {"name": "Neha", "department": "Development", "salary":
55000}, {"name": "Rahul", "department": "Testing", "salary": 42000}, {"name": "Priya", "department":
"Development", "salary": 60000}]
• Use list comprehension to get all employee names.
• Get employees earning more than 45,000.
• Get only Development department employees.
• Create a dictionary of employee names and salaries.
• Use map() to calculate yearly salaries.
• Use filter() to find employees earning more than 50,000.
• Use lambda and sorted() to sort employees by salary.
• Group employees by department.
• Calculate average salary for each department.
• Find the second-highest distinct salary

"""
# Sample Data
employees = [
    {"name": "Aman", "department": "Development", "salary": 45000},
    {"name": "Riya", "department": "HR", "salary": 38000},
    {"name": "Neha", "department": "Development", "salary": 55000},
    {"name": "Rahul", "department": "Testing", "salary": 42000},
    {"name": "Priya", "department": "Development", "salary": 60000}
] 

# 1. List comprehension - Get all employee names
names = [emp["name"] for emp in employees]
print("Employee Names:")
print(names)

# 2. Employees earning more than 45000
high_salary = [emp for emp in employees if emp["salary"] > 45000]
print("\nEmployees earning more than 45000:")
print(high_salary)

# 3. Development department employees
development = [emp for emp in employees if emp["department"] == "Development"]
print("\nDevelopment Employees:")
print(development)

# 4. Dictionary of employee names and salaries
salary_dict = {emp["name"]: emp["salary"] for emp in employees}
print("\nName and Salary Dictionary:")
print(salary_dict)

# 5. map() - Calculate yearly salaries
yearly_salary = list(map(lambda emp: emp["salary"] * 12, employees))
print("\nYearly Salaries:")
print(yearly_salary)

# 6. filter() - Employees earning more than 50000
more_than_50000 = list(filter(lambda emp: emp["salary"] > 50000, employees))
print("\nEmployees earning more than 50000:")
print(more_than_50000)

# 7. Sort employees by salary
sorted_employees = sorted(employees, key=lambda emp: emp["salary"])
print("\nEmployees Sorted by Salary:")
print(sorted_employees)

# 8. Group employees by department
groups = {}

for emp in employees:
    dept = emp["department"]

    if dept not in groups:
        groups[dept] = []

    groups[dept].append(emp)

print("\nEmployees Grouped by Department:")
print(groups)

# 9. Average salary for each department
average_salary = {}

for dept, emp_list in groups.items():
    total = sum(emp["salary"] for emp in emp_list)
    average_salary[dept] = total / len(emp_list)

print("\nAverage Salary by Department:")
print(average_salary)

# 10. Second-highest distinct salary
salaries = sorted(set(emp["salary"] for emp in employees), reverse=True)

if len(salaries) >= 2:
    print("\nSecond Highest Distinct Salary:", salaries[1])
else:
    print("\nSecond Highest Salary not found.")