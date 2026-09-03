# Create a base class named Person.

# The class should contain:
# Name
# Email
# Age

# Create two child classes:
# Student
# Teacher

# The Student class should contain:
# Course name
# Marks
# A method to display the student dashboard

# The Teacher class should contain:
# Subject name
# Salary
# A method to display the teacher dashboard

# Use method overriding to provide different dashboard output for students and teachers.

class Person:
    def __init__(self, name, email, age):
        self.name = name
        self.email = email
        self.age = age

    def person_dashboard(self):
        print("=====Person's Dashboard=====")
        print(f"Person's Name : {self.name}")
        print(f"Person's Email : {self.email}")
        print(f"Person's Age : {self.age}")

class Student(Person):
    def __init__(self, name, email, age, course_name, marks):
        super().__init__(name, email, age)
        self.course_name = course_name
        self.marks = marks

    def student_dashboard(self):
        print("======Student's Dashboard======")
        print("Name of student : ",self.name)
        print("Email of student : ",self.email)
        print("Age of student : ",self.age)
        print("Name of Course : ",self.course_name)
        print("Marks of Student : ",self.marks)
        
class Teacher(Person):
    def __init__(self, name, email, age, subject_name, salary):
        super().__init__(name, email, age)
        self.subject_name = subject_name
        self.salary = salary

    def teacher_dashboard(self):
        print("=====Teacher's Dashboard=====")
        print("Teacher's Name : ",self.name)
        print("Teacher's Email : ",self.email)
        print("Teacher's Age : ",self.age)
        print("Subject Name : ",self.subject_name)
        print("Teacher's salary : ",self.salary)

student_1 = Student("Deepika","deepika06@gmail.com",22,"Python",87)
teacher_1 = Teacher("Kapil","kapil111@gmail.com",55,"Web Development",60000)

student_1.student_dashboard()
teacher_1.teacher_dashboard()