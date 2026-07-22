class BankAccount:

    def __init__(self, account_no, holder_name, balance):
        self.account_no = account_no
        self.holder_name = holder_name
        self.__balance = balance      # Private Variable

    def deposit(self, amount):
        if amount <= 0:
            print("Invalid Deposit Amount")
            return

        self.__balance += amount
        print("Money Deposited Successfully")

    def withdraw(self, amount):
        if amount > self.__balance:
            print("Insufficient Balance")
        else:
            self.__balance -= amount
            print("Money Withdrawn Successfully")

    def check_balance(self):
        print("Current Balance:", self.__balance)

    def display_details(self):
        print("\n----- Account Details -----")
        print("Account Number :", self.account_no)
        print("Holder Name    :", self.holder_name)
        print("Balance        :", self.__balance)


class SavingsAccount(BankAccount):

    def __init__(self, account_no, holder_name, balance, interest_rate):
        super().__init__(account_no, holder_name, balance)
        self.interest_rate = interest_rate

    def add_interest(self):

        interest = self._BankAccount__balance * self.interest_rate / 100
        self._BankAccount__balance += interest
        print("Interest Added Successfully")

    def display_details(self):
        super().display_details()
        print("Interest Rate :", self.interest_rate, "%")

class CurrentAccount(BankAccount):

    def __init__(self, account_no, holder_name, balance, overdraft_limit):
        super().__init__(account_no, holder_name, balance)
        self.overdraft_limit = overdraft_limit

    def withdraw(self, amount):
        if amount <= self._BankAccount__balance + self.overdraft_limit:
            self._BankAccount__balance -= amount
            print("Money Withdrawn Successfully")
        else:
            print("Overdraft Limit Exceeded")

    def display_details(self):
        super().display_details()
        print("Overdraft Limit :", self.overdraft_limit)

accounts = {}
while True:

    print("\n===== Bank Management System =====")
    print("1. Create Savings Account")
    print("2. Create Current Account")
    print("3. Deposit Money")
    print("4. Withdraw Money")
    print("5. Check Balance")
    print("6. Display Account Details")
    print("7. Exit")

    choice = input("Enter Choice: ")
    try:
        if choice == "1":
            acc = input("Enter Account Number: ")
            if acc in accounts:
                print("Duplicate Account Number")
                continue

            name = input("Enter Holder Name: ")
            balance = float(input("Enter Balance: "))
            interest = float(input("Enter Interest Rate: "))

            accounts[acc] = SavingsAccount(acc, name, balance, interest)

            print("Savings Account Created Successfully")

        elif choice == "2":

            acc = input("Enter Account Number: ")

            if acc in accounts:
                print("Duplicate Account Number")
                continue

            name = input("Enter Holder Name: ")
            balance = float(input("Enter Balance: "))
            overdraft = float(input("Enter Overdraft Limit: "))

            accounts[acc] = CurrentAccount(acc, name, balance, overdraft)

            print("Current Account Created Successfully")

        elif choice == "3":

            acc = input("Enter Account Number: ")

            if acc not in accounts:
                print("Invalid Account Number")
                continue

            amount = float(input("Enter Deposit Amount: "))
            accounts[acc].deposit(amount)

        elif choice == "4":

            acc = input("Enter Account Number: ")

            if acc not in accounts:
                print("Invalid Account Number")
                continue

            amount = float(input("Enter Withdraw Amount: "))
            accounts[acc].withdraw(amount)

        elif choice == "5":

            acc = input("Enter Account Number: ")

            if acc not in accounts:
                print("Invalid Account Number")
                continue

            accounts[acc].check_balance()

        elif choice == "6":

            acc = input("Enter Account Number: ")

            if acc not in accounts:
                print("Invalid Account Number")
                continue

            accounts[acc].display_details()

        elif choice == "7":

            print("Thank You")
            break

        else:
            print("Invalid Menu Choice")

    except ValueError:
        print("Please Enter Valid Input")