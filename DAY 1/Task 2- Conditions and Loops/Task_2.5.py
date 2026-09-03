# Calculate the sum from 1 to n.
num = int(input("Enter number to print their sum : "))

total = 0
for i in range(1,num+1):
    total += i

print("Sum : ",total)