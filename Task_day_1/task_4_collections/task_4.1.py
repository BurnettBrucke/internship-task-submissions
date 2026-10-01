# Find the largest and smallest list values

numbers = [100,20,30,40,50,60,70,80,90]
largest = numbers[0]
smallest = numbers[0]

for n in numbers:
    if n > largest:
        largest = n
    if n < smallest:
        smallest = n

print("Largest value:-", largest)
print("Smallest value:-", smallest)