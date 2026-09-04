import json
import time
import json
from pathlib import Path

DATABASE_PATH = Path(__file__).parent / "database" / "students_saved.json"

def get_valid_mark():
    while True:
        try:
            mark = float(input("Enter marks: "))

            if 0 <= mark <= 100:
                return mark
            print("Marks must be between 0 and 100.")

        except ValueError:
            print("Please enter a valid number.")
def fatching_data(students):
    name = input("Enter the student name : ").capitalize().strip()
    for name in students:
        if name in students:
            print("Student already exists.")
            return
    if not name:
        print("please enter student name.")
        return
    print("Enter maths marks")
    sub1_marks = get_valid_mark()
    print("Enter python marks")
    sub2_marks = get_valid_mark()
    print("Enter english marks")
    sub3_marks = get_valid_mark()
    new_data = {name:{"math" : sub1_marks , "python" : sub2_marks , "english": sub3_marks}}
    return new_data
def add_students(students , new_data):
    for name in new_data:
        if name in students:
            print("Student already exists")
        else:
            students.update(new_data)

def update_marks(students , new_data):
    for name in new_data:
        if name in students:
            print("student is found.")
            students.update(new_data)
            print(f"{students[name]} marks is updated sucessfully.")

def display_students(students):
    print("Displaying all students...")
    for name , marks in students.items():
        print(f"\nStudent : {name}")
        print(f"Math: {marks['math']}")
        print(f"Python: {marks['python']}")
        print(f"English: {marks['english']}")


def delete_Student(students):
    name_search = input("Enter the name of the student:").capitalize().strip()

    if not name_search:
        print("Please enter student name.")
        return
    if name_search in students:
        del students[name_search]
        print(f"{name_search} data is deleted sucessfully.")

def search_student(students):
    name_search = (input("Enter the name of the student: ")).capitalize().strip()

    if not name_search:
        print("Please enter student name.")
        return

    if name_search in students:
        marks = students[name_search]

        total = sum(marks.values())
        average = total / len(marks)

        print(f"Name: {name_search}")
        print(f"Marks: {marks}")
        print(f"Total Marks: {total}")
        print(f"Average Marks: {average:.2f}")

    else:
        print("Student not found.")

def result_check(students):
    for name , marks in students.items():
        if all(mark >= 40 for mark in marks.values()):
            print(f"{name}: PASS")
        else:
            print(f"{name}: FAIL") 


def student_rank(students , rank:int):
    totals = {}
    for name, marks in students.items():
        totals[name] = sum(marks.values())

    sorted_students = sorted(totals.items(),key=lambda x: x[1],reverse=True)

    if rank > len(sorted_students) or rank <= 0:
        print("Invalid rank")
        return

    name, total = sorted_students[rank - 1]

    print(f"Rank {rank}: {name}")
    print(f"Total Marks: {total}")

def save_json(students):
    with open("Day-1/database/students_saved.json", "w") as f:
        json.dump(students, f, indent=4)

def load_json(file_path):
    try:
        if file_path:
            with open(file_path, "r") as f:
                print(f"Loading data from {file_path}...")
                return json.load(f)

        else:
            print("Please provide a JSON file.")
            return {}

    except FileNotFoundError:
        print("File not found.")
        return {}

    except json.JSONDecodeError:
        print("JSON file is empty or contains invalid data.")
        return {}
def main():
    students = load_json(DATABASE_PATH)
    while True:
        print("\n\n")
        time.sleep(1)
        print("Please wait while the program is loading...")
        time.sleep(0.5)
        print("|==============================================|")
        display_msg = "|        WElCOME TO THE MARKS MANAGER          |"
        for char in display_msg:
            print(char, end="", flush=True)
            time.sleep(0.05)
        print("\n|==============================================|")
        print("|==============================================|")
        print("| Press 1 for displaying all students          |")
        print("| Press 2 for searching a student              |")
        print("| Press 3 for updating marks                   |")
        print("| Press 4 for adding a new student             |")
        print("| Press 5 for delete a student                 |")
        print("| Press 6 for result                           |")
        print("| Press 7 for student rank                     |")
        print("| Press 8 for save data to JSON file           |")
        print("| Press 9 for load data from JSON file         |")
        print("| Press 0 for exit                             |")
        print("|==============================================|")
        print("| Please enter your choice:                    |")
        choice = input("|=> ").strip()
        print("|==============================================|")
        match choice:
            case "1":
                display_students(students)
            case "2":
                search_student(students)
            case "3":
                new_data = fatching_data(students)
                if new_data:
                    update_marks(students , new_data)
            case "4":
                new_data = fatching_data(students)
                if new_data:
                    add_students(students , new_data)

            case "5":
                delete_Student(students)
            case "6":
                result_check(students)
            
            case "7":
                try:
                    rank = int(input("Enter the rank you want to check: "))
                    student_rank(students , rank)
                except ValueError:
                    print("Please enter a valid integer for the rank.")
            case "0":
                print("Thank you for using the program.")
                print("Exiting the program...")

                return
            case "8":
                save_json(students)
            case "9":
                file_path = input("Enter the path to the JSON file: ")
                loaded_students = load_json(file_path)
                if loaded_students:
                    students.clear()
                    students.update(loaded_students)
                    print("Data loaded successfully.")
                else:
                    print("No data found in the JSON file.")
            case _:
                print("Invalid choice. Please try again.")


if __name__ == "__main__":
    main()

