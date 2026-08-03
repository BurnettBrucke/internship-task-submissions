from fastapi import FastAPI,HTTPException,status
import services
from schemas import StudentCreate,ResponseModel,StudentUpdate


app =FastAPI()

@app.get("/")
def home():
    return {"message":"fastapi is working"}

@app.get("/health")
def health():
    return {'status':"running"}

@app.get("/about")
def about():
    return {"name":"vikas gurjar",
            "collage":"ips academy"}

@app.get("/students",response_model=list[ResponseModel],status_code=status.HTTP_200_OK)
def get_std():
    return services.get_students()

# to get any specific student
@app.get("/students/{student_id}",status_code=status.HTTP_200_OK)
def get_std(student_id:int):
    student=services.get_student(student_id)
    if student is None:
        raise HTTPException(
            status_code=404,
            detail="student not found"
        )
    return student


# post method add student

# @app.post("/students")
# def create_student(student:StudentCreate):
#     print(student)
#     return services.create_student(student)
   

@app.post("/student",response_model=ResponseModel,status_code=status.HTTP_201_CREATED)
def create_student(student:StudentCreate):
    return services.create_student(student)

# patch method partial update 
# i wnat to my marks
@app.patch("/students/{student_id}",status_code=status.HTTP_200_OK)
def update_student(
    student_id:int,
    student:StudentUpdate):
    

    updated_data=student.model_dump(exclude_unset=True)

    updated_student=services.update_student(student_id,updated_data)

    print(student.model_dump())
    print(student.model_dump(exclude_unset=True))
    if updated_student is None:
        raise HTTPException(status_code=404,
                            detail="student not found")
    return updated_student

# delete path
@app.delete('/students/{student_id}', status_code=status.HTTP_204_NO_CONTENT)
def delete_student(student_id:int):
    delete=services.delete_update(student_id)
    if not delete:
        raise HTTPException(status_code=404,
                            detail="student not found")


# query parameter
@app.get("/filter_students",status_code=status.HTTP_200_OK)
def get_std(min_marks:float=None,
            active:bool=None):
    print("min marks:",min_marks)
    print("active status:",active)
    return services.get_students(min_marks,active)

# pagination
@app.get("/some_student",status_code=status.HTTP_200_OK)
def get_student(skip:int=0,limit:int=5):
    return services.pagination(skip,limit)  

# pagination
@app.get("/filter_some_student",status_code=status.HTTP_200_OK)
def get_student(skip:int=0,
                limit:int=5,
                min_marks:float=None,
                active:bool=None):
    return services.pagination(skip,limit,min_marks,active)  
