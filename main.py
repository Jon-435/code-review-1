import os
import getpass
from auth import login, logout
from umanager import create_account, add_account
import bank

def clear():
    os.system('cls')

def get_valid_amount(prompt):
    while True:
        try:
            amount = float(input(prompt))
            if amount <= 0:
                print("Amount must be positive")
            else:
                return amount
        except ValueError:
            print("Invalid input; amount must be numeric")

def get_valid_account(prompt):
    while True:
        try:
            account_number = int(input(prompt))
            return account_number
        except ValueError:
            print("Invalid input; account must be numeric")

def handle_login():
    while True:
        username = input("Enter username: ")
        password = getpass.getpass("Enter password: ")
        result = login(username, password)
        print(result)

        if "Login successful" in result:
            return username
        elif "Account is locked" in result:
            return None
        else:
            print("Please try again")

def handle_create_account():
    while True:
        username = input("Enter new username: ")
        password = getpass.getpass("Enter new password: ")

        result = create_account(username, password)
        print(result)

        if "successfully created" in result:
            return

def handle_bank(username):
    if username is None:
        return

    while True:
        print("\n1. View Balance")
        print("2. Deposit")
        print("3. Withdraw")
        print("4. Transfer")
        print("5. Member to Member")
        print("6. Add New Account")
        print("7. Logout")
        sub_choice = input("Choose an option: ")

        if sub_choice == '1':
            response = bank.view_balance(username)
        elif sub_choice == '2':
            amount = get_valid_amount("Enter amount to deposit: ")
            account_number = get_valid_account("Enter account number: ")
            response = bank.deposit(username, account_number, amount)
        elif sub_choice == '3':
            amount = get_valid_amount("Enter amount to withdraw: ")
            account_number = get_valid_account("Enter account number: ")
            response = bank.withdraw(username, account_number, amount)
        elif sub_choice == '4':
            from_account = get_valid_account("Enter source account number: ")
            to_account = get_valid_account("Enter destination account number: ")
            amount = get_valid_amount("Enter amount to transfer: ")
            response = bank.transfer(username, from_account, to_account, amount)
        elif sub_choice == '5':
            from_account = get_valid_account("Enter source account number: ")
            to_user = input("Enter recipient username: ")
            amount = get_valid_amount("Enter amount to transfer: ")
            response = bank.member_transfer(username, from_account, to_user, amount)
        elif sub_choice == '6':
            account_number = get_valid_account("Enter new account number: ")
            response = add_account(username, account_number)
        elif sub_choice == '7':
            response = logout(username)
            break
        else:
            response = "Invalid option"

        clear()
        print(response)
        # input("Press Enter to continue...")

def main():
    while True:
        clear()
        print("\nWelcome to Bucky's Banking")
        print("1. Login")
        print("2. Create Account")
        print("3. Exit")
        choice = input("Choose an option: ")

        if choice == '1':
            username = handle_login()
            if username:
                handle_bank(username)
        elif choice == '2':
            handle_create_account()
        elif choice == '3':
            break
        else:
            print("Invalid option")

if __name__ == "__main__":
    main()