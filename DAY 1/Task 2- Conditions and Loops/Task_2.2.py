# Check even or odd.
try: 
    num = int(input("Enter a number : "))

except ValueError:
    print("Please enter a valid numeric values.")
else:
    if num % 2 == 0:
        print(f"{num} is an even number.")
    else:
        print(f"{num} is an odd number.")
finally:
    print("Program Ended.")
