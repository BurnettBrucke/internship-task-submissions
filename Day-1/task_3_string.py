def reverse_sentence():
    msg = input("Enter a sentence : ")
    reversed_msg = " ".join(reversed(msg.split()))
    print(reversed_msg)


def check_palindrome():
    text = input("Enter the word: ").strip().lower()
    if not text:
        print("Input cannot be empty.")
        return
    i = 0
    j = len(text) - 1

    while i < j:
        if text[i] != text[j]:
            print(f"The word '{text}' is not a palindrome.")
            return

        i += 1
        j -= 1

    print(f"The word '{text}' is a palindrome.")
            
        
def count_vowels_consonants():
    vowels = ("a,e,i,o,u")
    vowels_count = 0
    consonants = 0

    text = ((input("Enter the text : ")).lower()).strip()
    
    for t in text:
        if t.isalpha():
            if t in vowels:
                vowels_count += 1
            elif t not in vowels:
                consonants += 1
    print(f"The text have {vowels_count} vowels and {consonants} consonants.")


def count_words():
    text = (input("Enter the text : " )).split()
    if not text:
        print("Input cannot be empty.")
        return
    print(f"Total words is {len(text)}")

def remove_extra_spaces():
    text = (input("Enter a sentacne")).strip()

    if not text:
        print("Input cannot be empty.")
        return
    cleaned_text = " ".join(text.split())
    print(f"The cleaned text is {cleaned_text}")
    

def character_frequency():
    text = (input("Enter the sentence : "))
    if not text:
        print("Input cannot be empty.")
        return
    frequency = {}

    for char in text.lower():
            if char in frequency:
                frequency[char] += 1
            else:
                frequency[char] = 1

    print("Character frequency:")

    for char, count in frequency.items():
        print(f"{char}: {count}")


def first_non_repeating_character():
    text = input("Enter a string: ").strip().lower()

    if not text:
        print("Input cannot be empty.")
        return

    frequency = {}

    for char in text:
        if char in frequency:
            frequency[char] += 1
        else:
            frequency[char] = 1

    for char in text:
        if frequency[char] == 1:
            print(f"First non-repeating character is: {char}")
            return

    print("There is no non-repeating character.")

def main():
    print("========== Task 3: String Operations ==========")

    print("\n--- Reverse Sentence ---")
    reverse_sentence()

    print("\n--- Palindrome Check ---")
    check_palindrome()

    print("\n--- Vowels and Consonants ---")
    count_vowels_consonants()

    print("\n--- Word Count ---")
    count_words()

    print("\n--- Remove Extra Spaces ---")
    remove_extra_spaces()

    print("\n--- Character Frequency ---")
    character_frequency()

    print("\n--- First Non-Repeating Character ---")
    first_non_repeating_character()
if __name__ == "__main__":
    main()


