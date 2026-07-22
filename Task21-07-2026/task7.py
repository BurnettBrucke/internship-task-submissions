'''Task 7: Object-Oriented Programming
Create a base class named Person.
The class should contain:

Name
Email
Age
Create two child classes:

Student
Teacher
The Student class should contain:

Course name
Marks
A method to display the student dashboard
The Teacher class should contain:

Subject name
Salary
A method to display the teacher dashboard
Use method overriding to provide different dashboard output for students and teachers.'''

class Person:

    def __init__(self, name, email, age):
        self.name = name
        self.email = email
        self.age = age

    def display_dashboard(self):
        print("Person Dashboard")


class Student(Person):

    def __init__(self, name, email, age, course_name, marks):
        super().__init__(name, email, age)
        self.course_name = course_name
        self.marks = marks

    def display_dashboard(self):
        print("\n----- Student Dashboard -----")
        print("Name :", self.name)
        print("Email :", self.email)
        print("Age :", self.age)
        print("Course :", self.course_name)
        print("Marks :", self.marks)


class Teacher(Person):

    def __init__(self, name, email, age, subject_name, salary):
        super().__init__(name, email, age)
        self.subject_name = subject_name
        self.salary = salary

    def display_dashboard(self):
        print("\n----- Teacher Dashboard -----")
        print("Name :", self.name)
        print("Email :", self.email)
        print("Age :", self.age)
        print("Subject :", self.subject_name)
        print("Salary :", self.salary)

while True:

    print("\n===== MENU =====")
    print("1. Student Dashboard")
    print("2. Teacher Dashboard")
    print("3. Exit")

    choice = input("Enter your choice: ")

    if choice == "1":

        name = input("Enter Student Name: ")
        email = input("Enter Email: ")
        age = int(input("Enter Age: "))
        course = input("Enter Course Name: ")
        marks = float(input("Enter Marks: "))

        student = Student(name, email, age, course, marks)
        student.display_dashboard()

    elif choice == "2":

        name = input("Enter Teacher Name: ")
        email = input("Enter Email: ")
        age = int(input("Enter Age: "))
        subject = input("Enter Subject Name: ")
        salary = float(input("Enter Salary: "))

        teacher = Teacher(name, email, age, subject, salary)
        teacher.display_dashboard()

    elif choice == "3":
        print("Thank You!")
        break

    else:
        print("Invalid Choice.")