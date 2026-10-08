import json
import re
import os
from sys import exception

employee_database = {}
filepath = r"Day2\employee.json"


def add_employee() -> str:
    emp_id = input("Enter Employee ID: ").strip()
    if emp_id in employee_database:
        print(f"empployee id {emp_id} already exist")

    name = input("Enter Employee Name: ").strip()
    email = input("Enter Employee Email: ").strip()
    department = input("Enter Department: ").strip()

    try:
        salary = float(input("Enter Salary: ").strip())
    except ValueError:
        return "Error: Salary must be a valid number."

    emailRegex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
    if re.match(emailRegex, email):
        f"Error,Invalid {email} format"
    if salary < 0:
        f"Error,Salary cannot be zero"
    employee_database[emp_id] = {
        "name": name,
        "email": email,
        "department": department,
        "salary": salary,
    }
    return f"success, {name} employee added successfully"


# ---------------------------------------------------------------------------------
def save_file() -> str:
    if not employee_database:
        return f"No databse exists!!!"

    try:
        directory = os.path.dirname(filepath)
        if directory:
            os.makedirs(directory, exist_ok=True)
        with open(filepath, mode="w", encoding="utf-8") as file:
            json.dump(employee_database, file, indent=4)
        return f"data is saved in the file {filepath}"
    except exception as e:
        return f"facing error in saving file"


# ----------------------------------------------------------------------------
def read_display_all() -> str:
    with open(filepath, mode="r", encoding="utf-8") as file:
        employee_data = json.load(file)
    print(employee_data)


# -----------------------------------------------------------------------------
def search_for_employee():
    emp_id = input("Enter the Employee ID of the employee you want to find: ")
    if emp_id in employee_database:
        print(employee_database[emp_id])


# ----------------------------------------------------------------------------------
def update_employee():
    save_file()
    emp_id = input("Enter the Employee ID: ")
    if emp_id in employee_database:
        field = input("Field you want to update: ")
        new_data = input(f"Enter the information you want to update in {field}: ")
        employee_database[emp_id][field] = new_data
        print(f"Field updated successfuly  {employee_database[emp_id]}")
    else:
        print("Employee with this ID does not exist")


# -------------------------------------------------------------------------
def delete_employee():
    emp_id = input("Enter the Employee ID you want to delete: ")
    if emp_id in employee_database:
        del employee_database[emp_id]
        print("Record Deleted Successfully!!")
        save_file()
    else:
        print("Could'nt find any employee with this ID")


# ----------------------------------------------------------------------------
def calculate_total_employees():

    print(f"Total number of Employees are: {len(employee_database)}")


# --------------------------------------------------------------------------------

while True:
    print("========= EMPLOYEE DATA HANDLING ==================")
    print("----- Choose the operation you want to perform: -----")
    print("1. To Add a Employee")
    print("2. To Save the JSON File")
    print("3. To Read and Display all Employees")
    print("4. To Search for an Employee based on Employee ID")
    print("5. To Update an Employee's Department or Salary")
    print("6. To Delete an Employee")
    print("7. To Display total number of Employee")
    print("8. To Exit")

    choice = input("Enter your choice: ")

    if choice == "1":
        print(add_employee())
    elif choice == "2":
        print(save_file())
    elif choice == "3":
        read_display_all()
    elif choice == "4":
        search_for_employee()
    elif choice == "5":
        update_employee()
    elif choice == "6":
        delete_employee()
    elif choice == "7":
        calculate_total_employees()
    elif choice == "8":
        break
    else:
        print("Make a valid Choice")
