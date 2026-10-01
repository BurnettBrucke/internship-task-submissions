# Find the second-largest distinct number without sorting the complete list

numbers = [3, 1, 4, 4, 5, 2, 5, 3]

largest = numbers[0]
second_largest = numbers[0]

for n in numbers:
    if n > largest:
        second_largest = largest
        largest = n
    elif n > second_largest and n < largest:
        second_largest = n

print("Second largest distinct number:",second_largest)