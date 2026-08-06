## Burnett Brucke Internship

# Project Name

training_project 

# How to run project at local machine

First of all you should have Python 3 installed on your system

after that create a virtual environment using command 

->  python virtualenv ("your venv name")

then activate it using command 

->  my_env/Scripts/activate

then install all packages using command

->  pip install -r requirements.txt

after installation, 

create database tables using command

->  python manage.py makemigrations

then apply all migrations using command 

->  python manage.py migrate

then create super user using command

->  python manage.py createsuperuser

just run your server using command

->  python manage.py runserver

then go to

->  http://127.0.0.1:8000/   for dashboard page

->  http://127.0.0.1:8000/home  for home page

->  http://127.0.0.1:8000/students  for students page

->  http://127.0.0.1:8000/students/1  for specific student page

->  http://127.0.0.1:8000/students/add    for add new student

->  http://127.0.0.1:8000/students/1/edit   for update specific student details 

->  http://127.0.0.1:8000/students/1/delete   for delete specific student




