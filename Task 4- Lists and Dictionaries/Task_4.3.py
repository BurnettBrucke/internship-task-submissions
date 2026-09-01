# Remove duplicates while preserving order
num = int(input("Please enter how many numbers you want to entered in list: "))
numbers = []
for i in range(1, num+1):
    val = int(input(f"Enter item {i} : "))
    numbers.append(val)
print("My list : ",numbers)

result = []

for i in numbers:
    if i not in result:
        result.append(i)

print("Distinct List : ",result)