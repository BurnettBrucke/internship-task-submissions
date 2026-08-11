#Task 5: Dictionary Program
#Create a student marks management program.
#The program should allow the user to:

#Add a student.
#Store marks for three subjects.
#Calculate total marks.
#Calculate average marks.
#Display pass or fail status.
#Display the student with the highest marks.

student = {}

while True :

    press = input("do you want to add student information (yes/no):")
    if press.lower() != 'yes':
        break
    name = input("enter your name:")
    maths_marks = int(input("enter your maths marks:"))
    hindi_marks = int(input("enter your hindi marks:"))
    science_marks = int(input("enter your science marks:"))

    total_marks = maths_marks + hindi_marks + science_marks
    avg_marks = total_marks / 3
    student['name'] = name
    student['maths_marks'] = maths_marks    
    student['hindi_marks'] = hindi_marks
    student['science_marks'] = science_marks
    student['total_marks'] = total_marks
    student['avg_marks'] = avg_marks

    if avg_marks <35:
        student['status'] = 'fail'

    student['status'] = 'pass'

    for key, value in student.items():
        print(f"{key}: {value}")

    