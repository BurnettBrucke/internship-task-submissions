class Person:
    def __init__(self,name,email,age):
        self.name=name
        self.email=email
        self.age=age
    
    def display(self):
        return f"""
    Name:{self.name}
    Email:{self.email}
    Age:{self.age}
    """
class Student(Person):
    def __init__(self, name, email, age,course_name,marks):
        super().__init__(name, email, age)
        self.course_name=course_name
        self.marks=marks
        
    def display(self):
        print("Student Dashboard")
        return f"""
    Name:{self.name}
    Email:{self.email}
    Age:{self.age}
    Course Name:{self.course_name}
    Marks:{self.marks}
    """

class Teacher(Person):
    def __init__(self,name,email,age,sub_name,salary):
        super().__init__(name,email,age)
        self.sub_name=sub_name
        self.salary=salary
        
    def display(self):
        print("Teacher Dashboard")
        return f"""
    Name:{self.name}
    Email:{self.email}
    Age:{self.age}
    Subject Name:{self.sub_name}
    Salary:{self.salary}
    """    

s1=Student("Sujal","Sujal004shasrma@gmail.com",22,"B.Tech",98)
print(s1.display())

t1=Teacher("Krati Mam","kratirathore27@gmail.com",22,"Psychology",100)
print(t1.display())