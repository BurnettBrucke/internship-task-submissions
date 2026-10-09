# Count character frequency

string = input("Enter a string: ")

if not string:
    print("You entered an empty string.")
else:
    string = string.lower()
    frequency = {}
    for char in string:
        if char in frequency:
            frequency[char] += 1
        else:
            frequency[char] = 1

    print("Character frequency:")
    for char, count in frequency.items():
        print(f"'{char}': {count}")