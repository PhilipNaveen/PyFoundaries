class SmartContract:
    name = "BaseContract"
    def execute(self, tx, chain):
        pass

class ERC20(SmartContract):
    name = "ERC20"
    def __init__(self):
        self.balances = {}
    def execute(self, tx, chain):
        # Minimal stub: update balances
        sender = tx.sender
        recipient = tx.recipient
        amount = tx.amount
        self.balances[sender] = self.balances.get(sender, 0) - amount
        self.balances[recipient] = self.balances.get(recipient, 0) + amount
