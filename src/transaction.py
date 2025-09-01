class Transaction:
    def __init__(self, sender, recipient, amount, contract=None):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.contract = contract
        # Add more fields as needed
