# Count vowels and consonants.
text = input("Enter a text : ")
vowel = ['a','e','i','o','u']
vowels = 0
consonants = 0

for ch in text.lower():
    if ch in vowel:
        vowels += 1

    else:
        consonants += 1

print("Total Vowels : ",vowels) 
print("Total Consonants : ",consonants)