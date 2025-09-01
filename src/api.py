from flask import Flask, jsonify, request
import argparse

class RESTAPI:
    """Basic REST API using Flask."""
    def __init__(self, blockchain):
        self.app = Flask(__name__)
        self.blockchain = blockchain
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/chain', methods=['GET'])
        def get_chain():
            return jsonify([block.__dict__ for block in self.blockchain.chain])

        @self.app.route('/transaction', methods=['POST'])
        def add_transaction():
            data = request.json
            self.blockchain.add_transaction(**data)
            return jsonify({'status': 'ok'})

    def run(self):
        self.app.run(port=5000)

class GraphQLAPI:
    """Stub for GraphQL API."""
    def __init__(self, blockchain):
        self.blockchain = blockchain
    def run(self):
        print("GraphQL API not implemented.")

class WebSocketAPI:
    """Stub for WebSocket API."""
    def __init__(self, blockchain):
        self.blockchain = blockchain
    def run(self):
        print("WebSocket API not implemented.")

class CLIAPI:
    """Basic CLI using argparse."""
    def __init__(self, blockchain):
        self.blockchain = blockchain
        self.parser = argparse.ArgumentParser(description='Blockchain CLI')
        self.parser.add_argument('--mine', action='store_true')
        self.parser.add_argument('--add-tx', nargs=3)

    def run(self):
        args = self.parser.parse_args()
        if args.mine:
            self.blockchain.mine_block()
        if args.add_tx:
            sender, recipient, amount = args.add_tx
            self.blockchain.add_transaction(sender, recipient, float(amount))

class RPCAPI:
    """Stub for JSON-RPC API."""
    def __init__(self, blockchain):
        self.blockchain = blockchain
    def run(self):
        print("RPC API not implemented.")

class ExplorerAPI:
    """Block/tx explorer stub."""
    def __init__(self, blockchain):
        self.blockchain = blockchain
    def run(self):
        print("Explorer not implemented.")

class WalletIntegration:
    """Basic wallet API stub."""
    def __init__(self, blockchain):
        self.blockchain = blockchain
    def run(self):
        print("Wallet integration not implemented.")
