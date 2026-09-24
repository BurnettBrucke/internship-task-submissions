#Helper funtion for Validate int and string 
def get_number(prompt):
    while True:
        try:
            return float(input(prompt))
        except ValueError:
            print("Invalid input. Please enter a number.")

def get_non_empty_input(prompt):
    while True:
        value = input(prompt).strip()

        if value:
            return value
        print("Input can't be empty, Please try again.")

def get_user_details():
    name = get_non_empty_input("Enter your Name : ")
    age = int(input("Enter your age : "))
    if age < 0 or age > 110:
        print("please enter a valid age.")
        age = int(input("Enter your age : "))
    gmail = get_non_empty_input("Enter your gmail : ")
    city = get_non_empty_input("Enter your city : ")

    return name, age, gmail, city

def introduction(name,age,gmail,city):
    print()
    print(f"Hello {name}, Welcome to the python basics program.")
    print(f"Your age is {age}.")
    print(f"Your gamil is {gmail}.")
    print(f"Your city is {city}")
    print("Thank you for details.")

def calculator():
    first_number = get_number("Enter the first number : ")
    second_number = get_number("Enter the Second number :")
    print("select the operation")
    print("+ for addition | - for subtraction | * for multiplication | / for divison | % for modulus")
    operation = str(input("Enter opreration : "))
    match operation:
        case "+":
            result = first_number + second_number
        case "-":
            result = first_number - second_number
        case "*":
            result = first_number * second_number
        case "/":
            if second_number == 0:
                print("Cannot divide or perform modulus by zero.")
                return
            result = first_number / second_number
        case "%":
            if second_number == 0:
                print("Cannot divide or perform modulus by zero.")
                return
            result = first_number % second_number
        case _:
            print("Invalid operation. Please choose +, -, *, / or %.")
            return
    print(f"{first_number} {operation} {second_number} = {result}")

def temparature_convertion():
    print("Welcome to the temparature convertion program")
    temp = get_number("Enter temperature in Celsius:")
    fahrenheit = (temp * 1.8) + 32
    print(f"Converted temparature is : {fahrenheit}F")

def rectangle_calculator():
    length = get_number("Enter the length : ")
    width = get_number("Enter the width : ")
    area = length * width
    perimeter = 2 * (length + width)
    print(f"The area of the rectangle is : {area}, and perimeter is : {perimeter}")

def calculate_salary():
    current_salary = get_number("Enter your current salary : ")
    increment = current_salary * 0.18
    incremented_salary = current_salary + increment
    print(f"Your increment amount is {increment}. So the final salary is {incremented_salary}")        
def main():
    print("------------(Introduction)-----------")
    name , age , gmail , city = get_user_details()

    introduction(name , age , gmail,city)

    print("------------(Calculator)-------------")
    calculator()

    print("-------(temparature_convertion)---------")
    temparature_convertion()

    print("--------(rectangle_calculator)--------")
    rectangle_calculator()

    print("----(salary increment calculator)----")
    calculate_salary()

if __name__ == "__main__":
    main()

    