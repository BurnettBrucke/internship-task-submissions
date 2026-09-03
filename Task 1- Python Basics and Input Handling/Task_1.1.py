#* Take name, age, email and city from the user and display a formatted introduction
name = input("Enter your name : ")
if not name:
    print("Name cannot be empty")

try:
    age = int(input("Enter your age : "))
except ValueError:
    print("Age must be in numbers")
else:
    print(f"I am {age} years old.")

email = input("Enter your email address : ")
if not email:
    print("Email cannot be empty")

city = input("Enter your city : ")
if not city:
    print("City cannot be empty")

print(f"My name is {name}.")

print(f"My email address is {email}.")
print(f"I am from {city}.")