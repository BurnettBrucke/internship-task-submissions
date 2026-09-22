# Check whether a word is a palindrome

word = input("Enter a word: ")
if not word:
    print("You entered an empty string.")
else :
    word = word.lower()
    reversed_word = word[::-1]
    if word == reversed_word:
      print("The word is a palindrome.")
    else:
     print("The word is not a palindrome.")