# Find the first non-repeating character

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
            
    first_non_repeating = None
    for char in string:
        if frequency[char] == 1:
            first_non_repeating = char
            break

    if first_non_repeating is not None:
        print("The first non-repeating character is:", first_non_repeating)
    else:
        print("There is no non-repeating character.")