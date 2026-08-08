# # Create task_2_file_handling.py and store data in employees.json.
# # Requirements
# # • Use the json module and with open(...).
# # • Validate salary and display meaningful error messages.


import json
import os

FILE_NAME = "employees.json"

def load_employees():
    """Load employees from JSON file."""
    if not os.path.exists(FILE_NAME):
        return []

    try:
        with open(FILE_NAME, "r") as file:
            data = json.load(file)

            if not isinstance(data, list):
                print("Error: Invalid JSON format. Resetting employee data.")
                return []

            return data

    except json.JSONDecodeError:
        print("Error: Invalid JSON data in file.")
        return []

    except Exception as e:
        print("Error:", e)
        return []


def save_employees(employees):
    """Save employees to JSON file."""
    try:
        with open(FILE_NAME, "w") as file:
            json.dump(employees, file, indent=4)
    except Exception as e:
        print("Error saving file:", e)


def add_employee():
    employees = load_employees()
    emp_id = input("Enter Employee ID: ")

    # Prevent duplicate IDs
    for emp in employees:
        if emp["id"] == emp_id:
            print("Error: Employee ID already exists.")
            return

    name = input("Enter Name: ")
    email = input("Enter Email: ")
    department = input("Enter Department: ")

    try:
        salary = float(input("Enter Salary: "))
        if salary < 0:
            print("Error: Salary cannot be negative.")
            return
    except ValueError:
        print("Error: Invalid salary.")
        return

    employee = {
        "id": emp_id,
        "name": name,
        "email": email,
        "department": department,
        "salary": salary
    }

    employees.append(employee)
    save_employees(employees)
    print("Employee added successfully.")


def display_employees():
    employees = load_employees()

    if not employees:
        print("No employees found.")
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


def search_employee():
    employees = load_employees()

    emp_id = input("Enter Employee ID to search: ")

    for emp in employees:
        if emp["id"] == emp_id:
            print("\nEmployee Found")
            for key, value in emp.items():
                print(f"{key.title()}: {value}")
            return

    print("Employee not found.")


def update_employee():
    employees = load_employees()

    emp_id = input("Enter Employee ID to update: ")

    for emp in employees:
        if emp["id"] == emp_id:
            print("1. Update Department")
            print("2. Update Salary")

            choice = input("Enter choice: ")

            if choice == "1":
                emp["department"] = input("Enter New Department: ")
                save_employees(employees)
                print("Department updated successfully.")

            elif choice == "2":
                try:
                    salary = float(input("Enter New Salary: "))
                    if salary < 0:
                        print("Error: Salary cannot be negative.")
                        return
                    emp["salary"] = salary
                    save_employees(employees)
                    print("Salary updated successfully.")
                except ValueError:
                    print("Error: Invalid salary.")
            else:
                print("Invalid choice.")
            return

    print("Employee not found.")


def delete_employee():
    employees = load_employees()

    emp_id = input("Enter Employee ID to delete: ")

    for emp in employees:
        if emp["id"] == emp_id:
            employees.remove(emp)
            save_employees(employees)
            print("Employee deleted successfully.")
            return

    print("Employee not found.")


def total_employees():
    employees = load_employees()
    print("Total Employees:", len(employees))


def menu():
    while True:
        print("\n===== Employee Management System =====")
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
            print("Exiting program...")
            break
        else:
            print("Invalid choice. Please try again.")


if __name__ == "__main__":
    menu()

'''
### Features included

* ✅ Add employee (ID, name, email, department, salary)
* ✅ Save data to `employees.json`
* ✅ Read and display all employees
* ✅ Search employee by ID
* ✅ Update department or salary
* ✅ Delete employee
* ✅ Display total number of employees
* ✅ Uses `json` module and `with open(...)`
* ✅ Handles missing file
* ✅ Handles invalid JSON data
* ✅ Prevents duplicate employee IDs
* ✅ Validates salary and displays meaningful error messages
'''