import json
import time

USER_DB = "users.json"
TRANSFER_LIMIT = 5000.00

def load_users():
    with open(USER_DB, 'r') as file:
        return json.load(file)
    
def save_users(users):
    with open(USER_DB, 'w') as file:
        json.dump(users, file, indent=4)

# def hash_password(password):
#     return hashlib.sha256(password.encode()).hexdigest()

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

def find_user(username, users):
    for user in users['users']:
        if user['username'] == username:
            return user
    return None

def find_account(accounts, account_number):
    for acc in accounts:
        if acc['account_number'] == account_number:
            return acc
    return None

def add_account(username, account_number):
    users = load_users()
    user = find_user(username, users)

    if user and not is_account_locked(user):
        if is_session_timed_out(user['last_activity']):
            return "Session timed out"
        
        accounts = user.get('accounts', [])
        if any(acc['account_number'] == account_number for acc in accounts):
            return "Account already exists"
        
        user['accounts'].append({
            'account_number': account_number,
            'balance': 0
        })

        user['last_activity'] = time.time()
        save_users(users)
        return f"Successfully added new account {account_number}"
    return "User not found or account is locked"

def is_account_locked(user):
    return user.get('locked', False)

def login(username, password):
    users = load_users()
    user = find_user(username, users)
    if not user:
        return "User not found"
    
    if is_account_locked(user):
        return "Account is locked due to multiple failed login attempts"
    
    # if hash_password(password) == user['password']:
    if password == user['password']:
        user['incorrect_attempts'] = 0
        user['last_activity'] = time.time()
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
    user = find_user(username, users)
    if user:
        user['last_activity'] = time.time()
        save_users(users)
        return "Logged out successfully"
    return "User not found"

def is_session_timed_out(last_activity):
    return (time.time() - last_activity) > 300

def view_balance(username):
    users = load_users()
    user = find_user(username, users)
    if user and not is_account_locked(user):
        if is_session_timed_out(user['last_activity']):
            return "Session timed out"
        
        user['last_activity'] = time.time()
        save_users(users)

        balance_info = []
        for account in user.get('accounts', []):
            balance_info.append(f"Account {account['account_number']}: ${account['balance']:.2f}")

        if balance_info:
            return "\n".join(balance_info)
        else:
            return "No accounts found for this user"
    return "User not found or account is locked"

def deposit(username, account_number, amount):
    users = load_users()
    user = find_user(username, users)
    if user and not is_account_locked(users):
        if is_session_timed_out(user['last_activity']):
            return "Session timed out"
        
        accounts = user.get('accounts', [])
        account = find_account(accounts, account_number)

        if account is None:
            return "Account not found"
        
        user['last_activity'] = time.time()
        account['balance'] += amount
        save_users(users)
        return f"Successfully deposited ${amount:.2f} into account {account_number}"
    return "User not found or account is locked"

def withdraw(username, account_number, amount):
    users = load_users()
    user = find_user(username, users)
    if user and not is_account_locked(user):
        if is_session_timed_out(user['last_activity']):
            return "Session timed out"
        
        accounts = user.get('accounts', [])
        account = find_account(accounts, account_number)

        if account is None:
            return "Account not found"

        if account['balance'] < amount:
            return "Insufficient funds"
        
        account['balance'] -= amount
        user['last_activity'] = time.time()
        save_users(users)
        return f"Successfuly withdrew ${amount:.2f} from account {account_number}"
    return "User not found or account is locked"

def transfer(username, from_account, to_account, amount):
    users = load_users()
    user = find_user(username, users)
    
    if user and not is_account_locked(user):
        if is_session_timed_out(user['last_activity']):
            return "Session timed out"
        
        f_acc = find_account(user.get('accounts', []), from_account)
        to_acc = find_account(user.get('accounts', []), to_account)

        if f_acc is None:
            return "Source account not found"
        if to_acc is None:
            return "Destination account not found"
        if f_acc == to_acc:
            return "Cannot transfer to the same account"
        
        if f_acc['balance'] < amount:
            return "Insufficient funds"
        if amount > TRANSFER_LIMIT:
            return f"Amount exceeds transfer limit of ${TRANSFER_LIMIT:.2f}"
        
        f_acc['balance'] -= amount
        to_acc['balance'] += amount
        user['last_activity'] = time.time()
        save_users(users)
        return f"Successfully transferred ${amount:.2f} from account {from_account} to account {to_account}"
    return "User not found or account is locked"

def member_transfer(from_user, from_account_number, to_user, amount):
    users = load_users()
    sender = find_user(from_user, users)
    recipient = find_user(to_user, users)

    if sender and recipient and not is_account_locked(sender):
        if is_session_timed_out(sender['last_activity']):
            return "Session timed out"
        
        from_account = find_account(sender.get('accounts', []), from_account_number)

        if from_account is None:
            return "Account not found"
        
        if from_account['balance'] < amount:
            return "Insufficient funds"
        if amount > TRANSFER_LIMIT:
            return f"Amount exceeds transfer limit of ${TRANSFER_LIMIT:.2f}"
        
        recipient_account = recipient.get('accounts', [])
        if not recipient_account:
            return "Recipient has no accounts"
        
        to_account = recipient_account[0]

        from_account['balance'] -= amount
        to_account['balance'] += amount
        sender['last_activity'] = time.time()
        save_users(users)
        return f"Successfully transferred ${amount:.2f} from account {from_account_number} to account {to_account['account_number']} of {to_user}"
    return "User not found or account is locked"