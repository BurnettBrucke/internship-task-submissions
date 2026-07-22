'''Task 5: Dictionary Program
Create a student marks management program.
The program should allow the user to:

Add a student.
Store marks for three subjects.
Calculate total marks.
Calculate average marks.
Display pass or fail status.
Display the student with the highest marks.'''

students = {}

n = int(input("Enter number of students: "))

for i in range(n):

    name = input("\nEnter student name: ")

    python = int(input("Enter Python marks: "))
    java = int(input("Enter Java marks: "))
    sql = int(input("Enter SQL marks: "))

    total = python + java + sql
    average = total / 3

    if python >= 33 and java >= 33 and sql >= 33:
        status = "Pass"
    else:
        status = "Fail"

    students[name] = {
        "Python": python,
        "Java": java,
        "SQL": sql,
        "Total": total,
        "Average": average,
        "Status": status
    }

print("\n------ Student Report ------")

for name, details in students.items():
    print("\nStudent:", name)

    for key, value in details.items():
        print(key, ":", value)

highest = 0
topper = ""

for name, details in students.items():
    if details["Total"] > highest:
        highest = details["Total"]
        topper = name

print("\nTopper :", topper)
print("Highest Marks :", highest)