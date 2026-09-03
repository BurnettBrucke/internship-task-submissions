# Calculate the sum from 1 to n

num = int(input("Enter a number: "))
total = 0
for i in range(1,num+1):
    total += i
print("The sum from 1 to",num,"is :",total)