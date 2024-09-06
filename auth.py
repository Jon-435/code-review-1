from umanager import load_users, save_users, find_user, update_last_activity, is_account_locked

# def hash_password(password):
#     return hashlib.sha256(password.encode()).hexdigest()

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
    user = find_user(username, users)
    if user:
        update_last_activity(user)
        save_users(users)
        return "Logged out successfully"
    return "User not found"