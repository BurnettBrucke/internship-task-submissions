# Task 7: Object-Oriented Programming
# Create a base class named Person.
# The class should contain:
#  Name
#  Email
#  Age
# Create two child classes:
#  Student
#  Teacher
# The Student class should contain:
#  Course name
#  Marks
#  A method to display the student dashboard
# The Teacher class should contain:
#  Subject name
#  Salary
#  A method to display the teacher dashboard
# Use method overriding to provide different dashboard output for students and teachers.

class Person:
    def __init__(self,name:str,email:str,age:int):
        self.name=name
        self.email=email
        self.age=age
    def display_dashboard(self):
        print("Person Dashboard")
        print(f"Name  : {self.name}")
        print(f"Email : {self.email}")
        print(f"Age   : {self.age}")

class Student(Person):
    def __init__(self, name:str, email:str, age:int, course_name:str, marks:int):
        super().__init__(name, email, age)
        self.course_name=course_name
        self.marks=marks
    def display_dashboard(self):
        """
        Overridden method for student dashboard.
        """
        print("\n===== Student Dashboard =====")
        print(f"Name        : {self.name}")
        print(f"Email       : {self.email}")
        print(f"Age         : {self.age}")
        print(f"Course Name : {self.course_name}")
        print(f"Marks       : {self.marks}")
class Teacher(Person):
    def __init__(self, name:str, email:str, age:int, subject_name:str, salary:float):
        super().__init__(name, email, age, )
        self.subject_name=subject_name
        self.salary=salary
    
    def display_dashboard(self):
        """
        Overridden method for teacher dashboard.
        """
        print("\n===== Teacher Dashboard =====")
        print(f"Name         : {self.name}")
        print(f"Email        : {self.email}")
        print(f"Age          : {self.age}")
        print(f"Subject Name : {self.subject_name}")
        print(f"Salary       : Rs.{self.salary}")

# Creating Student Object
student = Student(
    "Nancy",
    "nancy@gmail.com",
    23,
    "Python",
    92
)

# Creating Teacher Object
teacher = Teacher(
    "Rahul",
    "rahul@gmail.com",
    35,
    "Python Programming",
    65000
)

# Display Dashboards
student.display_dashboard()
teacher.display_dashboard()