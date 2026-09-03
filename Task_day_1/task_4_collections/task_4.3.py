# Remove duplicates while preserving order.

numbers=[3,1,4,4,5,2,5,3]

unique_numbers = []

for n in numbers:
    if n not in unique_numbers:
        unique_numbers.append(n)

print("List after removing duplicates:", unique_numbers)