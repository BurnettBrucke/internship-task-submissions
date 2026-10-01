#Take name, age, email and city from the user and display a formatted introduction.

while True:
    name = input("Enter your name: ").strip()

    if name:
        break
    else:
        print("Error: Name cannot be empty.")

while True:
    age = input("Enter your age: ").strip()

    if not age:
        print("Error:Age cannot be empty.")
        continue

    try:
        age = int(age)

        if age < 0:
            print("Error:Age cannot be negative.")
        else:
            break

    except ValueError:
        print("Error:Please enter a valid numeric age.")


while True:
    email = input("Enter your email: ").strip()

    if email:
        break
    else:
        print("Error:Email cannot be empty.")

while True:
    city = input("Enter your city: ").strip()

    if city:
        break
    else:
        print("Error:City cannot be empty.")

print( f"My name is {name}, I am {age} years old. "f"I live in {city}. My email address is {email}.")