import mysql.connector



def connect_db():
    return mysql.connector.connect(
        host="localhost",
        user="root",         
        password="7448582747",         
        database="banking_db"
    )


class BankAccount:

    def __init__(self, account_no, name, balance):
        self.account_no = account_no
        self.name = name
        self.balance = balance

    
    @staticmethod
    def create_account():
        db = connect_db()
        cursor = db.cursor()

        acc_no = int(input("Enter Account Number: "))
        name = input("Enter Account Holder Name: ")
        balance = float(input("Enter Initial Deposit Amount: "))

        query = "INSERT INTO accounts (account_no, name, balance) VALUES (%s, %s, %s)"
        cursor.execute(query, (acc_no, name, balance))

        db.commit()
        db.close()
        print(" Account Created Successfully!\n")

    
    @staticmethod
    def get_account(acc_no):
        db = connect_db()
        cursor = db.cursor()

        cursor.execute("SELECT * FROM accounts WHERE account_no=%s", (acc_no,))
        data = cursor.fetchone()

        db.close()

        if data:
            return BankAccount(data[0], data[1], data[2])
        else:
            return None


    def deposit(self, amount):
        self.balance += amount

        db = connect_db()
        cursor = db.cursor()

        cursor.execute("UPDATE accounts SET balance=%s WHERE account_no=%s",
                       (self.balance, self.account_no))

        db.commit()
        db.close()
        print(f" Deposited {amount}. New Balance: {self.balance}\n")

    
    def withdraw(self, amount):
        if amount > self.balance:
            print(" Insufficient Balance!\n")
            return

        self.balance -= amount

        db = connect_db()
        cursor = db.cursor()

        cursor.execute("UPDATE accounts SET balance=%s WHERE account_no=%s",
                       (self.balance, self.account_no))

        db.commit()
        db.close()
        print(f"💸 Withdrawn {amount}. New Balance: {self.balance}\n")

    
    def check_balance(self):
        print(f"🔎 Available Balance: {self.balance}\n")


def main():
    while True:
        print("===== Banking System =====")
        print("1. Create Account")
        print("2. Deposit Money")
        print("3. Withdraw Money")
        print("4. Check Balance")
        print("5. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            BankAccount.create_account()

        elif choice == "2":
            acc_no = int(input("Enter Account Number: "))
            account = BankAccount.get_account(acc_no)
            if account:
                amount = float(input("Enter Amount to Deposit: "))
                account.deposit(amount)
            else:
                print(" Account Not Found!\n")

        elif choice == "3":
            acc_no = int(input("Enter Account Number: "))
            account = BankAccount.get_account(acc_no)
            if account:
                amount = float(input("Enter Amount to Withdraw: "))
                account.withdraw(amount)
            else:
                print(" Account Not Found!\n")

        elif choice == "4":
            acc_no = int(input("Enter Account Number: "))
            account = BankAccount.get_account(acc_no)
            if account:
                account.check_balance()
            else:
                print(" Account Not Found!\n")

        elif choice == "5":
            print("Exiting System...")
            break

        else:
            print("Invalid Choice! Try Again.\n")


if __name__ == "__main__":
    main()
