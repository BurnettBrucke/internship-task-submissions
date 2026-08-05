
def add(num1, num2):
    return (num1 + num2)

def subtract(num1, num2):
    return (num1 - num2)

def multiply(num1, num2):
    return (num1 * num2)

def division(num1, num2):
    return (num1 / num2)

def modulus(num1, num2):
    return (num1 % num2)

user_input = input('''    
    Enter 1 for addition
    Enter 2 for subtraction
    Enter 3 for multiplication
    Enter 4 for division
    Enter 5 to find modulus of two numbers '''
)

number1 = float(input("Enter first number : "))
number2 = float(input("Enter second number : "))

if user_input == '1':
    print(f"The Sum of two numbers is {add(number1, number2)}")

elif user_input == '2':
    print(f"The Subtraction of two numbers is {subtract(number1, number2)}")

elif user_input == '3':
    print(f"The Multiplication of two numbers is {multiply(number1, number2)}")

elif user_input == '4':
    print(f"The Division of two numbers is {division(number1, number2)}")

elif user_input == '5':
    print(f"The Modulus of two numbers is {modulus(number1, number2)}")

else:
    print("Invalid Selection, please try again !")