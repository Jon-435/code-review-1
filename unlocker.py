import json
import sys

USER_DB = "users.json"

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
        print(f"Error: No user found with username '{username}")
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