import json

FILE_NAME = "employees.json"

def load_data():
    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except:
        return []

def save_data(data):
    with open(FILE_NAME, "w") as file:
        json.dump(data, file, indent=4)

def add_employee():
    employees = load_data()

    emp = {
        "id": input("Enter ID: "),
        "name": input("Enter Name: "),
        "email": input("Enter Email: "),
        "department": input("Enter Department: "),
        "salary": input("Enter Salary: ")
    }

    employees.append(emp)
    save_data(employees)
    print("Employee Added Successfully.\n")

def display_employee():
    employees = load_data()

    if len(employees) == 0:
        print("No Employee Found\n")
        return

    print("\nEmployee Details")
    for emp in employees:
        print(emp)
    print()

def search_employee():
    employees = load_data()

    emp_id = input("Enter Employee ID: ")

    for emp in employees:
        if emp["id"] == emp_id:
            print(emp)
            return

    print("Employee Not Found\n")

def update_employee():
    employees = load_data()

    emp_id = input("Enter Employee ID: ")

    for emp in employees:
        if emp["id"] == emp_id:
            emp["department"] = input("Enter New Department: ")
            emp["salary"] = input("Enter New Salary: ")

            save_data(employees)

            print("Employee Updated Successfully\n")
            return

    print("Employee Not Found\n")

def delete_employee():
    employees = load_data()

    emp_id = input("Enter Employee ID: ")

    for emp in employees:
        if emp["id"] == emp_id:
            employees.remove(emp)

            save_data(employees)

            print("Employee Deleted Successfully\n")
            return

    print("Employee Not Found\n")

def total_employee():
    employees = load_data()

    print("Total Employees =", len(employees), "\n")

while True:

    print("===== Employee Management System =====")
    print("1. Add Employee")
    print("2. Display Employees")
    print("3. Search Employee")
    print("4. Update Employee")
    print("5. Delete Employee")
    print("6. Total Employees")
    print("7. Exit")

    choice = input("Enter Choice: ")

    if choice == "1":
        add_employee()

    elif choice == "2":
        display_employee()

    elif choice == "3":
        search_employee()

    elif choice == "4":
        update_employee()

    elif choice == "5":
        delete_employee()

    elif choice == "6":
        total_employee()

    elif choice == "7":
        print("Program Closed.")
        break

    else:
        print("Invalid Choice\n")