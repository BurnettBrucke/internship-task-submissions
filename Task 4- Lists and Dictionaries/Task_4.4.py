# Separate even and odd numbers.
num = int(input("Please enter how many numbers you want to entered in list: "))
numbers = []
for i in range(1, num+1):
    val = int(input(f"Enter item {i} : "))
    numbers.append(val)
print("My list : ",numbers)

even = []
odd = []

for number in numbers:
    if number%2 == 0:
        even.append(number)
    if number%2 != 0:
        odd.append(number)

print("Even Number List : ",even)
print("Odd Number List : ",odd)