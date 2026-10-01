
import json 
from pathlib import Path

DATABASE_PATH = Path(__file__).parent / "employees.json"

def get_valid_salary():
    """
    Prompt the user to enter a valid salary value.
    Returns:
        float: A valid salary value.
    """
    try:
        salary = float(input("Enter salary: "))
        if salary < 0:
            raise ValueError("Salary cannot be negative.")
        return salary
    except ValueError:
        print("Please enter a valid salary.")
        return get_valid_salary()
def validate_string(prompt):
    """
    Prompt the user to enter a string value.
    Returns:
        str: A valid string value.
    """
    while True:
        value = input(prompt).strip()
        if value:
            return value
        print("Input cannot be empty. Please try again.")
def load_json(file_path):
    """
    Load data from a JSON file.
    Args:
        file_path (str): The path to the JSON file.
    Returns:
        dict: The data loaded from the JSON file.
    """

    try:
        if file_path:
            with open(file_path, "r") as f:
                print(f"Loading data from {file_path}...")
                data = json.load(f)
                return {
                    int(employee_id): employee_data
                    for employee_id, employee_data in data.items()}
        else:
            print("Please provide a JSON file.")
            return {}
        
    except FileNotFoundError:
        print("File not found.")
        return {}
    
    except json.JSONDecodeError:
        print("JSON file is empty or contains invalid data.")
        return {}

def display_employees(employees):
    """
    Display the details of all employees.
    """
    if not employees:
        print("No employee data available.")
    else:
        for emp_id , emp_data in employees.items():
            print(f"Employee ID: {emp_id}")
            for key, value in emp_data.items():
                print(f"{key.capitalize()}: {value}")
            print()

def search_employee(employees):
    """
    Search for an employee by ID.
    """
    try:
        employee_id = int(input("Enter employee ID to search: "))
        if not employee_id:
            print("Employee ID cannot be empty.")
            return
        if employee_id < 0:
            print("Employee ID cannot be negative.")
            return
        if employee_id in employees:
            employee = employees[employee_id]
            print("Employee found:")
            print("=============Employee Details=============")
            print(f"Employee ID: {employee_id}")
            for key, value in employee.items():
                print(f"{key.capitalize()}: {value}")
    except ValueError:
        print("Please enter a valid integer for employee ID.")

def add_employee(employees):
    """
    Add a new employee to the employees dictionary.
    """
    try:
        employee_id =int(input("Enter employee ID: "))
        if not employee_id:
            print("Employee ID cannot be empty.")
            return
        if employee_id <= 0:
            print("Employee ID must be a positive integer.")
            return

        if employee_id in employees:
            print(f"Employee with ID {employee_id} already exists.")
            return
        name = validate_string("Enter employee name: ")
        email = validate_string("Enter employee email: ")
        department = validate_string("Enter employee department: ")
        salary = get_valid_salary()
        employees[employee_id] = {
            "name": name,
            "email": email,
            "department": department,
            "salary": salary
        }
        print(f"Employee with ID {employee_id} added successfully.")
        save_to_json(DATABASE_PATH , employees)
    except ValueError:
        print("Please enter a valid integer for employee ID.")
def update_employee(employees):
    """
    Update the details of an existing employee.
    """
    try:
        employee_id = int(input("Enter employee ID to update: "))
        if not employee_id:
            print("Employee ID cannot be empty.")
            return
        if employee_id <= 0:
            print("Employee ID must be a positive integer.")
            return
        if employee_id in employees:
            print("Employee found, Enter details to update (skip to keep old detail)")
            employee = employees[employee_id]
            name = (input("Enter employee name: ")).strip()
            if name == "":
                name = employee["name"]
            email = input("Enter employee email: ").strip()
            if email == "":
                email = employee["email"]
            department = input("Enter employee department: ").strip()
            if department == "":
                department = employee["department"]
            salary_input = input("Enter new salary (press Enter to keep old): ").strip()

            if salary_input:
                try:
                    salary = float(salary_input)

                    if salary <= 0:
                        print("Salary must be greater than 0.")
                        return

                except ValueError:
                    print("Please enter a valid salary.")
                    return
            else:
                salary = employee["salary"]
                employees[employee_id] = {
                "name": name,
                "email": email,
                "department": department,
                "salary": salary
            }
            print(f"Employee with ID {employee_id} updated successfully.")
            save_to_json(DATABASE_PATH, employees)
        else:
            print(f"Employee with ID {employee_id} not found.")
    except ValueError:
        print("Please enter a valid integer for employee ID.")
def delete_employee(employees):
    """
    Delete an employee from the employees dictionary.
    """
    try:
        employee_id = int( input("Enter employee ID to delete: "))
        if not employee_id:
            print("Employee ID cannot be empty.")
            return
        if employee_id in employees:
            del employees[employee_id]
            save_to_json(DATABASE_PATH, employees)
            print(f"Employee with ID {employee_id} deleted successfully.")
        else:
            print(f"Employee with ID {employee_id} not found.")
    except ValueError:
        print("Please enter a valid integer for employee ID.")
def count_employees(employees):
    """
    count the number of employees
    """
    print(f"Total number of employees: {len(employees)}")

def save_to_json(file_path, data):
    """
    Save data to a json file
    """
    try:
        with open(file_path, "w") as f:
            json.dump(data, f, indent=4)
            print(f"Data saved to {file_path}.")
    except Exception as e:
        print(f"Error saving data to JSON: {e}")

def main():
    employees_data = load_json(DATABASE_PATH)
    print("|=================================================|")
    print("|           Welcome to employeee system           |")
    print("|=================================================|")
    print("| Press 1 for load data from a json file          |")
    print("| Press 2 for add an employee                     |")
    print("| Press 3 for display all employees               |")
    print("| Press 4 for count all the employees             |")
    print("| Press 5 for search an employee by ID            |")
    print("| Press 6 for delete an employee                  |")
    print("| Press 7 for update an employee                  |")
    print("| Press 8 for save the data in a json file        |")
    print("| Press 9 for exit                                |")
    print("|=================================================|")
    print("| Please enter your choice:                       |")
    choice = input("|=> ").strip()
    print("|=================================================|")
    match choice:
        case "1":
            file_path = input("Enter the path to the JSON file: ")
            loaded_employees = load_json(file_path)
            if loaded_employees:
                employees_data.clear()
                employees_data.update(loaded_employees)
                print("Data loaded successfully.")
            else:
                print("No data found in the JSON file.")
        case "2":
            add_employee(employees_data)
        case "3":
            display_employees(employees_data)
        case "4":
            count_employees(employees_data)
        case "5":
            search_employee(employees_data)
        case "6":
            delete_employee(employees_data)
        case "7":
            update_employee(employees_data)
        case "8":
            save_to_json(DATABASE_PATH, employees_data)
        case "9":
            print("Thannk you for using the program...")
            print("")
            exit()
        case _:
            print("Please enter a vaild input.")

while True:
    main()