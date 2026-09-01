#  Find the first non-repeating character.
text = input("Enter a word : ")
if not text:
    print("You entered an empty string.")
else:
    text = text.lower()
    frequency = {}
    for char in text:
        if char in frequency:
            frequency[char] += 1
        else:
            frequency[char] = 1

    first_non_repeating = None
    for char in text:
        if frequency[char] == 1:
            first_non_repeating = char
            break

    if first_non_repeating is not None:
        print("The first non repeating character is: ",first_non_repeating)
    else:
        print("There is non-repeating character.")
