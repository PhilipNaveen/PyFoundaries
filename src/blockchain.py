


from .consensus import Consensus
from .block import Block
from .transaction import Transaction
from .network import Node
from .config import BlockConfig, ConsensusConfig, NetworkConfig, ContractConfig, StateConfig, GovernanceConfig
from .backend import GethBackend

class Blockchain:
    """
    Modular Blockchain abstraction supporting configuration and deployment.
    """

    def __init__(self, name="MyChain", block=None, consensus=None, network=None, contract=None, state=None, governance=None, initial_nodes=None, backend=None, consensus_class=None):
        self.name = name
        self.block_config = block or BlockConfig()
        self.consensus_config = consensus or ConsensusConfig()
        self.network_config = network or NetworkConfig()
        self.contract_config = contract or ContractConfig()
        self.state_config = state or StateConfig()
        self.governance_config = governance or GovernanceConfig()

        self.node = Node(initial_nodes[0] if initial_nodes else "127.0.0.1:5000")
        for peer in (initial_nodes or [])[1:]:
            self.node.add_peer(peer)
        # Allow user to pass a custom consensus class
        if consensus_class:
            self.consensus = consensus_class(self.consensus_config)
        else:
            self.consensus = Consensus(self.consensus_config.type)
        self.contracts = []
        self.chain = []
        self.transaction_pool = []
        self.backend = backend or None
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, "0", [], nonce=0)
        self.chain.append(genesis_block)

    def add_transaction(self, sender, recipient, amount, contract=None):
        tx = Transaction(sender, recipient, amount, contract)
        self.transaction_pool.append(tx)

    def add_smart_contract(self, contract_cls):
        contract = contract_cls()
        self.contracts.append(contract)

    def mine_block(self):
        previous_block = self.chain[-1]
        block = Block(
            index=len(self.chain),
            previous_hash=previous_block.hash,
            transactions=[str(tx.__dict__) for tx in self.transaction_pool],
            nonce=0
        )
        # Use consensus to validate or modify block before adding
        if hasattr(self.consensus, "validate_block"):
            if not self.consensus.validate_block(block, self.chain):
                print("Block failed consensus validation.")
                return
        if hasattr(self.consensus, "on_block_mined"):
            self.consensus.on_block_mined(block, self.chain)
        self.chain.append(block)
        self.transaction_pool = []
        print(f"Block {block.index} mined: {block.hash}")

    def run(self):
        print(f"Running blockchain '{self.name}'")
        print(f"Block config: {self.block_config.__dict__}")
        print(f"Consensus config: {self.consensus_config.__dict__}")
        print(f"Network config: {self.network_config.__dict__}")
        print(f"Contract config: {self.contract_config.__dict__}")
        print(f"State config: {self.state_config.__dict__}")
        print(f"Governance config: {self.governance_config.__dict__}")
        print(f"Initial node: {self.node.address}")
        print(f"Peers: {self.node.peers}")
        print(f"Smart contracts: {[c.name for c in self.contracts]}")
        print(f"Genesis block: {self.chain[0].hash}")
        if self.transaction_pool:
            self.mine_block()
        print(f"Chain length: {len(self.chain)}")

    def deploy(self, backend=None):
        self.backend = backend or self.backend or GethBackend()
        print(f"Deploying blockchain '{self.name}' to backend: {self.backend.rpc_url}")
        return True

    def publish_contract(self, contract_cls, sender, bytecode, abi):
        if not self.backend:
            raise Exception("No backend configured. Call deploy() first.")
        print(f"Publishing contract '{contract_cls.name}' from {sender}")
        result = self.backend.deploy_contract(bytecode, abi, sender)
        print(f"Contract deployment result: {result}")
        return result
    def __init__(self, name="MyChain", block=None, consensus=None, network=None, contract=None, state=None, governance=None, initial_nodes=None, backend=None):
        self.name = name
        self.block_config = block or BlockConfig()
        self.consensus_config = consensus or ConsensusConfig()
        self.network_config = network or NetworkConfig()
        self.contract_config = contract or ContractConfig()
        self.state_config = state or StateConfig()
        self.governance_config = governance or GovernanceConfig()

        self.node = Node(initial_nodes[0] if initial_nodes else "127.0.0.1:5000")
        class Blockchain:
            """
            Modular Blockchain abstraction supporting configuration and deployment.
            """

            def __init__(self, name="MyChain", block=None, consensus=None, network=None, contract=None, state=None, governance=None, initial_nodes=None, backend=None):
                """
                Initialize the Blockchain with modular configs and optional backend.
                """
                self.name = name
                self.block_config = block or BlockConfig()
                self.consensus_config = consensus or ConsensusConfig()
                self.network_config = network or NetworkConfig()
                self.contract_config = contract or ContractConfig()
                self.state_config = state or StateConfig()
                self.governance_config = governance or GovernanceConfig()

                self.node = Node(initial_nodes[0] if initial_nodes else "127.0.0.1:5000")
                for peer in (initial_nodes or [])[1:]:
                    self.node.add_peer(peer)
                self.consensus = Consensus(self.consensus_config.type)
                self.contracts = []
                self.chain = []
                self.transaction_pool = []
                self.backend = backend or None
                self.create_genesis_block()

            def create_genesis_block(self):
                """
                Create the genesis block for the chain.
                """
                genesis_block = Block(0, "0", [], nonce=0)
                self.chain.append(genesis_block)

            def add_transaction(self, sender, recipient, amount, contract=None):
                """
                Add a transaction to the pool.
                """
                tx = Transaction(sender, recipient, amount, contract)
                self.transaction_pool.append(tx)

            def add_smart_contract(self, contract_cls):
                """
                Add a smart contract to the blockchain.
                """
                contract = contract_cls()
                self.contracts.append(contract)

            def mine_block(self):
                """
                Mine a block (stub for PoS/PoW).
                """
                previous_block = self.chain[-1]
                block = Block(
                    index=len(self.chain),
                    previous_hash=previous_block.hash,
                    transactions=[str(tx.__dict__) for tx in self.transaction_pool],
                    nonce=0
                )
                self.chain.append(block)
                self.transaction_pool = []
                print(f"Block {block.index} mined: {block.hash}")

            def run(self):
                """
                Run the blockchain node (prints config and mines if transactions exist).
                """
                print(f"Running blockchain '{self.name}'")
                print(f"Block config: {self.block_config.__dict__}")
                print(f"Consensus config: {self.consensus_config.__dict__}")
                print(f"Network config: {self.network_config.__dict__}")
                print(f"Contract config: {self.contract_config.__dict__}")
                print(f"State config: {self.state_config.__dict__}")
                print(f"Governance config: {self.governance_config.__dict__}")
                print(f"Initial node: {self.node.address}")
                print(f"Peers: {self.node.peers}")
                print(f"Smart contracts: {[c.name for c in self.contracts]}")
                print(f"Genesis block: {self.chain[0].hash}")
                if self.transaction_pool:
                    self.mine_block()
                print(f"Chain length: {len(self.chain)}")

            def deploy(self, backend=None):
                """
                Deploy the blockchain to a backend (e.g., Geth).
                """
                self.backend = backend or self.backend or GethBackend()
                print(f"Deploying blockchain '{self.name}' to backend: {self.backend.rpc_url}")
                # Real implementation would set up chain state, accounts, etc. on the backend
                return True

            def publish_contract(self, contract_cls, sender, bytecode, abi):
                """
                Publish a smart contract to the backend.
                """
                if not self.backend:
                    raise Exception("No backend configured. Call deploy() first.")
                print(f"Publishing contract '{contract_cls.name}' from {sender}")
                result = self.backend.deploy_contract(bytecode, abi, sender)
                print(f"Contract deployment result: {result}")
                return result
