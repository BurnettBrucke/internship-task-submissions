'''
Task 5: Dictionary Program
Create a student marks management program.
The program should allow the user to:

Add a student.
Store marks for three subjects.
Calculate total marks.
Calculate average marks.
Display pass or fail status.
Display the student with the highest marks.'''

students={}
n=int(input("enter no of student:"))
for i in range(n):
    name=input("enter student name :")

    marks1=int(input("enter a marks of maths:"))
    marks2=int(input("enter a marks of science:"))
    marks3=int(input("enter a marks of english:"))
    
    total=marks1+marks2+marks3
    avg=total/3

    if avg>+40:
        status='pass'
    else:
        status="fail"

    students[name]={
        "name":name,
        "marks1":marks1,
        "marks2":marks2,
        "marks3":marks3,
        "total":total,
        "avrage":avg,
        "status":status
    }

print("students\n")
for i in students:
    print(f"{students[name]}\n")

highest_marks=0
top_student=''

for i in students:
    if students[i]["total"]>highest_marks:
        highest_marks=students[i]['total']
        top_student=i
print("\n top student :",top_student)
print("highest marks:",highest_marks)
