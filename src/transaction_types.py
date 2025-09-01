import time

class TransactionType:
    """Base class for transaction types."""
    def validate(self, *args, **kwargs):
        return True

class UTXOTransaction(TransactionType):
    """UTXO model transaction."""
    def __init__(self, inputs, outputs):
        self.inputs = inputs  # list of (txid, index)
        self.outputs = outputs  # list of (address, amount)

    def validate(self, utxo_set):
        # Check all inputs are unspent
        for txid, idx in self.inputs:
            if (txid, idx) not in utxo_set:
                return False
        return True

    def apply(self, utxo_set):
        # Spend inputs, add outputs
        for txid, idx in self.inputs:
            utxo_set.pop((txid, idx), None)
        new_txid = f"tx_{int(time.time())}"
        for i, (address, amount) in enumerate(self.outputs):
            utxo_set[(new_txid, i)] = (address, amount)
        return utxo_set

class AccountTransaction(TransactionType):
    """Account-based transaction."""
    def __init__(self, sender, recipient, amount):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount

    def validate(self, balances):
        return balances.get(self.sender, 0) >= self.amount

    def apply(self, balances):
        balances[self.sender] -= self.amount
        balances[self.recipient] = balances.get(self.recipient, 0) + self.amount
        return balances

class ConfidentialTransaction(TransactionType):
    """Confidential transaction (stub)."""
    def __init__(self, sender, recipient, commitment):
        self.sender = sender
        self.recipient = recipient
        self.commitment = commitment  # e.g., Pedersen commitment

    def validate(self, *args, **kwargs):
        # Stub: always valid
        return True

class MultiSigTransaction(TransactionType):
    """Multi-signature transaction."""
    def __init__(self, signers, required, sender, recipient, amount):
        self.signers = signers  # list of public keys
        self.required = required  # number of required signatures
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.signatures = []

    def add_signature(self, signature):
        self.signatures.append(signature)

    def validate(self, balances):
        return len(self.signatures) >= self.required and balances.get(self.sender, 0) >= self.amount

    def apply(self, balances):
        balances[self.sender] -= self.amount
        balances[self.recipient] = balances.get(self.recipient, 0) + self.amount
        return balances

class AtomicSwapTransaction(TransactionType):
    """Atomic swap transaction (cross-chain stub)."""
    def __init__(self, sender, recipient, amount, secret_hash, expiry):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.secret_hash = secret_hash
        self.expiry = expiry
        self.redeemed = False

    def redeem(self, secret):
        if not self.redeemed and hash(secret) == self.secret_hash:
            self.redeemed = True
            return True
        return False

    def validate(self, balances):
        # Only valid if not expired and not redeemed
        return not self.redeemed and time.time() < self.expiry and balances.get(self.sender, 0) >= self.amount

    def apply(self, balances):
        if self.redeemed:
            balances[self.sender] -= self.amount
            balances[self.recipient] = balances.get(self.recipient, 0) + self.amount
        return balances

class TimeLockedTransaction(TransactionType):
    """Time-locked transaction."""
    def __init__(self, sender, recipient, amount, unlock_time):
        self.sender = sender
        self.recipient = recipient
        self.amount = amount
        self.unlock_time = unlock_time

    def validate(self, balances):
        return time.time() >= self.unlock_time and balances.get(self.sender, 0) >= self.amount

    def apply(self, balances):
        balances[self.sender] -= self.amount
        balances[self.recipient] = balances.get(self.recipient, 0) + self.amount
        return balances
