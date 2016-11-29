from decimal import Decimal
import getpass


def lines(path):
    with open('history.txt') as file_:
        for line in file_:
            yield line


def records(lines):
    for line in lines:
        yield line.split(',')


# Number,Amount
history = [(number, Decimal(amount)) for line in records(lines('history.txt'))]

# Number,Pin
accounts = list(records(lines('accounts.txt')))

account_numbers = [number for number,pin in accounts]

print('***********************')
print('Heidelberg Student Bank')
print('***********************')

account_number = input('Account Number: ')
if account_number not in account_numbers:
    print("Unknown Account.")
    exit()
else:
    pins = [
        pin.strip()
        for number,pin
        in accounts
        if number == account_number
    ]
    pin = pins[0]

logged_in = False

# Run Menu in Loop
while True:
    print("Menu")
    print("(B)alance (D)eposit (W)ithdraw (R)eport (Q)uit")
    choice = input("Select: ").lower()

    if not logged_in:
        for _ in range(3):
            print('Please enter PIN. Entry will be hidden.')
            entered_pin = getpass.getpass('Pin: ')
            if entered_pin == pin:
                logged_in = True
                break

    if not logged_in:
        print('You failed to authenticate.')
        exit()
        break

    if choice.strip() not in 'bdwrq':
        continue

    if choice == 'b':
        print("Balance")
        balance = Decimal(0.0)
        for number, amount in history:
            if number == account_number:
                balance += amount
        print(balance)
        continue

    if choice == 'd':
        print('Deposit')
        amount = input('Amount: ')
        amount = Decimal(amount)
        history.append((account_number, Decimal(amount)))
        continue

    if choice == 'w':
        print('Withdraw')
        amount = input('Amount: ')
        amount = Decimal(amount)
        history.append((account_number, -1 * Decimal(amount)))
        continue

    if choice == 'r':
        print('Report')
        for number, amount in history:
            if number != account_number:
                continue
            if amount < Decimal(0.0):
                print(amount * Decimal(-1), 'Withdraw')
            else:
                print(amount, 'Deposit')
        continue

    if choice == 'q':
        print('Thank you for using Heidelberg Student Bank services')
        break

# Program Done. Save History.
lines = ['%s,%s' % entry for entry in history]
content = '\n'.join(lines)

with open('history.txt', 'w') as file_:
    file_.write(content)
