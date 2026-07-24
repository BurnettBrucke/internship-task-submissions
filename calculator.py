num1 = float(input("Enter first number: "))
num2 = float(input("Enter second number: "))

print("\n Select Operation")
print("1. Addition")
print("2. Subtraction")
print("3. Multiplication")
print("4. Division")
print("5. Modulus")

choice = input("Enter your choice (1-5): ")

if choice == "1":
    print("Result =", num1 + num2)

elif choice == "2":
    print("Result =", num1 - num2)

elif choice == "3":
    print("Result =", num1 * num2)

elif choice == "4":
    if num2 == 0:
        print("Error! Division by zero is not allowed.")
    else:
        print("Result =", num1 / num2)

elif choice == "5":
    if num2 == 0:
        print("Error! Modulus by zero is not allowed.")
    else:
        print("Result =", num1 % num2)

else:
    print("Invalid Choice!")