## Task 3: List Operations
## Create a list of numbers and perform the following operations:
## Find the largest number.
## Find the smallest number.
## Remove duplicate numbers.
## Find the sum of all numbers.
## Find the second-largest distinct number.


n = int(input("enter length of list"))
list_int = [] 
for i in range(n):
    num = int(input("enter numbers"))
    list_int.append(num)

maxi1 = list_int[0]
maxi2 = list_int[0]
mini = list_int[0]
i =0
while(i< n):
    if(list_int[i] > maxi1):
        maxi1 = list_int[i]

    if(list_int[i] < mini):
        mini = list_int[i]
    i = i+1


print(f"largest numbers is {maxi1} fron the list")
print(f"largest numbers is {mini} fron the list")
i = 0
while(i < n):
    if(list_int[i] != maxi1 and list_int[i] >maxi2):
        maxi2 = list_int[i]
    i = i+1

print(f"Second highest value is {maxi2}")

i = 0
sum =0
while(i <n):
    sum = sum+list_int[i]
    i = i+1

print(f"sum of all elements is {sum}")




