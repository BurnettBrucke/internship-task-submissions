'''
Task 3: List Operations
Create a list of numbers and perform the following operations:

Find the largest number.
Find the smallest number.
Remove duplicate numbers.
Find the sum of all numbers.
Find the second-largest distinct number.
'''

my_list=[10,10,15,20,25,30,30,40,50]
print(f'original list : {my_list}')
print("\n")
# largest number of list
max=my_list[0]
for i in range(len(my_list)):
    if my_list[i]>max:
        max=my_list[i]
print(f"largest number of the list is :{max}\n")

#  smallest number of list
small=my_list[0]
for  i in range(len(my_list)):
    if my_list[i]<small:
        small=my_list[i]
print(f"smallest number of the list is :{small}\n")

# remove duplicate 
non_duplicate=[]
for i in range(len(my_list)):
    if my_list[i] not in non_duplicate:
        non_duplicate.append(my_list[i])
print(f"non diplicate list : {non_duplicate}\n")

#find sum of all numbers
sum=0
for i in range(len(my_list)):
    sum=sum+my_list[i]

print(f"sum of element of list are : {sum}\n")

#find secand largest distinct number 
distinct=[]
for i in range(len(my_list)):
    if my_list[i] not in distinct:
        distinct.append(my_list[i])
distinct.sort()
print(f"distinct second largest is : {distinct[-2]}")


