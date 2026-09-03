# • Add employee details: ID, name, email, department and salary.
# • Save employee details to a JSON file.
# • Read and display all employee details.
# • Search for an employee by ID.
# • Update an employee department or salary.
# • Delete an employee.
# • Display the total number of employees.

# *************Requirements***********
# • Use the json module and with open(...).
# • Handle missing files and invalid JSON data.
# • Prevent duplicate employee IDs.
# • Validate salary and display meaningful error messages.

import json

FILE_NAME = "employees.json"


# Read employees from JSON file
def read_employees():
    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)

    except FileNotFoundError:
        return []

    except json.JSONDecodeError:
        print("Invalid JSON data.")
        return []


# Save employees to JSON file
def save_employees(employees):
    with open(FILE_NAME, "w") as file:
        json.dump(employees, file, indent=4)


# Add employee
def add_employee():
    employees = read_employees()

    employee_id = input("Enter Employee ID: ")

    # Check duplicate ID
    for employee in employees:
        if employee["id"] == employee_id:
            print("Employee ID already exists!")
            return

    name = input("Enter Name: ")
    email = input("Enter Email: ")
    department = input("Enter Department: ")
    salary = float(input("Enter Salary: "))

    employee = {
        "id": employee_id,
        "name": name,
        "email": email,
        "department": department,
        "salary": salary
    }

    employees.append(employee)

    save_employees(employees)

    print("Employee added successfully!")


# Display all employees
def display_employees():
    employees = read_employees()

    if len(employees) == 0:
        print("No employees found.")
        return

    print("\nAll Employees:")

    for employee in employees:
        print("--------------------")
        print("ID:", employee["id"])
        print("Name:", employee["name"])
        print("Email:", employee["email"])
        print("Department:", employee["department"])
        print("Salary:", employee["salary"])


# Search employee
def search_employee():
    employees = read_employees()

    employee_id = input("Enter Employee ID to search: ")

    for employee in employees:
        if employee["id"] == employee_id:
            print("\nEmployee Found!")
            print("ID:", employee["id"])
            print("Name:", employee["name"])
            print("Email:", employee["email"])
            print("Department:", employee["department"])
            print("Salary:", employee["salary"])
            return

    print("Employee not found.")


# Update employee
def update_employee():
    employees = read_employees()

    employee_id = input("Enter Employee ID to update: ")

    for employee in employees:

        if employee["id"] == employee_id:

            print("1. Update Department")
            print("2. Update Salary")

            choice = input("Enter choice: ")

            if choice == "1":
                employee["department"] = input(
                    "Enter new department: "
                )

                print("Department updated successfully!")

            elif choice == "2":
                employee["salary"] = float(
                    input("Enter new salary: ")
                )

                print("Salary updated successfully!")

            else:
                print("Invalid choice.")

            save_employees(employees)
            return

    print("Employee not found.")


# Delete employee
def delete_employee():
    employees = read_employees()

    employee_id = input("Enter Employee ID to delete: ")

    for employee in employees:

        if employee["id"] == employee_id:

            employees.remove(employee)

            save_employees(employees)

            print("Employee deleted successfully!")
            return

    print("Employee not found.")


# Count employees
def total_employees():
    employees = read_employees()

    print("Total Employees:", len(employees))


# Main menu
while True:

    print("\n===== Employee Management System =====")
    print("1. Add Employee")
    print("2. Display All Employees")
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
        print("Program ended.")
        break

    else:
        print("Invalid choice!")