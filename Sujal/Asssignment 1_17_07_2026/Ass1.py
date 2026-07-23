customers={}
class BankAccount:
    def user(self):
        name=input("Enter the name od the account holder")
        try:
            account_no=int(input("Enter the account number:"))
        except ValueError:
            print("Enter the int value")
            return
        if account_no in customers:
            print("Account already exists")
            return
        self.__balance=1000
        return name,account_no,self.__balance
        
    def deposit(self,customers):
        try:
            account_no=int(input("Enter the account number:"))
        except ValueError:
            print("Enter the int value")
            return
        if account_no not in customers:
            print("Account doesnt Exist")
        else:
            amount=float(input("Enter the amount"))
            if amount <= 0:
                print("Invalid amount")
                return
            customers[account_no][2]+=amount
    
    def withdraw(self,customers):
        try:
            account_no=int(input("Enter the account number:"))
        except ValueError:
            print("Enter the int value")
            return
        if account_no not in customers:
            print("Account doesnt Exist")
        else:
            amount=float(input("Enter the amount"))
            if amount <= 0:
                print("Invalid amount")
                return
            customer_balance=customers[account_no][2]
            if customers[account_no][1] == "Saving":
                if amount>customer_balance:
                    print("Insufficient Balance")
                else:
                    customers[account_no][2]-=amount
            else:
                overdraft = customers[account_no][3]
                if amount>customer_balance:
                    if amount<=customer_balance+overdraft:
                        customers[account_no][2]-=amount
                    else:
                        print("Insifficient Balance")
                else:
                    customers[account_no][2]-=amount    
                    
    def get_balance(self,customers):
        try:
            account_no=int(input("Enter the account number:"))
        except ValueError:
            print("Enter the int value")
            return
        
        if account_no not in customers:
            print("Account doesnt Exist")
        else:        
            return customers[account_no][2]       
    
    def account_details(self,customers):
        try:
            account_no=int(input("Enter the account number:"))
        except ValueError:
            print("Enter the int value")
            return
        if account_no not in customers:
            print("Account doesnt Exist")
        else:
            print(customers[account_no])


class SavingAccount(BankAccount):
    def __init__(self):
        interest_rate=int(input("Enter the Interest Rate:"))
        account_type="Saving"
        name,account_no,balance=self.user()
        customers[account_no]=[name,account_type,balance,interest_rate]

class CurrentAccount(BankAccount):
    def __init__(self):
        overdraft_limit=int(input("Enter the OverDraftLimit:"))
        account_type="Current"
        name,account_no,balance=self.user()
        customers[account_no]=[name,account_type,balance,overdraft_limit]        

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
            SavingAccount()            
        case 2:
            print("Creating Current Account")
            CurrentAccount()          
        case 3:
            print("Deposit Money")
            b=BankAccount()
            b.deposit(customers)           
        case 4:
            print("Withdraw Money")
            b=BankAccount()
            b.withdraw(customers)    
        case 5:
            print("check Balance")
            b=BankAccount()
            print("Balance:", b.get_balance(customers))   
            
        case 6:
            print("Account Details")
            b=BankAccount()
            b.account_details(customers)    
            
        case 7:
            break
        case _:
            print("Invalid input")       