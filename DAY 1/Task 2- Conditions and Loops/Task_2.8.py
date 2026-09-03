# Calculating the factorial of a number.
num = int(input("Enter a number: "))
fact = 1
for i in range(num,1,-1):
    fact *= i

print("Factorial of a given number is: ",fact)