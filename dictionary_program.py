students = {}

n = int(input("Enter the number of students: "))

for i in range(n):
    print("\nStudent", i + 1)

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
        "Subject 1": sub1,
        "Subject 2": sub2,
        "Subject 3": sub3,
        "Total": total,
        "Average": average,
        "Status": status
    }

print("\n----- Student Details -----")

highest_marks = 0
top_student = ""

for name, details in students.items():
    print("\nName:", name)
    print("Subject 1:", details["Subject 1"])
    print("Subject 2:", details["Subject 2"])
    print("Subject 3:", details["Subject 3"])
    print("Total:", details["Total"])
    print("Average:", round(details["Average"], 2))
    print("Status:", details["Status"])

    if details["Total"] > highest_marks:
        highest_marks = details["Total"]
        top_student = name

print("\n----- Top Student -----")
print("Name:", top_student)
print("Highest Marks:", highest_marks)
