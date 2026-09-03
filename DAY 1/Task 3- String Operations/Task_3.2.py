# Check whether a word is a palindrome.
word = input("Enter a word : ").lower()

if word == word[::-1]:
    print("Pallindrome")
else:
    print("Not Pallindrome")