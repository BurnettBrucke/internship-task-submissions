# Build a calculator for addition, subtraction, multiplication, division and modulus.

num1 = int(input("Enter the first number: "))
num2 = int(input("Enter the second number: "))

operation = input("Enter the operation (+, -, *, /, %): ")

match operation:
    case "+":
        result = num1 +num2
        print("The result of addition is:", result)
    case "-": 
        result = num1 - num2
        print("The result of subtraction is:", result)   
    case "*":
        result = num1 * num2
        print("The result of multiplication is:", result)
    case "/":
        if num2 != 0:
            result = num1 / num2
            print("The result of division is:", result)
        else:
            print("Error: Division by zero is not allowed.")
    case "%":
         if num2 != 0:
            print("Result:", num1 % num2)
         else:
             print("Error: Modulus by zero is not allowed.")

    