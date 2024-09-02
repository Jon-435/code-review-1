import json
import bank

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

def handle_login():
    while True:
        username = input("Enter username: ")
        password = input("Enter password: ")
        result = bank.login(username, password)
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
        password = input("Enter new password: ")

        result = bank.create_account(username, password)
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
        print("5. Logout")
        sub_choice = input("Choose an option: ")

        if sub_choice == '1':
            print(bank.view_balance(username))
        elif sub_choice == '2':
            amount = get_valid_amount("Enter amount to deposit: ")
            print(bank.deposit(username, amount))
        elif sub_choice == '3':
            amount = get_valid_amount("Enter amount to withdraw: ")
            print(bank.withdraw(username, amount))
        elif sub_choice == '4':
            to_user = input("Enter recipient username: ")
            amount = get_valid_amount("Enter amount to transfer: ")
            print(bank.transfer(username, to_user, amount))
        elif sub_choice == '5':
            print(bank.logout(username))
            break
        else:
            print("Invalid option")

def main():
    while True:
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