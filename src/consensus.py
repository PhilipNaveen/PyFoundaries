class Consensus:
    """
    Base Consensus class. Users can inherit and override methods for custom consensus.
    """
    def __init__(self, config_or_name):
        if isinstance(config_or_name, str):
            self.name = config_or_name
        else:
            self.name = getattr(config_or_name, 'type', 'CustomConsensus')

    def validate_block(self, block, chain):
        """
        Validate a block before adding to the chain. Override for custom logic.
        """
        return True

    def on_block_mined(self, block, chain):
        """
        Optional hook called after a block is mined. Override for custom logic.
        """
        pass


class PoWConsensus(Consensus):
    """
    Proof-of-Work Consensus implementation.
    """
    def __init__(self, config_or_name):
        super().__init__(config_or_name)
        self.difficulty = getattr(config_or_name, 'params', {}).get('difficulty', 2)

    def validate_block(self, block, chain):
        # Simple PoW: block hash must start with '0' * difficulty
        return block.hash.startswith('0' * self.difficulty)

    def on_block_mined(self, block, chain):
        print(f"PoW block mined with hash: {block.hash}")


class DPoSConsensus(Consensus):
    """
    Delegated Proof-of-Stake Consensus implementation.
    """
    def __init__(self, config_or_name):
        super().__init__(config_or_name)
        self.validators = getattr(config_or_name, 'params', {}).get('validators', [])

    def validate_block(self, block, chain):
        # Stub: always valid, but could check validator signatures
        return True

    def on_block_mined(self, block, chain):
        print(f"DPoS block mined by validators: {self.validators}")
