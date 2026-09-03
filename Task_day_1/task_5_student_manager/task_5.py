# Build a menu-driven program with these options:
import json

students = {}
def get_marks():
    marks = {}

    subjects = ["English", "Hindi", "Maths"]

    for subject in subjects:
        while True:
            try:
                mark = int(input(f"Enter marks for {subject}: "))

                if 0 <= mark <= 100:
                    marks[subject] = mark
                    break
                else:
                    print("Marks must be between 0 and 100.")

            except ValueError:
                print("Please enter a valid number.")

    return marks

def calculate_total(marks):
    return sum(marks.values())

def calculate_average(marks):
    if not marks:
        return 0

    return sum(marks.values()) / len(marks)

def is_pass(marks):
    return all(mark >= 40 for mark in marks.values())

def find_student(name):
    return students.get(name)

def add_student():
    name = input("Enter student name: ").strip()

    if not name:
        print("Student name cannot be empty.")
        return

    if name in students:
        print("Student already exists.")
        return

    students[name] = get_marks()

    print("Student added successfully.")

def update_marks():
    name = input("Enter student name: ").strip()

    if name not in students:
        print("Student not found.")
        return

    print("Enter new marks:")
    students[name] = get_marks()

    print("Marks updated successfully.")

def delete_student():
    name = input("Enter student name: ").strip()

    if name not in students:
        print("Student not found.")
        return

    del students[name]

    print("Student deleted successfully.")

def view_students():
    if not students:
        print("No students available.")
        return

    for name, marks in students.items():

        print("\nName:", name)

        print("English:", marks["English"])
        print("Hindi:", marks["Hindi"])
        print("Maths:", marks["Maths"])

        total = calculate_total(marks)
        average = calculate_average(marks)

        print("Total:", total)
        print("Average:", f"{average:.2f}")
        print("Result:", "Pass" if is_pass(marks) else "Fail")

def search_student():
    name = input("Enter student name to search: ").strip()

    student = find_student(name)

    if student is None:
        print("Student not found.")
        return

    print("Name:", name)
    print("English:", student["English"])
    print("Hindi:", student["Hindi"])
    print("Maths:", student["Maths"])
    print("Total:", calculate_total(student))
    print("Average:", calculate_average(student))
    print("Result:", "Pass" if is_pass(student) else "Fail")

def display_result():
    if not students:
        print("No students available.")
        return

    for name, marks in students.items():
        result = "Pass" if is_pass(marks) else "Fail"
        print(name, ":", result)

def highest_scorer():
    if not students:
        print("No students available.")
        return

    highest_name = max(
        students,
        key=lambda name: calculate_total(students[name])
    )

    highest_marks = students[highest_name]
    total = calculate_total(highest_marks)

    print("Highest-scoring student:", highest_name)
    print("English:", highest_marks["English"])
    print("Hindi:", highest_marks["Hindi"])
    print("Maths:", highest_marks["Maths"])
    print("Total:", total)

def save_data():
    with open("students.json", "w") as file:
        json.dump(students, file, indent=4)

    print("Data saved successfully.")

def load_data():
    global students

    try:
        with open("students.json", "r") as file:
            students = json.load(file)

        print("Data loaded successfully.")

    except FileNotFoundError:
        print("No saved data found.")

def menu():
    while True:
        print("\n............. Student Marks Manager .............")
        print("1. Add student")
        print("2. Update marks")
        print("3. Delete student")
        print("4. View all students")
        print("5. Search by name")
        print("6. Calculate total and average")
        print("7. Display pass or fail")
        print("8. Display highest-scoring student")
        print("9. Save data")
        print("10. Load data")
        print("11. Exit")

        choice = input("Enter your choice: ").strip()

        if choice == "1":
            add_student()

        elif choice == "2":
            update_marks()

        elif choice == "3":
            delete_student()

        elif choice == "4":
            view_students()

        elif choice == "5":
            search_student()

        elif choice == "6":
            name = input("Enter student name: ").strip()

            if name in students:
                marks = students[name]
                print("Total:", calculate_total(marks))
                print("Average:", calculate_average(marks))
            else:
                print("Student not found.")

        elif choice == "7":
            display_result()

        elif choice == "8":
            highest_scorer()

        elif choice == "9":
            save_data()

        elif choice == "10":
            load_data()

        elif choice == "11":
            print("Program ended.")
            break

        else:
            print("Invalid choice. Please select a valid option.")

menu()