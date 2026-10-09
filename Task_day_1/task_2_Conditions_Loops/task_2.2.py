# Check even or odd.
 
def check_even_odd():
  if number % 2 == 0:     
     print(f"{number} is an even number.")
  else :
    print(f"{number} is an odd number.")

number = int(input("Enter a number: "))
check_even_odd()