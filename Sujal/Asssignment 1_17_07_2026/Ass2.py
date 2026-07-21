class BankAccount:
    def __init__(self,Account_no,name):
        self.Account_no=Account_no
        self.name=name
        self.__balance=1000#Encapsulation is done naming a private attribute
    
    def deposit(self,amount):
        if amount>0:
            self.__balance+=amount
        else:
            print("Deposit Amount is less than or zero Cant be Done ")
    
    def withdraw(self,amount):#check for insufficient balance is also made
        if amount<=self.__balance:
            self.__balance-=amount
        else:
            print("Insufficient Balance")
    
    def get_balance(self):
        return self.__balance 
    
    def _update_balance(self,amount):#This is for the updation evertime you cna the balance anywhere
        self.__balance+=amount
    
    def account_details(self):
        return f"""
    The Account No is :{self.Account_no},
    The Name of Account Holder is :{self.name},
    The Balance in Account is :{self.__balance}
    """
    
class SavingsAccount(BankAccount):
    def __init__(self, Account_no,name,interest_rate):
        super().__init__(Account_no, name)#Calling parent Constructor
        self.interest_rate=interest_rate
     
    def interest(self):
        return self.get_balance() * (self.interest_rate/100)
    
    def add_interest(self):
        self._update_balance(self.interest())
    
    def account_details(self):#overrided here with the same name and added a field
        return f"""
    The Account No is :{self.Account_no},
    The Name of Account Holder is :{self.name},
    The Intrest Rate is :{self.interest_rate}%,
    The Intrest Generated is :{self.interest()},
    The Balance in Account is :{self.get_balance()}
    """##was doing a mistake calling private attribute
    
    def __repr__(self):
        return f'({self.Account_no}, "{self.name}", {self.interest_rate},"Saving_Account",{self.get_balance()})'

class CurrentAccount(BankAccount):
    def __init__(self, Account_no, name,overdraft_limit):
        super(). __init__(Account_no,name)# Calling parent Constructor Again
        self.overdraft_limit=overdraft_limit
    
    def withdraw(self, amount):#mc logic internal calculation bhot baad me samjh aai
        available =self.get_balance()+self.overdraft_limit
        
        if amount<=available:
            self._update_balance(-amount)
        else:
            print("Insufficient Balance")

    def __repr__(self):
        return f'({self.Account_no}, "{self.name}", {self.overdraft_limit},"Current_Account",{self.get_balance()})'

print("Program Starting the main Body")

customers={}#Initializing a Python Dictionary



while True:
    if not len(customers)==0:
        print(customers)
                
    choice=int(input(f"""
1.Create Savings Account
2.Create Current Account
3.Deposit Money
4.Withdraw Money
5.Check Balance
6.Display Account Details
7.Exit

Enter Your Choice
"""))
    
    match choice:
        case 1:
            print("Creating Savings Account")
            try:
                account_no=int(input("Enter the Account Number:"))
            except ValueError:
                print("Please Enter Interger Value")
                
            name=input("Enter the name:")
            interest_rate=int(input("Enter the interest rate:"))
            if account_no not in customers:
                customers[account_no]=SavingsAccount(account_no,name,interest_rate)#This will make account_no as key and create a object of savings account
            else:
                print("Account Already Exists")
        case 2:
            print("Creating Current Account")
            try:
                account_no=int(input("Enter the Account Number:"))
            except ValueError:
                print("Please Enter Interger Value")
            name=input("Enter the name:")
            #i will be keeping the overdraftr limit as 2000 same for all as this is my bank
            customers[account_no]=CurrentAccount(account_no,name,2000)#This will make account_no as key and create a object of current account
            
        case 3:
            print("Deposit Money")
            try:
                account_no=int(input("Enter the Account Number:"))
            except ValueError:
                print("Please Enter Interger Value")
            if account_no in customers:
                amount=float(input("Enter the deposit Amount:"))
                customers[account_no].deposit(amount)#  customers[account_no]=BankAccount.deposit()
            else:
                print("Account Not Found")
           
        case 4:
            print("Withdraw Money")
            try:
                account_no=int(input("Enter the Account Number:"))
            except ValueError:
                print("Please Enter Interger Value")
            if account_no in customers:
                amount=float(input("Enter the withdraw Amount:"))
                customers[account_no].withdraw(amount)
            else:
                print("Account Not Found")
        case 5:
            print("check Balance")
            try:
                account_no=int(input("Enter the Account Number:"))
            except ValueError:
                print("Please Enter Interger Value")
            if account_no in customers:
                print(customers[account_no].get_balance())
            else:
                print("Account Not Found")
        case 6:
            print("Account Details")
            try:
                account_no=int(input("Enter the Account Number:"))
            except ValueError:
                print("Please Enter Interger Value")
            if account_no in customers:
                print(customers[account_no].account_details())
            else:
                print("Account Not Found")
        case 7:
            break
        case _:
            print("Invalid input")       