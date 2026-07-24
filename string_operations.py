
sentence = input("Enter a sentence: ")

# 1. Count the total characters
print("Total Characters:", len(sentence))

# 2. Count the total words
words = sentence.split()
print("Total Words:", len(words))

# 3. Reverse the sentence
reverse_sentence = sentence[::-1]
print("Reversed Sentence:", reverse_sentence)

# 4. Check whether the entered word is a palindrome
word = input("Enter a word to check palindrome: ")

if word == word[::-1]:
    print(word, "is a Palindrome.")
else:
    print(word, "is not a Palindrome.")

# 5. Find the frequency of each word
frequency = {}

for w in words:
    if w in frequency:
        frequency[w] += 1
    else:
        frequency[w] = 1

print("\nWord Frequencies:")
for key, value in frequency.items():
    print(key, ":", value)