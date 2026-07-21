

# bank management system 
class BankAccount:

    def __init__(self,account_no,holder_name,balance):
        self.account_no = account_no
        self.holder_name=holder_name
        self.__balance=balance

    def show(self):
        print(self.account_no,self.holder_name)

    def deposit(self,amount):
        if amount <=0:
            raise ValueError("deposit amount is less than zero")
        
        self.__balance = self.__balance+amount

        print("Amount deposite successfully")


    def withdraw(self,amount):
        if amount<=0:
            raise ValueError("amount must be greater than zero")
        
        if amount>self.__balance:
            raise ValueError("insufficient balance")
        
        self.__balance=self.__balance-amount
        print("withdraw succesfully")

    # helper method
    def _deduct_balance(self,amount):
        self.__balance=self.__balance-amount


    def get_balance(self):
        return self.__balance
    
    def display_details(self):
        print("Account details are :\n")
        print(f"Account number : {self.account_no}")
        print(f"Account Holder Name : {self.holder_name}")
        print(f"balance : {self.__balance}")

# acc1=BankAccount(101,"vikas",400)
# acc1.show()
# acc1.deposite(100)
# acc1.withdrow(300)
# acc1.display_details()


class SavingAccount(BankAccount):
    def __init__(self,account_no,holder_name,balance,interest_rate):
        super().__init__(account_no,holder_name,balance)
        self.interest_rate=interest_rate

    def add_interest(self):
        interest=self.get_balance()*self.interest_rate/100
        self.deposit(interest)
        print(f"{interest} amount interest is added ")

    def display_details(self):
        super().display_details()
        print(f"Interest Rate : {self.interest_rate} %")

# acc2=SavingAccount(102,"kamal",1000,2.5)
# acc2.add_interest()
# acc2.display_details()

class CurrentAccount(BankAccount):
    def __init__(self,account_no,holder_name,balance,over_draft_limit):
        super().__init__(account_no,holder_name,balance)
        self.over_draft_limit=over_draft_limit

    def withdraw(self, amount):
        if amount<=0:
            raise ValueError("amount must be greater than zero")
        
        available=self.get_balance()+self.over_draft_limit

        if amount>available:
            raise ValueError("overdraft limit exceed")
        

        self._deduct_balance(amount)
        print(f"{amount} is withdrow successfully.")

    def display_details(self):
        super().display_details()
        print(f"overdraft limit : {self.over_draft_limit}")
        print(f"Account type : current ")

# acc3=CurrentAccount(103,"govind",1000,500)
# acc3.withdrow(1200)
# acc3.display_details()


# menu
accounts={}

def find_account():
    account_no=int(input("enter a acount no:"))

    if account_no  not in accounts:
        raise ValueError("invalid account no")
    
    return accounts[account_no]

while True:

    print("\n========== BANK MENU ==========")
    print("1. Create Savings Account")
    print("2. Create Current Account")
    print("3. Deposit Money")
    print("4. Withdraw Money")
    print("5. Check Balance")
    print("6. Display Account Details")
    print("7. Add Interest")
    print("8. Exit")

    try:
        choice = int(input("\n Enter your choice : "))

        if choice == 1:
            account_no=int(input("enter a account no:"))

            if account_no in accounts:
                raise ValueError("account already present")
            
            holder=input("enter holder name: ")
            balance=float(input("initial balance:"))
            interest=float(input("enter intrest rate (in %) :"))

            accounts[account_no]=SavingAccount(account_no,
                                               holder,
                                               balance,
                                               interest)
            print("\n saving account is created ")

        elif choice==2:
            account_no=int(input("enter a account no : "))
            if account_no in accounts:
                raise ValueError("account already present")
            
            holder=input("enter holder name: ")
            balance=float(input("enter initail balance: "))
            over_draft_limit=float(input("enter over draft limit :"))

            accounts[account_no]=CurrentAccount(account_no,
                                                holder,
                                                balance,
                                                over_draft_limit)
            
            print("\n current account created succesfully")

        elif choice==3:
            account=find_account()
            amount=float(input("enter a deposite ammount: "))
            account.deposit(amount)
            
        elif choice==4:
            account=find_account()
            amount=float(input("enter a withdraw ammount:"))
            account.withdaw(amount)

        elif choice==5:
            account=find_account()
            print(f"current balance is {account.get_balance()}")

        elif choice==6:
            account=find_account()
            account.display_details() 

        elif choice==7:
            account=find_account()
            if isinstance(account,SavingAccount):
                account.add_interest()
            else:
                print("can only add to saving account")

        elif choice==8:
            break

        else:
            print("invalid choice")

    except ValueError as e:
        print("error" ,e)
    except Exception as e:
        print("unexpected error ",e)
    


