# Base Class
class Person:
    def __init__(self, name, email, age):
        self.name = name
        self.email = email
        self.age = age

    def display_dashboard(self):
        print("Person Dashboard")


# Child Class - Student
class Student(Person):
    def __init__(self, name, email, age, course_name, marks):
        super().__init__(name, email, age)
        self.course_name = course_name
        self.marks = marks

    # Method Overriding
    def display_dashboard(self):
        print("\n----- Student Dashboard -----")
        print("Name:", self.name)
        print("Email:", self.email)
        print("Age:", self.age)
        print("Course:", self.course_name)
        print("Marks:", self.marks)


# Child Class - Teacher
class Teacher(Person):
    def __init__(self, name, email, age, subject_name, salary):
        super().__init__(name, email, age)
        self.subject_name = subject_name
        self.salary = salary

    # Method Overriding
    def display_dashboard(self):
        print("\n----- Teacher Dashboard -----")
        print("Name:", self.name)
        print("Email:", self.email)
        print("Age:", self.age)
        print("Subject:", self.subject_name)
        print("Salary:", self.salary)


# Creating Student Object
student = Student(
    "Tejasva",
    "tejasva@gmail.com",
    20,
    "Python",
    88
)

# Creating Teacher Object
teacher = Teacher(
    "Amit",
    "amit@gmail.com",
    35,
    "Computer Science",
    50000
)

# Calling Overridden Methods
student.display_dashboard()
teacher.display_dashboard()