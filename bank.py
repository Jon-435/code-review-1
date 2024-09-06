import time
from umanager import load_users, save_users, find_user, is_account_locked, is_session_timed_out, find_account, update_last_activity

TRANSFER_LIMIT = 5000.00

def view_balance(username):
    users = load_users()
    user = find_user(username, users)
    if user and not is_account_locked(user):
        if is_session_timed_out(user['last_activity']):
            return "Session timed out"
        
        update_last_activity(user)
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
        
        update_last_activity(user)
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
        update_last_activity(user)
        save_users(users)
        return f"Successfuly withdrew ${amount:.2f} from account {account_number}"
    return "User not found or account is locked"

def transfer(username, from_account_number, to_account, amount):
    users = load_users()
    user = find_user(username, users)
    
    if user and not is_account_locked(user):
        if is_session_timed_out(user['last_activity']):
            return "Session timed out"
        
        from_account = find_account(user.get('accounts', []), from_account_number)
        to_acc = find_account(user.get('accounts', []), to_account)

        if from_account is None:
            return "Source account not found"
        if to_acc is None:
            return "Destination account not found"
        if from_account == to_acc:
            return "Cannot transfer to the same account"
        
        if from_account['balance'] < amount:
            return "Insufficient funds"
        if amount > TRANSFER_LIMIT:
            return f"Amount exceeds transfer limit of ${TRANSFER_LIMIT:.2f}"
        
        from_account['balance'] -= amount
        to_acc['balance'] += amount
        update_last_activity(user)
        save_users(users)
        return f"Successfully transferred ${amount:.2f} from account {from_account_number} to account {to_account}"
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
        update_last_activity(sender)
        save_users(users)
        return f"Successfully transferred ${amount:.2f} from account {from_account_number} to account {to_account['account_number']} of {to_user}"
    return "User not found or account is locked"