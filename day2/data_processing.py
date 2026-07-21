'''Create task_3_data_processing.py and use this sample data:
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
• Find the second-highest distinct salary.
Do not modify the original employee list. Handle an empty list and explain when
comprehension is better than a normal loop.'''

employees = [
    {"name": "Aman", "department": "Development", "salary": 45000}, 
    {"name": "Riya","department": "HR", "salary": 38000},
    {"name": "Neha", "department": "Development", "salary":55000},
    {"name": "Rahul", "department": "Testing", "salary": 42000},
    {"name": "Priya", "department":"Development", "salary": 60000}
]
    
# • Use list comprehension to get all employee names.
name_list=[i['name'] for i in employees]
print(name_list)

# Get employees earning more than 45,000
earning_more=[i for i in employees if i['salary']>45000]
print("\nemployee earning more")
for i in earning_more:
    print(i)
# print(earning_more)

#  Get only Development department employees
development_dept=[i for i in employees if i['department']=='Development']
print("\nemployees of development dept")
for i in development_dept:
    print(i)

#  Create a dictionary of employee names and salaries.
employee_dict={i['name']:i['salary'] for i in employees}
print('\n name: salary')
for k,v in employee_dict.items():
    print(f"{k}:{v}")

# Use map() to calculate yearly salaries.
yearly_sal=list(map(lambda i:i['salary']*12,employees))
print('\n yearly salary ')
print(yearly_sal)

# Use filter() to find employees earning more than 50,000.
more_sal=list(filter(lambda i:i['salary']>50000,employees))
print('\n salary more tahn 50000')
print(more_sal)

# Use lambda and sorted() to sort employees by salary.
sorted_list=sorted(employees,key=lambda i: i['salary'])
print('\n')
for i in sorted_list:
    print(i)

#  Group employees by department.
grouped={}
for emp in employees:
    dept=emp['department']
    if dept not in grouped:
        grouped[dept]=[]
    grouped[dept].append(emp)
print("\n")
for k,v in grouped.items():
    print(f"{k}")
    for i in v:
        print(f'{v}')


# Calculate average salary for each department
dept_sal={}
for i in employees:
    dept=i['department']
    if dept not in dept_sal:
        dept_sal[dept]=[]
    dept_sal[dept].append(i['salary'])
print("\n avrage sal by dept")
for k,v in dept_sal.items():
    avg=sum(v)/len(v)
    print(f"{k}:{avg}")

#  Find the second-highest distinct salary.
sorted_list=sorted(employees,key=lambda i: i['salary'])
print('\n second highest salary')
print(sorted_list[-2])

    