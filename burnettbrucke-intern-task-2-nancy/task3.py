# Task 3: List Operations
# Create a list of numbers and perform the following operations:
#  Find the largest number.
#  Find the smallest number.
#  Remove duplicate numbers.
#  Find the sum of all numbers.
#  Find the second-largest distinct number.

lst = [12,5,1,24,26,23,5,1]

#original list
print(f"original list: {lst}")

#largest number
print(f"Largest number: {max(lst)}")

#smallest number
print(f"Smallest number: {min(lst)}")

#remove duplicates number
print(f"After removing duplicates: {list((set(lst)))}")

#sum of all numbers
print(f"Sum of all num: {sum(lst)}")

#second largest
unique = list(set(lst))
second_largest = unique[-2]
print(f"Second largest: {second_largest}")

#By scratch- Find the Largest Number
numbers = [10, 25, 8, 25, 40, 15, 40, 5, 30]

largest = numbers[0]

for num in numbers:
    if num > largest:
        largest = num

print("Largest Number:", largest)

# Find the Smallest Number
numbers = [10, 25, 8, 25, 40, 15, 40, 5, 30]

smallest = numbers[0]

for num in numbers:
    if num < smallest:
        smallest = num

print("Smallest Number:", smallest)

# Remove Duplicate Numbers
numbers = [10, 25, 8, 25, 40, 15, 40, 5, 30]

unique = []

for num in numbers:
    if num not in unique:
        unique.append(num)

print("List without duplicates:", unique)

# Find the Sum of All Numbers
numbers = [10, 25, 8, 25, 40, 15, 40, 5, 30]

total = 0

for num in numbers:
    total += num

print("Sum =", total)

# Find the Second Largest Distinct Number
numbers = [10, 25, 8, 25, 40, 15, 40, 5, 30]

largest = second_largest = float('-inf')

for num in numbers:
    if num > largest:
        second_largest = largest
        largest = num
    elif num > second_largest and num != largest:
        second_largest = num

print("Second Largest Distinct Number:", second_largest)

