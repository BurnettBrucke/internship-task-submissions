## Task 2: Calculator
## Create a calculator that performs:
## Addition,Subtraction,Multiplication,Division,Modulus
## Handle division by zero properly

num1 = int(input(" enter first number"))
num2 = int(input(" enter second number"))

operation = input("enter which mathematical operation want to perform")

if(operation == '+'):
    add = num1+num2
    print(f"Addition of {num1} and {num2} is {add}")

elif(operation == "-"):
    sub = num1-num2
    print(f"Subtraction of {num1} and {num2} is {sub}") 

elif(operation == "*"):
    mul = num1*num2
    print(f"Multiplication of {num1} and {num2} is {mul}")

elif(operation == "/"):
    try:
       div = num1/num2

    except ZeroDivisionError:
        print("cannot divide by zero")
    else:
        print(f"Division of {num1} and {num2} is {div}")

elif(operation == "%"):
    try:
       mod = num1%num2

    except ZeroDivisionError:
        print("cannot divide by zero")
    else:
        print(f"Division of {num1} and {num2} is {mod}")