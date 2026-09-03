# Count character frequency.
text = input("Enter a sentence : ")
if not text:
    print("You entered an empty string.")
else:
    text = text.lower()
    frequency = {}
    for ch in text:
        if ch in frequency:
            frequency[ch] += 1
        else:
            frequency[ch] = 1

    print("Character Frequency")
    for ch,count in frequency.items():
        print(f"{ch} : {count}")