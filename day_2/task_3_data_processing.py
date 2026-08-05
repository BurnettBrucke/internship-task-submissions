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


# # • Use list comprehension to get all employee names.
# get_all_employee_names = [i['name'] for i in employees]
# print(get_all_employee_names)


# # • Get employees earning more than 45,000.
# get_employees_earning = [i['name'] for i in employees if i['salary'] > 45000]
# print(get_employees_earning)


# • Get only Development department employees.
employees = [
    {"name": "Aman", "department": "Development", "salary": 45000},
    {"name": "Riya","department": "HR", "salary": 38000}, 
    {"name": "Neha", "department": "Development", "salary":55000}, 
    {"name": "Rahul", "department": "Testing", "salary": 42000}, 
    {"name": "Priya", "department":"Development", "salary": 60000}
    ]

# get_development_employees = [i['name'] for i in employees if i['department']['Development']]
# print(get_development_employees)
# for i in employees:
#     # print(i['department'])
#     if i['department'] == ['Development']:
#         print(i.get('name'))

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


# # • Use map() to calculate yearly salaries.
employees_2 = [
    {"name": "Aman", "salary": 45000},
    {"name": "Riya", "salary": 38000}, 
    {"name": "Neha", "salary": 55000}, 
    {"name": "Rahul", "salary": 42000}, 
    {"name": "Priya", "salary": 60000}
    ]
# yearly_salaries = lambda emp: {
#     "name": emp["name"], 
#     "yearly_salary": emp["salary"] * 12
#     }
# yearly_salaries = list(map(yearly_salaries, employees_2))
# print(yearly_salaries)


# # • Use lambda and sorted() to sort employees by salary.
# # Sort employees by salary (ascending)
# employees_2 = [
#     {"name": "Aman", "salary": 45000},
#     {"name": "Riya", "salary": 38000}, 
#     {"name": "Neha", "salary": 55000}, 
#     {"name": "Rahul", "salary": 42000}, 
#     {"name": "Priya", "salary": 60000}
#     ]

# # sorted(iterable, key=None, reverse=False)
# sorted_salaries = sorted(employees_2, key=lambda i: i["salary"])
# print(sorted_salaries)


# • Group employees by department.
employees = [
    {"name": "Aman", "department": "Development", "salary": 45000},
    {"name": "Riya","department": "HR", "salary": 38000}, 
    {"name": "Neha", "department": "Development", "salary":55000}, 
    {"name": "Rahul", "department": "Testing", "salary": 42000}, 
    {"name": "Priya", "department":"Development", "salary": 60000}
    ]


# • Calculate average salary for each department.
employees = [
    {"name": "Aman", "department": "Development", "salary": 45000},
    {"name": "Riya","department": "HR", "salary": 38000}, 
    {"name": "Neha", "department": "Development", "salary":55000}, 
    {"name": "Rahul", "department": "Testing", "salary": 42000}, 
    {"name": "Priya", "department":"Development", "salary": 60000}
    ]

del employees['name']['Riya']

count = 0
sum = 0
for i in employees:
    print(i)
    # for values in i.items():
    #     print(values)

# print("Average Salary : ", average_salary)



# • Find the second-highest distinct salary.

