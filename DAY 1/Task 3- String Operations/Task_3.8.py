# Count the total characters.
word = input("Enter a word : ").lower()
frequency = {}
for ch in word:
    if ch in frequency:
        frequency[ch] +=1
    else:
        frequency[ch] = 1

total_characters = sum(frequency.values())

print("Total Characters : ",total_characters)
 
# print(len(word))