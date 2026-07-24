# Create a list of numbers and perform the following operations:
#  Find the largest number.
#  Find the smallest number.
#  Remove duplicate numbers.
#  Find the sum of all numbers.
#  Find the second-largest distinct number.

numbers = [10, 25, 15, 40, 25, 10, 50, 40, 30]

largest = max(numbers)
smallest = min(numbers)

unique_numbers = list(set(numbers))
sum_of_numbers = sum(numbers)

second_largest = sorted(set(numbers), reverse=True)[1]

print("Largest number:", largest)
print("Smallest number:", smallest)
print("Unique numbers:", unique_numbers)
print("Sum of all numbers:", sum_of_numbers)
print("Second-largest distinct number:", second_largest)