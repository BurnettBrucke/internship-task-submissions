import json

file_name = "employees.json"

try:
    with open(file_name, "r") as file:
        employees = json.load(file)

except FileNotFoundError:
    employees = {}

except json.JSONDecodeError:
    print("Error: JSON file is invalid.")
    employees = {}


emp_id = input("Enter employee ID: ")

if emp_id in employees:
    print("Error: Employee ID already exists.")

else:
    name = input("Enter employee name: ")
    salary = input("Enter salary: ")

    if not salary.isdigit() or int(salary) <= 0:
        print("Error: Salary must be greater than 0.")

    else:
        employees[emp_id] = {
            "name": name,
            "salary": int(salary)
        }

        with open(file_name, "w") as file:
            json.dump(employees, file, indent=4)

        print("Employee added successfully.")