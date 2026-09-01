
def get_valid_marks(prompt="Enter marks (0-100): "):
    while True:
        try:
            marks = float(input(prompt))
            if 0 <= marks <= 100:
                return marks  # 'return' automatically exits the loop and the function
            else:
                print("Error: Marks must be between 0 and 100. Please try again.")
        except ValueError:
            print("Error: Invalid input. Please enter a valid numeric value.")



def add_student():
      name=input("Enter the name of the student: ")
      
      if name in student:
                  print("Student Already Exist")
      else:
                  
                  math=get_valid_marks()
                  science=get_valid_marks()
                  english=get_valid_marks()
      
                  student[name]={
                       "math":math,
                       "science":science,
                       "english":english
                  }
                  print("Student Added Successfully")
# ----------------------------------------------------------------------------------------
def update():
       name=input("Enter your name: ")
       if name in student:
                   print(f"current marks,{student[name]}")
                   subject=input("Enter the subject to update (Maths/science/english): ")
                   if subject in student[name]:
                  
                     new_marks=get_valid_marks()
                     student[name][subject]=new_marks
                     print("Marks updated succesfully")
                   else:
                       print("Invalid Subject")
       else:
                       print("Student Not Found")

# -------------------------------------------------------------------------------------------
def delete_student():
       name=input("Enter Students name: ")
       if name in student:
                             del student[name]
                             print("Student deleted successfully")
       else:
                             print("Student not found")

# -------------------------------------------------------------------------------------------

def view_all():
       if not student:
                     print("No Student Found")
       else:
            print("==== All Students ====") 
            for name,marks in student.items():
                     print(f"Name: {name}")
                     print(f"Maths:{marks['math']}")
                     print(f"Science:{marks['science']}")
                     print(f"english:{marks['english']}")
# --------------------------------------------------------------------------------
def search_by_name():
       name=input("Enter the name you want to search: ")
       if name in student:
            print(f"name: {name}")
            print(f"marks: {student[name]}")
       else:
            print("Student Not Found")
# ------------------------------------------------------------------------------------
def calculate_total_average():
       name=input("Enter the name: ")
       if name in student:
            marks=student[name]
            total=sum(marks.values())
            average=total/len(marks)
       
            print(f"Total Marks: {total}")
            print(f"Average Marks: {average}")
       else:
            print("Student Not Found")
# -----------------------------------------------------------------------------------
def display_pass_fail():
       name=input("Enter name: ")
       if name in student:
             marks=student[name]
             if all(marks>40 for marks in marks.values()):
                     print(f"{name} has passed the exam")
             else:
                     print(f"{name} has failed the exam")
       
       else:
            print("Student not found")
# ----------------------------------------------------------------------------------
def highest_scoring_student():
       if not student:
            print("No Student Available") 
       else:
             highest_student=max(
                     student,
                      key=lambda name:sum(student[name].values())
              )
             total = sum(student[highest_student].values())
             print("===== HIGHEST SCORING STUDENT =====")
             print("Name:", highest_student)
             print("Total Marks:", total)
# ------------------------------------------------------------------------------------

student={}
while True:
    print("======== Student Marks Manager ============")
    print("1. Add Student")
    print("2. Update marks")
    print("3. Delete Student")
    print("4. View all")
    print("5. Search By Name")
    print("6. Calculate Total and Average")
    print("7. Display Pass or Fail")
    print("8. Display Highest Scoring Student")
    print("9. Exit")

    choice=input("Enter your Choice: ")

     
    if choice=='1':
        add_student()

    elif choice=='2':
        update()    
         
    elif choice=='3':
        delete_student()
                
    elif choice=='4':
        view_all()

    elif choice=='5':
        search_by_name()

    elif choice=='6':
        calculate_total_average()
                
    elif choice=='7':
        display_pass_fail()

    elif choice=='8':
        highest_scoring_student()

    elif choice == "9":
        print("Program exited successfully!")
        break
    else:
          print("Your choice is invalid!!")
                 





      
                