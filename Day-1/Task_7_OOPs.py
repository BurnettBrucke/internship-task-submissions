#base class 
class Person():
    def __init__(self , name:str , email: str  , age:int):
        self.name = name 
        self.email = email
        self.age = age
    def display_person_details(self):
        print("Hello", self.name)
        print("Your email : " , self.email)
        print("Your age : ",self.age)

    def display_dashboard(self):
        print("Person Dashboard")

#child class
class Student(Person):
    def __init__(self, name: str, email: str, age: int, course_name: str, marks: int):
        super().__init__(name, email, age)
        self.course_name = course_name
        self.marks = marks

    def display_dashboard(self): # Method overriding
        print("\n--- Student Dashboard ---")
        print("Name:", self.name)
        print("Email:", self.email)
        print("Age:", self.age)
        print("Course Name:", self.course_name)
        print("Marks:", self.marks)

#child class
class Teacher(Person):
    def __init__(self, name : str , email : str , age : int , subject_name : str , salary: int):
        super().__init__(name , email , age)
        self.subject_name =subject_name 
        self.salary = salary

    def display_dashboard(self): # Method overriding
        print("\n--- Teacher Dashboard ---")
        print("Name:", self.name)
        print("Email:", self.email)
        print("Age:", self.age)
        print("Subject Name:", self.subject_name)
        print("Salary:", self.salary)


student = Student(
    input("Enter student name: "),
    input("Enter student email: "),
    int(input("Enter student age: ")),
    input("Enter course name: "),
    int(input("Enter marks: "))
)
student.display_dashboard()

teacher = Teacher(
    input("\nEnter teacher name: "),
    input("Enter teacher email: "),
    int(input("Enter teacher age: ")),
    input("Enter subject name: "),
    int(input("Enter salary: "))
)
teacher.display_dashboard()