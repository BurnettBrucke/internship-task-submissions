## Task 4: String Operations
## Create a program that accepts a sentence and performs the following:

## Count the total characters.
## Count the total words.
## Reverse the sentence.
## Check whether the entered word is a palindrome.
## Find the frequency of each word.

# Task 4: String Operations

sentence = input("Enter a sentence: ")

# 1. Count total characters
print("Total characters:", len(sentence))

# 2. Count total words
words = sentence.split()
print("Total words:", len(words))

# 3. Reverse the sentence
print("Reversed sentence:", sentence[::-1])

# 4. Check whether the entered word is a palindrome
word = input("Enter a word to check palindrome: ")

if word == word[::-1]:
    print(word, "is a palindrome.")
else:
    print(word, "is not a palindrome.")

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