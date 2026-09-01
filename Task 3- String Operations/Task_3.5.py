# Remove extra spaces.

text = input("Enter a sentence : ")
if not text:
    print("You entered an empty string")
else:
    text = " ".join(text.split())
    print("Remove extra space : ",text)