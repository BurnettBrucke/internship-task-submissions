# • Find the largest and smallest list numbers
num = int(input("Please enter how many numbers you want to entered in list: "))
numbers = []
for i in range(1, num+1):
    val = int(input(f"Enter item {i} : "))
    numbers.append(val)
print("My list : ",numbers)

smallest = numbers[0]
largest = numbers[0]

for item in numbers:
    if item < smallest:
        smallest = item
    if item > largest:
        largest = item

print("Largest Number = ",largest)
print("Smallest Number = ",smallest)
