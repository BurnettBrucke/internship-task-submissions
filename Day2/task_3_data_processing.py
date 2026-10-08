employees = [
    {"name": "Aman", "department": "Development", "salary": 45000},
    {"name": "Riya", "department": "HR", "salary": 38000},
    {"name": "Neha", "department": "Development", "salary": 55000},
    {"name": "Rahul", "department": "Testing", "salary": 42000},
    {"name": "Priya", "department": "Development", "salary": 60000},
]

# print(employees['Aman'])


def employee_names():
    names = [employee["name"] for employee in employees]
    print(names)


# employee_names()


def employees_earning45():
    emp = [employee["name"] for employee in employees if employee["salary"] > 45000]
    print(emp)


# employees_earning45()


def employee_development():
    emp = [
        employee["name"]
        for employee in employees
        if employee["department"] == "Development"
    ]
    print(emp)


# employee_development()


def emp_dict():
    for employee in employees:
        dicti = {employee["name"], employee["salary"]}
        print(dicti)


# emp_dict()


def map_salary():

    yearly_salary = list(map(lambda employee: employee["salary"] * 12, employees))
    print(yearly_salary)


# map_salary()

# high_earner_50000=list(filter(lambda employee:employee["salary"]>50000,employees))
# print(high_earner_50000)


def sorted_salary():
    sort_employe = sorted(employees, key=lambda employee: employee["salary"])
    for emp in sort_employe:
        print(emp["name"], emp["salary"])


def grouping_department():
    grouped = {}
    for employee in employees:
        department = employee["department"]
        if department not in grouped:
            grouped[department] = []
        grouped[department].append(employee)
    #  print(grouped)

    for department, employee_list in grouped.items():

        total_salary = sum(employee["salary"] for employee in employee_list)

        average_salary = total_salary / len(employee_list)

        print(department, average_salary)


# grouping_department()
def second_highest():
    second_highest = sorted(
        set(employee["salary"] for employee in employees), reverse=True
    )[1]

    print(second_highest)
