#  Separate even and odd numbers.

number = [int(x) for x in input("Enter numbers separated by space: ").split()]
if not number:
    print("No numbers entered.")
    exit()

even_numbers = []
odd_numbers = []

for n in number:
    if n % 2 == 0:
        even_numbers.append(n)
    else:
        odd_numbers.append(n)

print("Even numbers:", even_numbers)
print("Odd numbers:", odd_numbers)