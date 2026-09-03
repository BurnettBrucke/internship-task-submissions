# Count frequency of each number.
num = int(input("Please enter how many numbers you want to entered in list: "))
numbers = []
for i in range(1, num+1):
    val = int(input(f"Enter item {i} : "))
    numbers.append(val)
print("My list : ",numbers)

frequency = {}
for item in numbers:
        if item in frequency:
            frequency[item] += 1
        else:
            frequency[item] = 1

print("Character Frequency")
for ch,count in frequency.items():
    print(f"{ch} : {count}")