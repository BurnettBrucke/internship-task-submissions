
import json

FILE_NAME = "employees.json"



def load_data():
    """Load employee data from JSON file."""
    try:
        with open(FILE_NAME, "r") as file:
            return json.load(file)

    except FileNotFoundError:
        return []

    except json.JSONDecodeError:
        print("Error: JSON file contains invalid data.")
        return []



def save_data(employees):
    """Save employee data to JSON file."""
    with open(FILE_NAME, "w") as file:
        json.dump(employees, file, indent=4)



def add_employee():
    employees = load_data()

    emp_id = input("Enter Employee ID: ")

    # Prevent duplicate IDs
    for emp in employees:
        if emp["id"] == emp_id:
            print("Error: Employee ID already exists.")
            return

    name = input("Enter Name: ")
    email = input("Enter Email: ")
    department = input("Enter Department: ")

    # Validate salary
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
    save_data(employees)

    print("Employee added successfully.")



def display_employees():
    employees = load_data()

    if not employees:
        print("No employee records found.")
        return

    print("\nEmployee Details")
    print("-" * 50)

    for emp in employees:
        print(f"ID         : {emp['id']}")
        print(f"Name       : {emp['name']}")
        print(f"Email      : {emp['email']}")
        print(f"Department : {emp['department']}")
        print(f"Salary     : {emp['salary']}")
        print("-" * 50)



def search_employee():
    employees = load_data()

    emp_id = input("Enter Employee ID to search: ")

    for emp in employees:
        if emp["id"] == emp_id:
            print("\nEmployee Found")
            print(emp)
            return

    print("Employee not found.")



def update_employee():
    employees = load_data()

    emp_id = input("Enter Employee ID: ")

    for emp in employees:

        if emp["id"] == emp_id:

            print("1. Update Department")
            print("2. Update Salary")

            choice = input("Enter choice: ")

            if choice == "1":
                emp["department"] = input("Enter new department: ")
                print("Department updated.")

            elif choice == "2":
                try:
                    salary = float(input("Enter new salary: "))
                    if salary < 0:
                        print("Salary cannot be negative.")
                        return
                    emp["salary"] = salary
                    print("Salary updated.")

                except ValueError:
                    print("Invalid salary.")
                    return

            else:
                print("Invalid choice.")
                return

            save_data(employees)
            return

    print("Employee not found.")



def delete_employee():
    employees = load_data()

    emp_id = input("Enter Employee ID: ")

    for emp in employees:
        if emp["id"] == emp_id:
            employees.remove(emp)
            save_data(employees)
            print("Employee deleted successfully.")
            return

    print("Employee not found.")



def total_employees():
    employees = load_data()
    print("Total Employees:", len(employees))



def main():
    while True:

        print("\n===== Employee Management =====")
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
            print("Invalid choice. Try again.")


main()