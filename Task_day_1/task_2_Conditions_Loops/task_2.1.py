# Check positive, negative or zero.


def check_number():
  if number < 0:
    print("Number is Negative.")
  elif number > 0:
    print("Number is Positive.")
  else:
    print("Number is zero.")

number = int(input("Enter a number: "))
check_number()