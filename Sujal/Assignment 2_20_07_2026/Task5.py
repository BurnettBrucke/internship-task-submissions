students={}
class Students:
    def student_data(self,students):
        name=input("Enter the name of the Student:")
        id=int(input("Enter the id of Student"))
        
        if id in students:
            print("Already Exists")
            return
        
        english=float(input("Enter the Mark of English:"))
        hindi=float(input("Enter the Mark of Hindi")) 
        maths=float(input("Enter the Marks of Maths "))
    
        students[id]=[name,english,hindi,maths]
    
    def total_marks(self,students,id):
        if id not in students:
            print("Invalid Id")
            return
        total=students[id][1]+students[id][2]+students[id][3]
        return total

    def average_marks(self,students,id):
        if id not in students:
            print("Invalid Id")
            return
        return (self.total_marks(students,id))/3
        
    def result(self,students,id):
        if id not in students:
            print("Invalid Id")
            return
        avg=self.average_marks(students,id)
        if avg>= 33:
            print("Pass")
        else:
            print("Fail")
    
    def highest(self,students):
        highest_marks=float('-inf')
        for mark in students.keys():
            if self.total_marks(students,mark)>highest_marks:
                highest_marks=self.total_marks(students,mark)
                id=mark
        return highest_marks,id
                
while True:
    choice= int(input(f"""
    1.Add a student and Store marks for three subjects..
    2.Calculate total marks..
    3.Calculate average marks..
    4.Display pass or fail status..
    5.Display the student with the highest marks..
    6.Exit

    Enter your Choice
    """))
    match choice:
        case 1:
            Students().student_data(students)
        case 2:
            id=int(input("Enter the id of Student"))
            print(Students().total_marks(students,id))
        case 3:
            id=int(input("Enter the id of Student"))
            print(Students().average_marks(students,id))
        case 4:
            id=int(input("Enter the id of Student"))
            print(Students().result(students,id))
        case 5:
            print(Students().highest(students))
        case 6:
            break
        case _:
            print("Invalid Input")
        
        
        