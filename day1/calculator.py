'''Task 2: Calculator
Create a calculator that performs:

Addition
Subtraction
Multiplication
Division
Modulus
Handle division by zero properly.'''

print("1.addition")
print("2.subtraction")
print("3.multiplication")
print("4.division")
print("5.modulus")

num1=float(input("enter a number :"))
num2=float(input("enter a second number:"))

choice=int(input("enter your choice (1-5):"))

if choice==1:
    print(f"result = {num1+num2}")
elif choice==2:
    print(f"result = {num1-num2}")
elif choice==3:
    print(f"result = {num1*num2}")
elif choice==4:
    if num2==0:
        print("division by zero not allowed")
    else:
        print(f"result = {num1/num2}")
elif choice==5:
    if num2==0:
        print("modulus by zero not allowed")
    else:
        print(f"result = {num1%num2}")

else:
    print(f"invalid choice")


