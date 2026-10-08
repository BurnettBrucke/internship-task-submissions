def user_input():
    name = input("Enter your name : ")
    age = int(input("Enter your age: "))
    email = input("Enter the Email: ")
    city = input("Enter the city: ")
    print()
    print(f"User's Name is {name}")
    print(f"User's Age is {age}")
    print(f"User's Email is {email}")
    print(f"User's City is {city}")


# user_input()


def calculator():

    try:
        a = int(input("Enter the first operand: "))
        b = int(input("Enter the second operand: "))
        operation = input("Enter the operation's symbol you need to perform: ")
        match operation:
            case "+":
                return print(a + b)
            case "-":
                return print(a - b)
            case "*":
                return print(a * b)
            case "%":
                return print(a % b)
            case "/":
                return print(a / b)
    except ZeroDivisionError:
        print("Error, You cannot divide by zero")


# calculator()


def celsius_to_farenheit():
    celsius = float(input("Enter the temprature in Celsius: "))
    farenheit = (celsius * 9 / 5) + 32
    print(f"The {celsius} degree Celsius in Farenheit would be {farenheit}")


# celsius_to_farenheit()


def rectangle_area():
    length = float(input("Enter the length of the reactangle: "))
    breadth = float(input("Enter the breadth of the reactangle: "))

    return print(f"Area of the Reactangle is {length*breadth}")


# rectangle_area()


def salary_increment():
    salary = int(input("Enter the Current Salary: "))
    return print(f"The salary after 18% increment is {salary+(salary*0.18)}")


salary_increment()
