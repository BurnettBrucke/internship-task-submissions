'''Task 3: List Operations
Create a list of numbers and perform the following operations:

Find the largest number.
Find the smallest number.
Remove duplicate numbers.
Find the sum of all numbers.
Find the second-largest distinct number.'''

number=[1,2,3,4,5,6,6]
print("The number of list are as:",number)
print("Largest Number",max(number))
print("Smallest Number", min(number))

duplicate=list(set(number))
print("After Removing Duplicates",duplicate)
print("Sum of all number is:",sum(number))

second_largest=duplicate[-2]
print("The second largest distinct number is :",second_largest)
