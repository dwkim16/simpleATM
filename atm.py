
# Bank system
class BankSystem:
    def __init__(self):
        self.userInfo = {}

    # Add new card info in the bank system
    def addNewCard(self, cardNum, account, pin, amount):
        self.userInfo[cardNum] = {"account": {account: amount}, "pin": pin}

    # Update the amount of an account if the card exists
    def updateAmount(self, cardNum, account, amount):
        if account in self.userInfo[cardNum]["account"]:
            self.userInfo[cardNum]["account"][account] = amount
            return amount
        else:
            return None

    # Add new account of a certain card in the bank system
    def addNewAccount(self, cardNum, account, amount):
        if cardNum in self.userInfo and account not in self.userInfo[cardNum]["account"]:
            self.userInfo[cardNum]["account"][account] = amount

    # Check if pin is correct and if true return account
    def pinCheck(self, cardNum, pin):
        if cardNum not in self.userInfo:
            return None
        if self.userInfo[cardNum]["pin"] == pin:
            return self.userInfo[cardNum]["account"]
        else:
            return None


class AtmController:
    def __init__(self, bank, cash):
        self.bankSystem = bank
        self.cashBin = cash
        self.userAccount = None

    # User inserts card and check the PIN validity
    def insertCard(self, cardNum, pin):
        self.userAccount = self.bankSystem.pinCheck(cardNum, pin)
        if self.userAccount is None:
            print("Incorrect PIN or Incorrect Card Number")
            return False
        else:
            print("Select your Account")
            return True

    # See if the account is valid and do the action
    def selectAccountAndAction(self, cardNum, account, action, amount=0):
        if account not in self.userAccount:
            print("Invalid Account")
            return None
        else:
            if action == "See Balance":
                return self.userAccount[account]
            elif action == "Deposit":
                newAmount = self.userAccount[account] + amount

            elif action == "Withdraw":
                if self.userAccount[account] >= amount and self.cashBin >= amount:
                    newAmount = self.userAccount[account] - amount
                else:
                    return None
            else:
                return None
            self.userAccount[account] = newAmount
            self.cashBin += amount
            self.bankSystem.updateAmount(cardNum, account, newAmount)
            return newAmount

    # For testing purposes
    def __call__(self, cardNum, account, pin, amount, action):
        pinValidated = self.insertCard(cardNum, pin)
        if pinValidated:
            newAmount = self.selectAccountAndAction(cardNum, account, action, amount)
            if newAmount is  not None:
                return newAmount
        return "Invalid Action"

if __name__ == '__main__':

    newBankSystem = BankSystem()
    newAtmController = AtmController(newBankSystem, 900)

    # Initialize Bank
    newBankSystem.addNewCard(1111222233334444, "Checking", 1234, 100)
    newBankSystem.addNewCard(5555666677778888, "Checking", 5678, 1000)
    newBankSystem.addNewAccount(1111222233334444, "Saving", 500)
    actions = ["See Balance", "Deposit", "Withdraw"]

    # Test 1: test See Balance
    if newAtmController(1111222233334444, "Checking", 1234, 0, "See Balance") == 100:
        print("PASS -- ATM works correctly for See Balance.")
    else:
        print("FAIL -- ATM does not work correctly for See Balance.")

    # Test 2: test Deposit
    if newAtmController(1111222233334444, "Checking", 1234, 10, "Deposit") == 110:
        print("PASS -- ATM works correctly for Deposit.")
    else:
        print("FAIL -- ATM does not work correctly for Deposit.")

    # Test 3: test Withdraw (after test 2 deposit we get 110 -> -10 will be 100 again)
    if newAtmController(1111222233334444, "Checking", 1234, 10, "Withdraw") == 100:
        print("PASS -- ATM works correctly for Withdraw.")
    else:
        print("FAIL -- ATM does not work correctly for Withdraw.")

    # Test 4: Incorrect card number
    if newAtmController(1111555533334444, "Checking", 1234, 10, "Deposit") == "Invalid Action":
        print("PASS -- ATM works correctly for Incorrect card number.")
    else:
        print("FAIL -- ATM does not work correctly for Incorrect card number.")

    # Test 5: Incorrect PIN number
    if newAtmController(1111222233334444, "Checking", 4321, 10, "Deposit") == "Invalid Action":
        print("PASS -- ATM works correctly for Incorrect PIN.")
    else:
        print("FAIL -- ATM does not work correctly for Incorrect PIN.")

    # Test 6: Incorrect account
    if newAtmController(5555666677778888, "Saving", 5678, 10, "Deposit") == "Invalid Action":
        print("PASS -- ATM works correctly for Incorrect account.")
    else:
        print("FAIL -- ATM does not work correctly for Incorrect account.")

    # Test 7: Withdrawing more than balance
    if newAtmController(1111222233334444, "Checking", 1234, 200, "Withdraw") == "Invalid Action":
        print("PASS -- ATM works correctly for Withdrawing more than balance.")
    else:
        print("FAIL -- ATM does not work correctly for Withdrawing more than balance.")

    # Test 8: Withdrawing more than cash bin amount
    if newAtmController(5555666677778888, "Checking", 5678, 1000, "Withdraw") == "Invalid Action":
        print("PASS -- ATM works correctly for Withdrawing more than cash bin amount.")
    else:
        print("FAIL -- ATM does not work correctly for Withdrawing more than cash bin amount.")