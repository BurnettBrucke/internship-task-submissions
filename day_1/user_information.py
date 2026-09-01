
def user_info(name, age, email, city):
    print('/n---------------------------------------------')
    print(f" Name  : {name}")
    print(f" Age   : {age} years old")
    print(f" Email : {email}")
    print(f" City  : {city}")
    print('/n---------------------------------------------')

user_name = input("Enter your name: ")
user_age = input("Enter your age: ")
user_email = input("Enter your email: ")
user_city = input("Enter your city: ")


user_info(user_name, user_age, user_email, user_city)
