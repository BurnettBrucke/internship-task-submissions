'''Task 1: Basic Python Program
Create a program that takes the following information from the user:

Name
Age
Email
City
Display all information in a properly formatted message.'''


def display_info(Name,Age,Email,City):
    print("-----info-------\n")
    print(f"Name:{Name}")
    print(f"Age:{Age}")
    print(f"Email:{Email}")
    print(f"City:{City}")

Name=input("enter your name :")
Age=int(input('Enter your age:'))
Email=input("enter your email  :")
City=input("enter you city:")

display_info(Name,Age,Email,City)
