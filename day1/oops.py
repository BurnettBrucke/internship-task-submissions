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
    def __init__(self,name,email,age):
        self.name=name
        self.email=email
        self.age=age

    
class  Student(Person):
    def __init__(self,name,email,age,course,marks):
        super().__init__(name,email,age)
        self.course=course
        self.marks=marks

    def display_info(self):
        print("-----student details-----")
        print(f"name : {self.name}")
        print(f"eamil : {self.email}")
        print(f"age : {self.age}")
        print(f"course : {self.course}")
        print(f"marks : {self.marks}")


class Teacher(Person):
    def __init__(self,name,email,age,subject,salary):
        super().__init__(name,email,age)
        self.subject=subject
        self.salary=salary
    def display_info(self):
        print("\n-----Teacher details-----")
        print(f"name : {self.name}")
        print(f"eamil : {self.email}")
        print(f"age : {self.age}")
        print(f"subject : {self.subject}")
        print(f"salary : {self.salary}")


vikas=Student('vikas','vk@gamil.com',22,'python',50)
vikas.display_info()
govind=Teacher('gv','gv@gamil.com',34,'dbms',50000)
govind.display_info()

    
        