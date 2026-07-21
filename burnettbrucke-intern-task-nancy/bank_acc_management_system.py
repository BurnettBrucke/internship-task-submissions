# base class
class BankAccount:
    def __init__(self, account_number, holder_name, balance=0):
        self.account_number = account_number
        self.holder_name = holder_name
        self.__balance = balance   # private (Encapsulation)

    def deposit(self, amount):
        if amount <= 0:
            raise ValueError("Deposit amount must be greater than zero.")
        self.__balance += amount
        print(f"Deposited {amount}. New balance = {self.__balance}")

    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdraw amount must be greater than zero.")
        if amount > self.__balance:
            raise ValueError("Insufficient balance.")
        self.__balance -= amount
        print(f"Withdrew {amount}. New balance = {self.__balance}")

    def check_balance(self):
        return self.__balance

    def display_details(self):
        print("Account Number :", self.account_number)
        print("Holder Name    :", self.holder_name)
        print("Balance        :", self.__balance)

        
    def _get_balance(self):
        return self.__balance

    def _set_balance(self, new_balance):
        self.__balance = new_balance


#Saving account
class SavingsAccount(BankAccount):
    def __init__(self, account_number, holder_name, balance, interest_rate):
        super().__init__(account_number, holder_name, balance)
        self.interest_rate = interest_rate

    def add_interest(self):
        interest = self._get_balance() * (self.interest_rate / 100)
        self._set_balance(self._get_balance() + interest)
        print(f"Interest of {interest} added. New balance = {self._get_balance()}")

    # Method Overriding: adds interest rate to the printed details
    def display_details(self):
        super().display_details()
        print("Interest Rate  :", self.interest_rate, "%")


#current account
class CurrentAccount(BankAccount):
    def __init__(self, account_number, holder_name, balance, overdraft_limit):
        super().__init__(account_number, holder_name, balance)
        self.overdraft_limit = overdraft_limit

    # Method Overriding: allows balance to go negative up to overdraft_limit
    def withdraw(self, amount):
        if amount <= 0:
            raise ValueError("Withdraw amount must be greater than zero.")
        if amount > self._get_balance() + self.overdraft_limit:
            raise ValueError("Overdraft limit exceeded.")
        self._set_balance(self._get_balance() - amount)
        print(f"Withdrew {amount}. New balance = {self._get_balance()}")

    def display_details(self):
        super().display_details()
        print("Overdraft Limit:", self.overdraft_limit)



accounts = {}  # stores all accounts


def create_savings():
    acc_no = input("Enter account number: ")
    if acc_no in accounts:
        print("Error: Account number already exists.")
        return
    name = input("Enter holder name: ")
    balance = float(input("Enter initial balance: "))
    rate = float(input("Enter interest rate (%): "))
    accounts[acc_no] = SavingsAccount(acc_no, name, balance, rate)
    print("Savings account created successfully.")


def create_current():
    acc_no = input("Enter account number: ")
    if acc_no in accounts:
        print("Error: Account number already exists.")
        return
    name = input("Enter holder name: ")
    balance = float(input("Enter initial balance: "))
    limit = float(input("Enter overdraft limit: "))
    accounts[acc_no] = CurrentAccount(acc_no, name, balance, limit)
    print("Current account created successfully.")


def deposit_money():
    acc_no = input("Enter account number: ")
    if acc_no not in accounts:
        print("Error: Account not found.")
        return
    amount = float(input("Enter deposit amount: "))
    try:
        accounts[acc_no].deposit(amount)
    except ValueError as e:
        print("Error:", e)


def withdraw_money():
    acc_no = input("Enter account number: ")
    if acc_no not in accounts:
        print("Error: Account not found.")
        return
    amount = float(input("Enter withdraw amount: "))
    try:
        accounts[acc_no].withdraw(amount)
    except ValueError as e:
        print("Error:", e)


def check_balance():
    acc_no = input("Enter account number: ")
    if acc_no not in accounts:
        print("Error: Account not found.")
        return
    print("Balance =", accounts[acc_no].check_balance())


def display_details():
    acc_no = input("Enter account number: ")
    if acc_no not in accounts:
        print("Error: Account not found.")
        return
    accounts[acc_no].display_details()


def main():
    while True:
        print("\n----- BANK MANAGEMENT SYSTEM -----")
        print("1. Create Savings Account")
        print("2. Create Current Account")
        print("3. Deposit Money")
        print("4. Withdraw Money")
        print("5. Check Balance")
        print("6. Display Account Details")
        print("7. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            create_savings()
        elif choice == "2":
            create_current()
        elif choice == "3":
            deposit_money()
        elif choice == "4":
            withdraw_money()
        elif choice == "5":
            check_balance()
        elif choice == "6":
            display_details()
        elif choice == "7":
            print("THANK YOU!")
            break
        else:
            print("Invalid choice. Try again.")


if __name__ == "__main__":
    main()