# Find common values between two lists
list_1 = [1,3,4,6,2,1,3]
list_2 = [2,4,3,5,2,4,5,1]

list_1 = set(list_1)
list_2 = set(list_2)

print("Common Values in both the list : ",list(list_1.intersection(list_2)))
print("Common Values in both the list : ",list(list_1 & list_2))