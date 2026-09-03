# Check positive, negative or zero.
try: 
    num = int(input("Enter a number : "))

except ValueError:
    print("Please enter a valid numeric values.")
else:
    if num < 0:
        print(f"{num} is negative number.")
    elif num > 0:
        print(f"{num} is positive number.")
    else:
        print("Number is zero")
