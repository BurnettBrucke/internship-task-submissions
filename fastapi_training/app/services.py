from data import students
# student list was on data.py 

# to get all students
def get_students():
    return students

# to get any specific student
def get_student(student_id):
    for student in students:
        if student["id"]==student_id:
            return student
    return None

# to add student
def create_student(student):
    new_student=student.model_dump()
    new_student['id']=len(students)+1
    students.append(new_student)
    return new_student

# to update student
def update_student(student_id,student_data):
    for student in students:
        if student['id']==student_id:
            student.update(student_data)
            return student
    return None

# to delete student
def delete_update(student_id):
    for student in students:
        if student['id']==student_id:
            students.remove(student)
            return True
    return False

def get_students(min_marks=None,
                 active=None):
    result=students

    if min_marks is not None:
        result=[student for student in result
                if student['marks']>=min_marks]
    if active is not None:
            result=[student for student in result
                    if student['active']==active]
        
    return result

def pagination(skip=0,limit=0,min_marks=None,active=None):
    result=students
    
    if min_marks is not None:
        result=[student for student in result
                if student['marks']>=min_marks]
    if active is not None:
            result=[student for student in result
                    if student['active']==active]
            
    return result[skip:skip+limit]
    