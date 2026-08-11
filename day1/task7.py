#Task 7: Object-Oriented Programming
#Create a base class named Person.
#The class should contain:
#Name,Email,Age

#Create two child classes:
#Student,Teacher

#The Student class should contain:
#Course name,Marks
#A method to display the student dashboard
#The Teacher class should contain:
#Subject name,Salary

#A method to display the teacher dashboard
#Use method overriding to provide different dashboard output for students and teachers.

class Person:
    def __init__(self,name:str,email:str,age:int):
        self.name = name
        self.email = email
        self.age = age

class Student(Person):
     def __init__(self, name: str, email: str, age: int,
                 course: str, marks: int):
        super().__init__(name,email,age)
        self.course = course
        self.marks = marks

        def display_dashboard(self):
            print(f"Student Name : {self.name}")
            print(f"Student Email : {self.email}")
            print(f"Student Age : {self.age}")
            print(f"Student Course : {self.course}")
            print(f"Student Marks : {self.marks}")

class Teacher(Person):
    def __init__(self, name: str, email: str, age: int,
                 subject: str, salary: int):
        super.__init(name,email,age)

        self.subject = subject
        self.salary = salary

    def display_dashboard(self):
        print(f"Teacher Name : {self.name}")
        print(f"Teacher Subject : {self.subject}")
        print(f"Teacher Salary : {self.salary}")

student = Student("subhi","subhi@gmail.com",20,"python",56)
teacher = Teacher("ram","ram@gmail.com",30,"python",50000)

student.display_dashboard()
teacher.display_dashboard()