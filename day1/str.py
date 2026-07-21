'''Task 4: String Operations
Create a program that accepts a sentence and performs the following:

Count the total characters.
Count the total words.
Reverse the sentence.
Check whether the entered word is a palindrome.
Find the frequency of each word.'''

sentance=input("enter your sentance :")

# count total charcters
x=len(sentance.replace(" ",""))
print("toatl cahracters are:",x)

# count total no of word
word=sentance.split()
print(f"toatl words are :{len(word)}")

# reverse a sentance 
reversed=sentance[::-1]
print(f"reversed: {reversed}")

# chech palindrom 
if sentance==reversed:
    print("palindrom")
else:
    print("not palindrom")

# frequency of each word
words=sentance.split()
freq={}
for word in words:
    if word in freq:
        freq[word]+=1
    else:
        freq[word]=1

print(F"frequancy of words : {freq}")