# Task 5: Dictionary Program
# Create a student marks management program.
# The program should allow the user to:
#  Add a student.
#  Store marks for three subjects.
#  Calculate total marks.
#  Calculate average marks.
#  Display pass or fail status.
#  Display the student with the highest marks.

students = {}

# Number of students
n = int(input("Enter the number of students: "))

# Add student details
for i in range(n):
    print(f"\nEnter details for Student {i+1}")

    name = input("Enter student name: ")

    sub1 = int(input("Enter marks in Subject 1: "))
    sub2 = int(input("Enter marks in Subject 2: "))
    sub3 = int(input("Enter marks in Subject 3: "))

    total = sub1 + sub2 + sub3
    average = total / 3

    if average >= 40:
        status = "Pass"
    else:
        status = "Fail"

    students[name] = {
        "Subject1": sub1,
        "Subject2": sub2,
        "Subject3": sub3,
        "Total": total,
        "Average": average,
        "Status": status
    }

# Display all student details
print("\n------ Student Report ------")
for name, details in students.items():
    print("\nStudent Name:", name)
    print("Subject 1:", details["Subject1"])
    print("Subject 2:", details["Subject2"])
    print("Subject 3:", details["Subject3"])
    print("Total Marks:", details["Total"])
    print("Average Marks:", round(details["Average"], 2))
    print("Result:", details["Status"])

# Find student with highest marks
highest_student = ""
highest_marks = 0

for name, details in students.items():
    if details["Total"] > highest_marks:
        highest_marks = details["Total"]
        highest_student = name

print("\n------ Highest Scorer ------")
print("Student Name:", highest_student)
print("Total Marks:", highest_marks)