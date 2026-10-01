# Count frequency of each number

numbers = [3, 1, 4, 4, 5, 2, 5, 3]

if not numbers:
    print("list cannot be empty.")
    exit()

frequency = {}
for n in numbers:
    if n in frequency:
        frequency[n] += 1
    else:
        frequency[n] = 1
for n, count in frequency.items():
    print(f"{n} : {count}")