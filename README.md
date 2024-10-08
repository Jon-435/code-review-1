# 4360-banking

A command line based banking app. Navigate the menu through numeric input (1-9).

## RUN
`python main.py`

## LOGIN
You can login to the banking application using one of the default accounts, **"john_doe", "password123"** or **"jane_doe", "password456"**.

## FUNCTIONS
- System allows users to view the balance of their accounts
- System allows users to deposit, withdraw, and transfer funds
- System enforces a timeout after 5 minutes of inactivity
- User accounts are locked after 5 incorrect login attempts
- Transfers are limited to amounts of 5000.00 or less
## NON-FUNCTIONS
- Application processes should respond instantly to user input

## DATABASE
Uses json as a mock database.

## FEATURES
- Account creation
- Member to member transferring

If you're locked out of the account, run the following:
`python unlocker.py <username>`