class GovernanceMechanism:
    """Base class for governance mechanisms."""
    pass

class OnChainVoting(GovernanceMechanism):
    """Simple on-chain voting."""
    def __init__(self):
        self.votes = {}
    def vote(self, proposal_id, voter, choice):
        self.votes.setdefault(proposal_id, {})[voter] = choice
    def tally(self, proposal_id):
        choices = self.votes.get(proposal_id, {}).values()
        return {c: list(choices).count(c) for c in set(choices)}

class GovernanceToken(GovernanceMechanism):
    """Governance token (ERC20-like)."""
    def __init__(self):
        self.balances = {}
    def mint(self, address, amount):
        self.balances[address] = self.balances.get(address, 0) + amount
    def balance_of(self, address):
        return self.balances.get(address, 0)

class LiquidDemocracy(GovernanceMechanism):
    """Delegation logic for liquid democracy."""
    def __init__(self):
        self.delegations = {}
    def delegate(self, voter, to):
        self.delegations[voter] = to
    def get_delegate(self, voter):
        return self.delegations.get(voter, voter)

class Futarchy(GovernanceMechanism):
    """Stub for prediction market-based governance."""
    def __init__(self):
        self.markets = {}
    def create_market(self, proposal_id):
        self.markets[proposal_id] = []
    def bet(self, proposal_id, outcome, amount):
        self.markets.setdefault(proposal_id, []).append((outcome, amount))

class HardFork(GovernanceMechanism):
    """Chain versioning for hard forks."""
    def __init__(self):
        self.versions = [1]
    def fork(self, new_version):
        self.versions.append(new_version)

class SoftFork(GovernanceMechanism):
    """Soft fork logic."""
    def __init__(self):
        self.restrictions = []
    def add_restriction(self, rule):
        self.restrictions.append(rule)
