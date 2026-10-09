# Create task_2_file_handling.py and store data in employees.json.
import json

FILE_NAME = "employees.json"

def validate_salary(salary):
    """Validate salary value."""

    if salary == "":
        raise ValueError("Salary cannot be empty.")

    try:
        salary = float(salary)
    except ValueError:
        raise ValueError("Salary must be a number.")

    if salary < 0:
        raise ValueError("Salary cannot be negative.")

    return salary


def load_employees():
    """Load employee data from the JSON file."""

    try:
        with open(FILE_NAME, "r") as file:
            employees = json.load(file)

            if not isinstance(employees, list):
                raise ValueError("Invalid JSON data.")

            return employees

    except FileNotFoundError:
        return []

    except json.JSONDecodeError:
        print("Error: employees.json contains invalid JSON data.")
        return []


def save_employees(employees):
    """Save employee data to the JSON file."""

    with open(FILE_NAME, "w") as file:
        json.dump(employees, file, indent=4)


def add_employee():
    """Add a new employee."""

    employees = load_employees()

    employee_id = input("Enter employee ID: ")

    if not employee_id or not employee_id.isdigit():
        print("Error: Employee ID must be a non-empty numeric value.")
        return
    
    for employee in employees:
        if str(employee["id"]) == employee_id:
            print("Error: Employee ID already exists.")
            return

    name = input("Enter employee name: ")
    email = input("Enter employee email: ")
    department = input("Enter department: ")

    salary = input("Enter salary: ")

    try:
        salary = validate_salary(salary)
    except ValueError as error:
        print("Error:", error)
        return

    employee = {
        "id": employee_id,
        "name": name,
        "email": email,
        "department": department,
        "salary": salary
    }

    employees.append(employee)

    save_employees(employees)

    print("Employee added successfully.")


def display_employees():
    """Display all employees."""

    employees = load_employees()

    if not employees:
        print("No employees found.")
        return

    print("\n....... Employee Details .......")

    for employee in employees:
        print("ID:", employee["id"])
        print("Name:", employee["name"])
        print("Email:", employee["email"])
        print("Department:", employee["department"])
        print("Salary:", employee["salary"])
        print("----------------------------")


def search_employee():
    """Search for an employee by ID."""

    employees = load_employees()

    employee_id = input("Enter employee ID to search: ")

    for employee in employees:
        if str(employee["id"]) == employee_id:
            print("\nEmployee found:")
            print("ID:", employee["id"])
            print("Name:", employee["name"])
            print("Email:", employee["email"])
            print("Department:", employee["department"])
            print("Salary:", employee["salary"])
            return

    print("Error: Employee not found.")

def update_employee():
    """Update employee department or salary."""

    employees = load_employees()

    employee_id = input("Enter employee ID to update: ")

    for employee in employees:
        if str(employee["id"]) == employee_id:

            print("\n1. Update Department")
            print("2. Update Salary")

            choice = input("Enter your choice: ")

            if choice == "1":
                new_department = input("Enter new department: ")

                employee["department"] = new_department

                save_employees(employees)

                print("Department updated successfully.")
                return

            elif choice == "2":
                new_salary = input("Enter new salary: ")

                try:
                    new_salary = validate_salary(new_salary)
                except ValueError as error:
                    print("Error:", error)
                    return

                employee["salary"] = new_salary

                save_employees(employees)

                print("Salary updated successfully.")
                return

            else:
                print("Error: Invalid choice.")
                return

    print("Error: Employee not found.")

def delete_employee():
    """Delete an employee by ID."""

    employees = load_employees()

    employee_id = input("Enter employee ID to delete: ")

    for employee in employees:
        if str(employee["id"]) == employee_id:

            employees.remove(employee)

            save_employees(employees)

            print("Employee deleted successfully.")
            return

    print("Error: Employee not found.")

def employee_count():
    """Display the total number of employees."""

    employees = load_employees()

    print("Total employees:", len(employees))


def main():
    """Run the employee management program."""

    while True:

        print("\n....... Employee Management System .......")
        print("1. Add Employee")
        print("2. Display All Employees")
        print("3. Search Employee")
        print("4. Update Employee")
        print("5. Delete Employee")
        print("6. Display Employee Count")
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
            employee_count()

        elif choice == "7":
            print("Program ended.")
            break

        else:
            print("Error: Invalid choice.")

if __name__ == "__main__":
    main()