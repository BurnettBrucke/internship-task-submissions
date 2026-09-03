#* Take name, age, email and city from the user and display a formatted introduction
while True:
    name = input("Enter your name : ")
    if name:
        break
    else:
        print("Name cannot be empty")

while True:
    age = input("Enter your age : ")
    if not age:
        print("Age cannot be empty.")
    try:
        age = int(age)
        if age<0:
            print("Age cannot be negative")
        else:
            break
    except ValueError:
        print("Please enter a valid numeric age.")
    

while True:
    email = input("Enter your email address : ")
    if email:
        break
    else:
        print("Email cannot be empty")

while True:
    city = input("Enter your city : ")
    if city:
        break
    else:
        print("City cannot be empty")

print(f"My name is {name}.")
print(f"I am {age} years old.")
print(f"My email address is {email}.")
print(f"I am from {city}.")