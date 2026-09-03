# Check whether a number is prime

num = int(input("Enter a number to check whether it is prime or not : "))

count = 0

if num<=1:
    print("Not Prime Number")

else:
    for i in range(1,num+1):
        if num%i == 0:
            count += 1

if count == 2:
    print("Prime Number")
else:
    print("Not Prime Number")