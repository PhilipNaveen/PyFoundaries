class BlockConfig:
    def __init__(self, size="dynamic", interval=13, structure="merkle_tree", header_fields=None):
        self.size = size
        self.interval = interval
        self.structure = structure
        self.header_fields = header_fields or ["prev_hash", "merkle_root", "timestamp", "nonce", "difficulty", "version"]

class ConsensusConfig:
    def __init__(self, type="PoS", variant="delegated", params=None):
        self.type = type
        self.variant = variant
        self.params = params or {}

class NetworkConfig:
    def __init__(self, type="public", node_type="full", peer_protocol="gossip"):
        self.type = type
        self.node_type = node_type
        self.peer_protocol = peer_protocol

class ContractConfig:
    def __init__(self, vm="EVM", language="solidity", verification="formal"):
        self.vm = vm
        self.language = language
        self.verification = verification

class StateConfig:
    def __init__(self, model="account", pruning="snapshot", channels=True):
        self.model = model
        self.pruning = pruning
        self.channels = channels

class GovernanceConfig:
    def __init__(self, model="community", tokens="GOV", voting="liquid"):
        self.model = model
        self.tokens = tokens
        self.voting = voting
