import json
import time

USER_DB = "users.json"

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

        update_last_activity(user)
        save_users(users)
        return f"Successfully added new account {account_number}"
    return "User not found or account is locked"

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