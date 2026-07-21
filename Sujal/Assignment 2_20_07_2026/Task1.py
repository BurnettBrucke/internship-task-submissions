def Info():
    name=input("Enter the name of the User: ")
    age=int(input("Enter your age: "))
    email=input("Enter your Email: ")
    city=input("Enter yiur City: ")

    print(f"""
Name:{name},
Age:{age},
Email:{email},
city:{city}
          """)

Info()