# Task 4: String Operations
# Create a program that accepts a sentence and performs the following:
#  Count the total characters.
#  Count the total words.
#  Reverse the sentence.
#  Check whether the entered word is a palindrome.
#  Find the frequency of each word.

string = input("Type a sentence = ")
#count total char
total = len(string)
print(f"Total characters = {total}")

# Count the total words.
words = string.split()
print(f"Total words = {len(words)}")

# reverse the sentence
rev_sentence = "".join(words[::-1])
print(f"reverse sentence = {rev_sentence}")

#frequency of each word
frequency = {}
for word in words:
    if word in frequency:
        frequency[word] +=1
    else:
        frequency[word] = 1

print("frequency of words")
for key,value in frequency.items():
    print(key,":",value)


#check word is palindrome
str1=input("enter word: ")
if str1==str1[::-1]:
    print("word is palindrome")
else:
    print("word is not palindrom")


