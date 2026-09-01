# # 1. Find the largest number in a list
my_list = [43,65,41,52,39,56]
largest_no = my_list[0]
for i in my_list:
    if i > largest_no:
        largest_no = i
print("largest no. is : ", largest_no)


# # 2. Find the smallest number in a list
my_list = [43,65,41,52,39,56,67,26]
smallest_no = my_list[0]
for i in my_list:
    if i < smallest_no:
        smallest_no = i
print(smallest_no)


# # 3. Remove duplicate numbers from a list
my_list = [43,65,41,52,39,56,65,26,52,43,41,39,56]
duplicate_items = []
for i in my_list:
    if i not in duplicate_items:
        duplicate_items.append(i)
print(duplicate_items)


# # 4. Find the Sum of all numbers from a list
my_list = [1,2,3,4,5,6,7,8,9]
sum = 0
for i in my_list:
    sum = sum + i
print(sum)


# 5. Find the second-largest distinct number from a list
my_list = [43,65,41,71,39,56,67,26]
largest = my_list[0]
second_largest = my_list[1]
for i in my_list:
    if i > largest:
        second_largest = largest
        largest = i
    elif second_largest < i:
        second_largest = i
print(second_largest)
