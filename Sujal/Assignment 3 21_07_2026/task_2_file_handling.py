import json

FILE_NAME = "employees.json"

def load_data():
    try:
        with open(FILE_NAME,'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("File not Found")
    except json.JSONDecodeError:
        print("Invalid JSON data found")
    
def save_data(employees):
    with open(FILE_NAME,'w') as f:
        json.dump(employees,f,indent=4)

def validate_salary(salary):
    if salary<0:
        raise ValueError("Salary cannot be negative")

def add_employee():
    employees=load_data()
    
    try:
        emp_id=int(input("Enter the employee id"))
    except ValueError:
        print("Employee id must be a integer")
        return
    
    for emp in employees:
        if emp["id"]==emp_id:
            print("Employee ID already Exist")
            return
    
    name=input("Enter the name of the Employee")
    email=input("Enter the Email of the Employee")
    department=input("Enter the department")
    
    try:
        salary=float(input("Enter the Salary of the Employee"))
    except ValueError as e:
        print(e)
        return

    employee={
        "id":emp_id,
        "name":name,
        "email":email,
        "department":department,
        "salary":salary
    }
    
    employees.append(employee)
    save_data(employees)
    
    print("Employee Added")

def display():
    employees=load_data()
    
    if not employees:
        print("No employee records found.\n")
        return

    print("\nEmployee Details")
    print("-" * 60)

    for emp in employees:
        print(f"ID         : {emp['id']}")
        print(f"Name       : {emp['name']}")
        print(f"Email      : {emp['email']}")
        print(f"Department : {emp['department']}")
        print(f"Salary     : {emp['salary']}")
        print("-" * 60)
    
def search():
    employees=load_data()
    
    try:
        emp_id=int(input("Enter the employee id"))
    except ValueError:
        print("Invalid Id")
        return

    for emp in employees:
        if emp["id"]==emp_id:
            print("Employee Exist")
            print(emp)
            return
    
    print("Employee not found")

def update():
    employees=load_data()
    
    try:
        emp_id=int(input("Enter the employee id"))
    except ValueError:
        print("Invalid Id")
        return
    for emp in employees:

        if emp["id"] == emp_id:

            print("1. Update Department")
            print("2. Update Salary")

            choice = input("Enter choice: ")

            if choice == "1":
                emp["department"] = input("Enter New Department: ")
                save_data(employees)
                print("Department updated successfully.")

            elif choice == "2":

                try:
                    salary = float(input("Enter New Salary: "))
                    validate_salary(salary)
                    emp["salary"] = salary
                    save_data(employees)
                    print("Salary updated successfully.")

                except ValueError as e:
                    print(e)
                    
def delete_employee():
    

    employees = load_data()

    try:
        emp_id = int(input("Enter Employee ID: "))
    except ValueError:
        print("Invalid ID.")
        return

    for emp in employees:
        if emp["id"] == emp_id:
            employees.remove(emp)
            save_data(employees)
            print("Employee deleted successfully.")
            return

    print("Employee not found.")


def total_employees():
    

    employees = load_data()

    print(f"\nTotal Employees: {len(employees)}\n")


def menu():

    while True:

        print("\n====== Employee Management System ======")
        print("1. Add Employee")
        print("2. Display Employees")
        print("3. Search Employee")
        print("4. Update Employee")
        print("5. Delete Employee")
        print("6. Total Employees")
        print("7. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_employee()

        elif choice == "2":
            display()

        elif choice == "3":
            search()

        elif choice == "4":
            update()

        elif choice == "5":
            delete_employee()

        elif choice == "6":
            total_employees()

        elif choice == "7":
            print("Exiting...")
            break

        else:
            print("Invalid choice.")

menu()