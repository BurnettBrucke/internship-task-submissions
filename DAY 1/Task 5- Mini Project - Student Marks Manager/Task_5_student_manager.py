# Build a menu-driven program with these options:
# • Add a student and marks for three subjects.
# • Update marks.
# • Delete a student.
# • View all students.
# • Search by name.
# • Calculate total and average.
# • Display pass or fail.
# • Display the highest-scoring student.
# • Exit.

import json

students = {}


#  ADD STUDENT 
def add_student():
    name = input("Enter student name: ").strip()

    if name in students:
        print("Student already exists!")
        return

    marks = []

    for subject in ["English", "Maths", "Science"]:
        while True:
            try:
                mark = float(input(f"Enter marks for {subject} (0-100): "))

                if 0 <= mark <= 100:
                    marks.append(mark)
                    break
                else:
                    print("Marks must be between 0 and 100.")

            except ValueError:
                print("Please enter a valid number.")

    students[name] = {
        "English": marks[0],
        "Maths": marks[1],
        "Science": marks[2]
    }

    print("Student added successfully!")


# UPDATE MARKS 
def update_marks():
    name = input("Enter student name: ").strip()

    if name not in students:
        print("Student not found!")
        return

    print("Enter new marks:")

    for subject in students[name]:
        while True:
            try:
                mark = float(input(f"{subject} (0-100): "))

                if 0 <= mark <= 100:
                    students[name][subject] = mark
                    break
                else:
                    print("Marks must be between 0 and 100.")

            except ValueError:
                print("Please enter a valid number.")

    print("Marks updated successfully!")


# DELETE STUDENT 
def delete_student():
    name = input("Enter student name: ").strip()

    if name in students:
        del students[name]
        print("Student deleted successfully!")
    else:
        print("Student not found!")


# VIEW ALL STUDENTS 
def view_all_students():
    if not students:
        print("No students available.")
        return

    print("\n------ ALL STUDENTS ------")

    for name, marks in students.items():
        print(f"\nName: {name}")
        print(f"English: {marks['English']}")
        print(f"Maths: {marks['Maths']}")
        print(f"Science: {marks['Science']}")


#  SEARCH BY NAME
def search_student():
    name = input("Enter student name to search: ").strip()

    if name in students:
        print("\nStudent Found!")
        print(f"Name: {name}")

        for subject, mark in students[name].items():
            print(f"{subject}: {mark}")
    else:
        print("Student not found!")


# TOTAL AND AVERAGE
def calculate_total_average():
    name = input("Enter student name: ").strip()

    if name not in students:
        print("Student not found!")
        return

    marks = students[name]

    total = sum(marks.values())
    average = total / 3

    print(f"\nStudent: {name}")
    print(f"Total Marks: {total}")
    print(f"Average Marks: {average:.2f}")


# PASS OR FAIL
def pass_or_fail():
    name = input("Enter student name: ").strip()

    if name not in students:
        print("Student not found!")
        return

    marks = students[name]

    if all(mark >= 40 for mark in marks.values()):
        print(f"{name} has PASSED.")
    else:
        print(f"{name} has FAILED.")


# HIGHEST SCORING STUDENT
def highest_student():
    if not students:
        print("No students available.")
        return

    highest_name = None
    highest_total = -1

    for name, marks in students.items():
        total = sum(marks.values())

        if total > highest_total:
            highest_total = total
            highest_name = name

    average = highest_total / 3

    print("\n------ HIGHEST SCORING STUDENT ------")
    print(f"Name: {highest_name}")
    print(f"Total Marks: {highest_total}")
    print(f"Average: {average:.2f}")


# SAVE DATA TO JSON
def save_data():
    with open("students.json", "w") as file:
        json.dump(students, file, indent=4)

    print("Data saved successfully!")


# LOAD DATA FROM JSON
def load_data():
    global students

    try:
        with open("students.json", "r") as file:
            students = json.load(file)

        print("Data loaded successfully!")

    except FileNotFoundError:
        print("No previous data found. Starting with empty data.")


# ---------------- MENU ----------------
def menu():
    while True:
        print("\n==============================")
        print("     STUDENT MANAGEMENT")
        print("==============================")
        print("1. Add Student")
        print("2. Update Marks")
        print("3. Delete Student")
        print("4. View All Students")
        print("5. Search Student")
        print("6. Calculate Total & Average")
        print("7. Display Pass or Fail")
        print("8. Display Highest-Scoring Student")
        print("9. Save Data")
        print("10. Load Data")
        print("11. Exit")
        print("==============================")

        choice = input("Enter your choice: ")

        if choice == "1":
            add_student()

        elif choice == "2":
            update_marks()

        elif choice == "3":
            delete_student()

        elif choice == "4":
            view_all_students()

        elif choice == "5":
            search_student()

        elif choice == "6":
            calculate_total_average()

        elif choice == "7":
            pass_or_fail()

        elif choice == "8":
            highest_student()

        elif choice == "9":
            save_data()

        elif choice == "10":
            load_data()

        elif choice == "11":
            print("Thank you! Program exited.")
            break

        else:
            print("Invalid choice! Please enter a number from 1 to 11.")


# ---------------- START PROGRAM ----------------
load_data()
menu()