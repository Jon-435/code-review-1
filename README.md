# 4360-banking

A command line based banking app. Navigate the menu through numeric input (1-5).

## LOGIN
You can login to the banking application using **"john_doe", "password123"** or **"jane_doe", "password456"**.

## FUNCTIONS
- Deposit
- Withdraw
- Transfer

## DATABASE
Uses json as a mock database.

## FEATURES
- Account will be timed out after 5 minutes of no interaction
- After 5 incorrect login attempts, the user will be locked out

If you're locked out of the account, go into "users.json":
- change "incorrect_attempts" to "0"
- change "locked" to "false"