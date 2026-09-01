# Build a calculator for addition, subtraction, multiplication, division and modulus.

def add(*args):
    total = 0
    for num in args:
        total += num
    return total

def sub(*args):
    minus = args[0]
    for num in args:
        minus -= num
    return minus

def mul(*args):
    product = 1
    for num in args:
        product *= num
    return product

def div(a,b):
    try:
        result = a/b
    except ZeroDivisionError:
        print("Division by zero is not allowed. Please try again!")
        return None
    else:
        return result
    

def mod(a,b):
    try:
        return a % b
    except ZeroDivisionError:
        print("Division by zero is not allowed.")
        return None

while True:
    print("-----------SIMPLE CALCULATOR-------------")
    print("1. Addition")
    print("2. Subtraction")
    print("3. Multiplication")
    print("4. Division")
    print("5. Modulus")
    print("6. Exit")
    try: 
        ch = int(input("Enter your choice : "))
    except ValueError:
        print("Invalid Input, Please select 1 to 5")
        break

    if ch == 6:
        print("Calculator Closed.")
        break

    if ch == 1 or ch == 2 or ch == 3:
        n = int(input("How many numbers do you want to enter? : "))
        numbers = []
        for i in range(n):
            num = int(input("Enter numbers : "))
            numbers.append(num)

    elif ch == 4 or ch == 5:
        a = int(input("Enter first number : "))
        b = int(input("Enter second number : "))

    else:
        print("Invalid choice! Please select 1 to 6.")
        continue

    match ch:
        case 1:
            print("Addition is : ",add(*numbers))

        case 2:
            print("Subraction is : ",sub(*numbers))

        case 3:
            print("Multiplication is : ",mul(*numbers))

        case 4:
            result = div(a,b)
            if result is not None:
                print("Division is:", result)
            

        case 5:
            result = mod(a, b)

            if result is not None:
                print("Modulus is:", result)

        case _:
            print("Invalid choice")
