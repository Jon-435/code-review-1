import json
import time

USER_DB = "users.json"

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
        "balance": 0.00,
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
        return f"Your balance is ${user['balance']:.2f}"
    return "User not found or account is locked"

def deposit(username, amount):
    users = load_users()
    user = find_user(username, users)
    if user and not is_account_locked(users):
        if is_session_timed_out(user['last_activity']):
            return "Session timed out"
        user['last_activity'] = time.time()
        user['balance'] += amount
        save_users(users)
        return f"Successfully deposited ${amount:.2f}"
    return "User not found or account is locked"

def withdraw(username, amount):
    users = load_users()
    user = find_user(username, users)
    if user and not is_account_locked(user):
        if is_session_timed_out(user['last_activity']):
            return "Session timed out"
        if user['balance'] >= amount:
            user['balance'] -= amount
            user['last_activity'] = time.time()
            save_users(users)
            return f"Successfuly withdrew ${amount:.2f}"
        return "Insufficient funds"
    return "User not found or account is locked"

def transfer(from_user, to_user, amount):
    users = load_users()
    user_from = find_user(from_user, users)
    user_to = find_user(to_user, users)
    transfer_limit = 3000.00

    if user_from and user_to and not is_account_locked(user_from):
        if is_session_timed_out(user_from['last_activity']):
            return "Session timed out"
        if user_from['balance'] >= amount and amount <= transfer_limit:
            user_from['balance'] -= amount
            user_to['balance'] += amount
            user_from['last_activity'] = time.time()
            save_users(users)
            return f"Successfully transferred ${amount:.2f} to {to_user}"
        return f"Insufficient funds or amount exceeds transfer limit of ${transfer_limit:.2f}"
    return "User not found or account is locked"