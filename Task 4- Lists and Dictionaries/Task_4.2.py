# Find the second-largest distinct number without sorting the complete list.
num = int(input("Please enter how many numbers you want to entered in list: "))
numbers = []
for i in range(1, num+1):
    val = int(input(f"Enter item {i} : "))
    numbers.append(val)
print("My list : ",numbers)

largest_number = max(numbers)
numbers.remove(largest_number)

print("Second largest number = ",max(numbers))
