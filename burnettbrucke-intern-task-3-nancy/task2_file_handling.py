"""
Task 2: File Handling and JSON
Create task_2_file_handling.py and store data in employees.json.
• Add employee details: ID, name, email, department and salary.
• Save employee details to a JSON file.
• Read and display all employee details.
• Search for an employee by ID.
• Update an employee department or salary.
• Delete an employee.
• Display the total number of employees.

"""
import json

FILE_NAME = "employees.json"


# Load data from JSON file
def load_data():
    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []


# Save data to JSON file
def save_data(data):
    with open(FILE_NAME, "w") as file:
        json.dump(data, file, indent=4)


# Add employee
def add_employee():
    employees = load_data()

    emp = {
        "id": input("Enter ID: "),
        "name": input("Enter Name: "),
        "email": input("Enter Email: "),
        "department": input("Enter Department: "),
        "salary": float(input("Enter Salary: "))
    }

    employees.append(emp)
    save_data(employees)
    print("Employee added successfully.\n")


# Display all employees
def display_employees():
    employees = load_data()

    if not employees:
        print("No employee found.\n")
        return

    for emp in employees:
        print(emp)
    print()


# Search employee by ID
def search_employee():
    employees = load_data()
    emp_id = input("Enter Employee ID to search: ")

    for emp in employees:
        if emp["id"] == emp_id:
            print("Employee Found:")
            print(emp)
            return

    print("Employee not found.\n")


# Update department or salary
def update_employee():
    employees = load_data()
    emp_id = input("Enter Employee ID to update: ")

    for emp in employees:
        if emp["id"] == emp_id:
            print("1. Update Department")
            print("2. Update Salary")
            choice = input("Enter choice: ")

            if choice == "1":
                emp["department"] = input("Enter New Department: ")
            elif choice == "2":
                emp["salary"] = float(input("Enter New Salary: "))
            else:
                print("Invalid choice.")
                return

            save_data(employees)
            print("Employee updated successfully.\n")
            return

    print("Employee not found.\n")


# Delete employee
def delete_employee():
    employees = load_data()
    emp_id = input("Enter Employee ID to delete: ")

    for emp in employees:
        if emp["id"] == emp_id:
            employees.remove(emp)
            save_data(employees)
            print("Employee deleted successfully.\n")
            return

    print("Employee not found.\n")


# Count employees
def total_employees():
    employees = load_data()
    print("Total Employees:", len(employees))
    print()


# Menu
while True:
    print("===== Employee Management =====")
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
        display_employees()
    elif choice == "3":
        search_employee()
    elif choice == "4":
        update_employee()
    elif choice == "5":
        delete_employee()
    elif choice == "6":
        total_employees()
    elif choice == "7":
        print("Program Closed.")
        break
    else:
        print("Invalid choice.\n")