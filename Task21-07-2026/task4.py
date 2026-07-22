'''Task 4: String Operations
Create a program that accepts a sentence and performs the following:

Count the total characters.
Count the total words.
Reverse the sentence.
Check whether the entered word is a palindrome.
Find the frequency of each word.'''

sentence=input("Enter the sentence")
print(f"The total characters in a sentence are: {len(sentence)}")
    
words=sentence.split()
print(f"The total words are:{len(words)}")

reverse=sentence[ : :-1]
print(f"The reverse of the sentence are as: {reverse}")

text=input("Enter the word:")
if text==text[ : :-1]:
    print("Palindrome")
else:
    print("Not Palindrome")

#program for frequency of each word 
sentence=input("Enter your sentence")
words=sentence.split()
frequency={}
for word in words:
    if word in frequency:
        frequency[word]+=1
    else:
        frequency[word]=1

print(frequency)
