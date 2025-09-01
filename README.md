# PyFoundaries Modular Blockchain Framework


<img width="2311" height="1111" alt="Screenshot 2025-09-01 113825" src="https://github.com/user-attachments/assets/7e56b0d1-3711-487d-91f1-9323c4bcc826" />

This repo is a simple proof of concept that allows for blockchain development with a simple, Keras-esque API.

## Features
- Pluggable consensus algorithms: PoW, PoS, DPoS, PBFT, PoA, custom
- Smart contract engines: EVM (Geth RPC), WASM, Native Python
- Transaction types: UTXO, account-based, confidential, multi-sig, atomic swap, time-locked
- Network features: node discovery, gossip, DHT, sharding, mesh, Lightning, node roles
- API integrations: REST (Flask), CLI, GraphQL, WebSocket, RPC, explorer, wallet
- Governance: on-chain voting, governance tokens, liquid democracy, futarchy, hard/soft forks

## Quick Start

### Install dependencies
```bash
pip install flask
# For WASM contracts:
pip install wasmer
```

### Example Usage
```python
from pychain import Blockchain, BlockConfig, ConsensusConfig, NetworkConfig, ContractConfig, StateConfig, GovernanceConfig
from pychain.consensus import PoWConsensus
from pychain.contracts.engines import EVMEngine
from pychain.transaction_types import AccountTransaction

chain = Blockchain(
    name="MyChain",
    block=BlockConfig(size="dynamic"),
    consensus=ConsensusConfig(type="PoW", params={"difficulty": 2}),
    consensus_class=PoWConsensus,
    initial_nodes=["127.0.0.1:5000"]
)

# Add transactions
chain.add_transaction("Alice", "Bob", 10)
chain.add_transaction("Bob", "Carol", 5)

# Mine a block
chain.mine_block()

# Run REST API
# from pychain.api import RESTAPI
# api = RESTAPI(chain)
# api.run()
```

## Running Tests
```bash
python3 -m unittest tests/test_blockchain.py
```

## Directory Structure
```
pychain/
  blockchain.py
  consensus.py
  contracts/
    engines.py
    __init__.py
  transaction_types.py
  networking.py
  api.py
  governance.py
  __init__.py

/tests/
  test_blockchain.py
  __init__.py
```

## Extending PyChain
- Implement your own consensus, contract engine, transaction type, network feature, or governance mechanism by subclassing the relevant base class.
- Plug your custom class into the `Blockchain` constructor.

## License
MIT
