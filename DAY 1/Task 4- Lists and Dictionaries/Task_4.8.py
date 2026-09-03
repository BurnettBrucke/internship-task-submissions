# Find the sum of all numbers.
num = int(input("Please enter how many numbers you want to entered in list: "))
numbers = []
for i in range(1, num+1):
    val = int(input(f"Enter item {i} : "))
    numbers.append(val)
print("My list : ",numbers)

total = 0
for num in numbers:
    total += num
print("Sum of all numbers : ",total)