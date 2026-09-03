class Person:
    def __init__(self):
        name = input("Enter your name: ")
        email = input("Enter email: ")
        age = int(input("Enter age: "))

        self.name = name
        self.email = email
        self.age = age


class Student(Person):
    def __init__(self):
        super().__init__()
        self.course_name = input("Enter the course name: ")
        self.marks = int(input("Enter the marks: "))

    def dashboard(self):
        print("============= Student's dashboard ============")
        print(f"Student's name: {self.name}")
        print(f"Student email: {self.email}")
        print(f"Student age: {self.age}")
        print(f"Student Course: {self.course_name}")
        print(f"Student marks: {self.marks}")


class Teacher(Person):
    def __init__(self):
        super().__init__()
        self.subject_name = input("Enter the Subject Name: ")
        self.salary = float(input("Enter the Salary you get: "))

    def dashboard(self):
        print("==== TEACHERS DASHBOARD ====")
        print(f"Teacher's name: {self.name}")
        print(f"Teacher's email: {self.email}")
        print(f"Teacher's age: {self.age}")
        print(f"Teacher's subject: {self.subject_name}")
        print(f"Teacher's salary: {self.salary}")


def main():
    your_role = input("Enter who are you student/teacher: ")
    if your_role.lower() == "teacher":
        teacher = Teacher()
        teacher.dashboard()
    else:
        student1 = Student()
        student1.dashboard()


main()
