class Person:
    def __init__(self, name, email, age):
        self.name = name
        self.email = email
        self.age = age

class Student(Person):
    def __init__(self, name, email, age, course_name, marks):
        super().__init__(name, email, age)  
        self.course_name = course_name
        self.marks = marks
    
    def dashboard(self):
        print("Name : ", self.name)
        print("Email Id : ", self.email)
        print("Age : ", self.age)
        print("Course Name : ", self.course_name)
        print("Marks : ", self.marks)

# sonali = Student('Sonali','sonali@gmail.com',23,'BE',864)
# sonali.dashboard()

class Teacher(Person):
    def __init__(self, name, email, age, subject_name, salary):
        super().__init__(name, email, age)
        self.subject_name = subject_name
        self.salary = salary
    
    def dashboard(self):
        print("Name : ", self.name)
        print("Email Id : ", self.email)
        print("Age : ", self.age)
        print("Subject Name : ", self.subject_name)
        print("Salary : ", self.salary)


sunita = Teacher('Sunita','sunita@gmail.com',23,'Science',25000)
sunita.dashboard()