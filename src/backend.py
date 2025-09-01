import requests

class GethBackend:
    def __init__(self, rpc_url="http://localhost:8545"):
        self.rpc_url = rpc_url

    def rpc_call(self, method, params=None):
        payload = {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or [],
            "id": 1
        }
        response = requests.post(self.rpc_url, json=payload)
        return response.json()

    def deploy_contract(self, bytecode, abi, sender):
        # Minimal stub: send raw transaction
        tx = {
            "from": sender,
            "data": bytecode
        }
        return self.rpc_call("eth_sendTransaction", [tx])

    def send_transaction(self, tx):
        return self.rpc_call("eth_sendTransaction", [tx])

    def get_block_number(self):
        return self.rpc_call("eth_blockNumber")
