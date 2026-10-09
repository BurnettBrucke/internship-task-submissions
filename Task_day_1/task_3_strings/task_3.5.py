# Remove extra spaces.

string = input("Enter a string: ")
if not string:
    print("You entered an empty string.")
else:
    string = " ".join(string.split())
    print("String after removing extra spaces:", string)