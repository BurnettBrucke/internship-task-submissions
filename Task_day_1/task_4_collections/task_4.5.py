# Find common values between two lists.

list1 = [1,3,4,7,8]
list2 = [1,2,3,4,5]

if not list1 or not list2:
    print("lists cannot be empty.")
    exit()

common_values=[]
for n in list1:
    if n in list2 and n not in common_values:
        common_values.append(n)

print("common values:",common_values)