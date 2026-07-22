'''Task 2: Calculator
Create a calculator that performs:
Addition
Subtraction
Multiplication
Division
Modulus
Handle division by zero properly.'''

print("Smart Calculator")
while True:
    num1=int(input("Enter your first number"))
    symbol=input("Enter the symbol like +,-,*,/,% :")
    num2=int(input("Enter your second number"))
    if symbol=='+':
        result=num1+num2
        print(f"Addition of two number is:{result}")
    elif symbol=='-':
        result=num1-num2
        print(f"Subtraction of two number is:{result}")
    elif symbol=='*':
        result=num1*num2
        print(f"Multiplication of two number is:{result}")
    elif symbol=='/':
       try:
        result=num1/num2
       except ZeroDivisionError:
        print("Cannot be divided by zero")
    elif symbol=='%':
        result=num1%num2
        print(f"Modulus of two number is:{result}")
    else :
       print("Invalid Symbol")
    choice=input("You want to do the calculation again Yes/No:").lower()
    if choice!='yes':
      print("Have a nice day ")
      break
    
