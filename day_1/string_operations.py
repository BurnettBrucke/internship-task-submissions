# Create a program that accepts a sentence and performs the following:
# # 1. Count the total characters.
# my_str = input("Enter a sentence : ")
# count = 0
# str = ''
# for i in my_str:
#     if i not in str:
#         if i == ' ':
#             continue
#         count = count + 1
# print(count)
# ---------------------------------------------------------------------------------

# # 2. Count the total words.
# my_str = "Hello guys my name is rahul singh bod gurjar"
# word_count = 0
# for word in my_str.split():
#     word_count = word_count + 1

# print("Total words are : ", word_count)
# ---------------------------------------------------------------------------------

# # 3. Reverse the sentence.
# # (1) using .join(reversed)
# my_str = input("Enter a sentence : ")
# for i in my_str:
#     reverse = ''.join(reversed(my_str))
# print(reverse)


# # (2) using [::-1]
# my_str = input("Enter a sentence : ")
# reverse = my_str[::-1]
# print(reverse)
# -----------------------------------------------------------------------------------

# # 4. Check whether the entered word is a palindrome.
# my_str = input("Enter a word to check : ")

# reverse = ''.join(reversed(my_str))
# if reverse == my_str:
#     print("Yes, It is a palindrome")
# else:
#     print("No, It is not a palindrome")
# -----------------------------------------------------------------------------------

# # 5. Find the frequency of each word.

# from collections import Counter
# my_str = 'apple banana apple cherry banana apple'

# # split the string into a list of words
# words = my_str.split()

# word_counts = Counter(words)
# print(word_counts)

my_str = 'apple banana apple cherry banana apple'
word_counts = {}
for word in my_str.split():
    word_counts[word] = word_counts.get(word, 0) + 1
print(word_counts)


