import os
import sys
import json
import time

TRANSFER_LIMIT = 5000.00
USER_DB = "users.json"

# Update to accommodate for POSIX-compliant systems like Linux, BSD, and MacOS
def clear():
    os.system('clear')

def security_checks(username, users):
    user = find_user(username, users)
    if not user:
        return False, "User not found"
    
    if is_account_locked(user):
        return False, "Account is locked due to multiple failed login attempts"

    if is_session_timed_out(user['last_activity']):
        return False, "Session timed out"
    
    return True, user

def login(username, password):
    users = load_users()
    valid, result = security_checks(username, users)
    if not valid:
        return result
    
    user = result 

    if password == user['password']:
        user['incorrect_attempts'] = 0
        update_last_activity(user)
        save_users(users)
        return "Login successful"
    else:
        user['incorrect_attempts'] += 1
        if user['incorrect_attempts'] >= 5:
            user['locked'] = True
        save_users(users)
        return "Incorrect password"

def logout(username):
    users = load_users()
    valid, result = security_checks(username, users)
    if not valid:
        return result
    
    user = result 
    update_last_activity(user)
    save_users(users)
    return "Logged out successfully"

def view_balance(username):
    users = load_users()
    valid, result = security_checks(username, users)
    if not valid:
        return result
    
    user = result

    balance_info = []
    for account in user.get('accounts', []):
        balance_info.append(f"Account {account['account_number']}: ${account['balance']:.2f}")

    if balance_info:
        return "\n".join(balance_info)
    else:
        return "No accounts found for this user"

def deposit(username, account_number, amount):
    users = load_users()
    valid, result = security_checks(username, users)
    if not valid:
        return result
    
    user = result
    accounts = user.get('accounts', [])
    account = find_account(accounts, account_number)

    if account is None:
        return "Account not found"
    
    account['balance'] += amount
    update_last_activity(user)
    save_users(users)
    return f"Successfully deposited ${amount:.2f} into account {account_number}"

def withdraw(username, account_number, amount):
    users = load_users()
    valid, result = security_checks(username, users)
    if not valid:
        return result
    
    user = result
    accounts = user.get('accounts', [])
    account = find_account(accounts, account_number)

    if account is None:
        return "Account not found"

    if account['balance'] < amount:
        return "Insufficient funds"
    
    account['balance'] -= amount
    update_last_activity(user)
    save_users(users)
    return f"Successfully withdrew ${amount:.2f} from account {account_number}"

def transfer(username, from_account_number, to_account_number, amount):
    users = load_users()
    valid, result = security_checks(username, users)
    if not valid:
        return result
    
    user = result
    from_account = find_account(user.get('accounts', []), from_account_number)
    to_account = find_account(user.get('accounts', []), to_account_number)

    if from_account is None:
        return "Source account not found"
    if to_account is None:
        return "Destination account not found"
    if from_account == to_account:
        return "Cannot transfer to the same account"
    
    if from_account['balance'] < amount:
        return "Insufficient funds"
    if amount > TRANSFER_LIMIT:
        return f"Amount exceeds transfer limit of ${TRANSFER_LIMIT:.2f}"
    
    from_account['balance'] -= amount
    to_account['balance'] += amount
    update_last_activity(user)
    save_users(users)
    return f"Successfully transferred ${amount:.2f} from account {from_account_number} to account {to_account_number}"

def member_transfer(from_user, from_account_number, to_user, amount):
    users = load_users()
    valid_sender, sender = security_checks(from_user, users)
    if not valid_sender:
        return sender
    
    valid_recipient, recipient = security_checks(to_user, users)
    if not valid_recipient:
        return recipient

    from_account = find_account(sender.get('accounts', []), from_account_number)

    if from_account is None:
        return "Account not found"
    
    if from_account['balance'] < amount:
        return "Insufficient funds"
    if amount > TRANSFER_LIMIT:
        return f"Amount exceeds transfer limit of ${TRANSFER_LIMIT:.2f}"
    
    recipient_accounts = recipient.get('accounts', [])
    if not recipient_accounts:
        return "Recipient has no accounts"
    
    to_account = recipient_accounts[0]

    from_account['balance'] -= amount
    to_account['balance'] += amount
    update_last_activity(sender)
    save_users(users)
    return f"Successfully transferred ${amount:.2f} from account {from_account_number} to account {to_account['account_number']} of {to_user}"

def unlock_user(username):
    with open(USER_DB, 'r') as file:
        data = json.load(file)

    user_found = False
    for user in data.get('users', []):
        if user['username'] == username:
            user['incorrect_attempts'] = 0
            user['locked'] = False
            user_found = True
            break

    if not user_found:
        print(f"Error: No user found with username '{username}'")
        return
    
    try:
        with open(USER_DB, 'w') as file:
            json.dump(data, file, indent=4)
        print(f"User '{username}' has been unlocked successfully")
    except IOError:
        print(f"Error: Could not write to {USER_DB} file")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python unlocker.py <username>")
    else:
        unlock_user(sys.argv[1])

def load_users():
    with open(USER_DB, 'r') as file:
        return json.load(file)
    
def save_users(users):
    with open(USER_DB, 'w') as file:
        json.dump(users, file, indent=4)

def find_user(username, users):
    for user in users['users']:
        if user['username'] == username:
            return user
    return None

def is_session_timed_out(last_activity):
    return (time.time() - last_activity) > 300

def update_last_activity(user):
    user['last_activity'] = time.time()
    save_users(load_users())

def is_account_locked(user):
    return user.get('locked', False)

def find_account(accounts, account_number):
    for acc in accounts:
        if acc['account_number'] == account_number:
            return acc
    return None

def add_account(username, account_number):
    users = load_users()
    valid, result = security_checks(username, users)
    if not valid:
        return result
    
    user = result
    accounts = user.get('accounts', [])
    if any(acc['account_number'] == account_number for acc in accounts):
        return "Account already exists"
    
    user['accounts'].append({
        'account_number': account_number,
        'balance': 0
    })

    update_last_activity(user)
    save_users(users)
    return f"Successfully added new account {account_number}"

def create_account(username, password):
    users = load_users()

    if any(u['username'] == username for u in users['users']):
        return "Username already exists"

    new_user = {
        "username": username,
        "password": password,
        "accounts": [
            {
                "account_number": 101,
                "balance": 0
            }
        ],
        "incorrect_attempts": 0,
        "locked": False,
        "last_activity": time.time()
    }

    users['users'].append(new_user)
    save_users(users)

    return "Account successfully created"
