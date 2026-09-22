# Task 7: Object-Oriented Programming

class Person:
    def __init__(self, name, email, age):
        self.name = name
        self.email = email
        self.age = age

    def display_dashboard(self):
        print("Person Dashboard")
        print(f"Name: {self.name}")
        print(f"Email: {self.email}")
        print(f"Age: {self.age}")


class Student(Person):
    def __init__(self, name, email, age, course_name, marks):
        super().__init__(name, email, age)
        self.course_name = course_name
        self.marks = marks

    # Method overriding
    def display_dashboard(self):
        print("\n... Student Dashboard ...")
        print(f"Name: {self.name}")
        print(f"Email: {self.email}")
        print(f"Age: {self.age}")
        print(f"Course: {self.course_name}")
        print(f"Marks: {self.marks}")


class Teacher(Person):
    def __init__(self, name, email, age, subject_name, salary):
        super().__init__(name, email, age)
        self.subject_name = subject_name
        self.salary = salary

    # Method overriding
    def display_dashboard(self):
        print("\n... Teacher Dashboard ...")
        print(f"Name: {self.name}")
        print(f"Email: {self.email}")
        print(f"Age: {self.age}")
        print(f"Subject: {self.subject_name}")
        print(f"Salary: {self.salary}")


# Creating Student object
student = Student(
    "Riya",
    "riya@gmail.com",
    21,
    "Python Development",
    85
)

# Creating Teacher object
teacher = Teacher(
    "Ruchita",
    "ruchi@gmail.com",
    25,
    "Python",
    50000
)

# Display dashboards
student.display_dashboard()
teacher.display_dashboard()