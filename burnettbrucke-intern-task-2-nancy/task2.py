# Task 2: Calculator
# Create a calculator that performs:
#  Addition
#  Subtraction
#  Multiplication
#  Division
#  Modulus
# Handle division by zero properly.

num1 = float(input("Enter first number : "))
num2 = float(input("Enter second number : "))

print("\n 1.Addition")
print("\n 2.Subtraction")
print("\n 3.Multiplications")
print("\n 4.Division")
print("\n 5.Modulus")

user_choice = input("Enter your choice (1-5): ")

if user_choice=="1":
    print(f"{num1} + {num2} = {num1+num2}")
elif user_choice=="2":
    print(f"{num1} - {num2} = {num1-num2}")
elif user_choice=="3":
    print(f"{num1} * {num2} = {num1*num2}")
elif user_choice=="4":
    if num2==0:
        print("Division by zero is not allowed")
    else:
        print(f"{num1} / {num2} = {num1/num2}")
elif user_choice=="5":
    if num2==0:
        print("Modulus by zero is not allowed.")
    else:
        print(f"{num1} % {num2} = {num1%num2}")
else:
    print("Invalid choice! Please select a number b/w 1 and 5")
 