'''Task 2: File Handling and JSON
Create task_2_file_handling.py and store data in employees.json.
• Add employee details: ID, name, email, department and salary.
• Save employee details to a JSON file.
• Read and display all employee details.
• Search for an employee by ID.
• Update an employee department or salary.
• Delete an employee.
• Display the total number of employees.
Requirements
• Use the json module and with open(...).
• Handle missing files and invalid JSON data.
• Prevent duplicate employee IDs.'''


import json
# hand missing file and invalid json format  
try:
    with open("employee.json",'r') as file:
        employees=json.load(file)
except FileNotFoundError:
    print("json file not found")
    employees=[]
except json.JSONDecodeError:
    print("invalid json data")
    employees=[]

# • Add employee details: ID, name, email, department and salary.
while True:

    emp_id=int(input("enter employee id: "))

    duplicate=False
    for employee in employees:
        if employee['id']==emp_id:
            duplicate=True
            break
    if duplicate:
        print("employee already present ")
    else:
        # emp_id = int(input("Enter ID: "))
        name = input("Enter Name: ")
        email = input("Enter Email: ")
        dept = input("Enter Department: ")
        while True:
            try:
                salary=float(input("enter a salary: "))
                if salary<=0:
                    print("salary must be greater than zero")
                else:
                    break
            except ValueError:
                print("please enter valid salary")
        employee={
                'id': emp_id,
                'name': name,
                'email': email,
                'dept': dept,
                'salary': salary
        }

        employees.append(employee) # in list append data as dictionary 
        print("employee added")

    choice = input("want to add more (y/n)")
    if choice!='y':
        break
print(employees) 
print("\n")


#  Save employee details to a JSON file.
with open("employee.json",'w') as file:
    json.dump(employees,file,indent=4)


# • Read and display all employee details.
# with open("employee.json",'r') as file:
#     employees=json.load(file)
print("\nemployees detail")
for employee in employees:
    print(employee)
print('\n')

# Search for an employee by ID.

# with open("employee.json",'r') as file:
#     employees=json.load(file)
serach_id=int(input("enter id you want to serach :"))

for employee in employees:
    if employee['id']==serach_id:
        print(employee)
        break
else:
    print("employee not found")

#  Update an employee department or salary.
# with open("employee.json", "r") as file:
#     employees = json.load(file)

update_id = int(input("enter employee id: "))
for employee in employees:

    if employee['id']==update_id:
        choice=input("department or salary : ").lower()

        if choice=='department':
            employee['dept']=input("new dept: ")
        elif choice=='salary':
            while True:
                try:
                    salary=float(input("enter a salary: "))
                    if salary<=0:
                        print("salary must be greater than zero")
                    else:
                        break
                except ValueError:
                    print("please enter valid salary")
        print(employee)
        break
else:
    print("employee not found")
# update to json also
with open('employee.json','w')as file:
    json.dump(employees,file,indent=4) #inden=4 for spacing and formating

#  Delete an employee.
# with open("employee.json",'r') as file:
#     employees=json.load(file)

delete_id=int(input("enter id you want to delete : "))
for employee in employees:
    if employee['id'] == delete_id:
        employees.remove(employee)
        print("employee deleted succesfully")
        break
else: 
    print("employee not found")
# save again 
with open("employee.json",'w') as file:
    json.dump(employees,file,indent=4)

#  Display the total number of employees.
# with open('employee.json','r') as file:
#     employees=json.load(file)

no_of_employee=len(employees)
print(f"total no of employees:{no_of_employee}")

print("/n all  employees")
for i in employees:
    print(i)


