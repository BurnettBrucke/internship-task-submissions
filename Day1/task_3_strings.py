def reversing_sentence():
    stringstr = input("Enter the sentence you want to reverse: ")
    str = list(stringstr)

    start = 0
    end = len(str) - 1
    while start < end:
        str[start], str[end] = str[end], str[start]
        start = start + 1
        end = end - 1
    print(str)


# reversing_sentence()


def count_vowel_consonants():
    str = input("Enter the word: ")
    str = str.lower()
    length = len(str)
    vowel = 0

    for char in str:
        if char == "a" or char == "e" or char == "i" or char == "o" or char == "u":
            vowel = vowel + 1

    print(f"The total number of vowels are {vowel} and consonants are {length-vowel}")


# count_vowel_consonants()


def count_words():
    sentence = input("Enter the sentence: ")
    count = 0
    for ch in sentence:
        if ch == " ":
            pass
        else:
            count = count + 1

    print(f"Total number of words in {sentence} are {count}")


# count_words()


def count_frequency():
    text = input("Enter the text: ")
    frequency = {}
    for char in text:
        frequency[char] = frequency.get(char, 0) + 1

    return print(frequency)


# count_frequency()


def first_non_repeating():
    text = input("Enter the text: ")
    frequency = {}
    for char in text:
        frequency[char] = frequency.get(char, 0) + 1

    for char in text:
        if frequency[char] == 1:
            print(char)


first_non_repeating()
