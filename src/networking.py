import random

class NodeRole:
    FULL = "full"
    LIGHT = "light"
    ARCHIVE = "archive"
    MINING = "mining"
    VALIDATOR = "validator"

class NodeDiscovery:
    """Simple peer list management."""
    def __init__(self):
        self.peers = set()
    def add_peer(self, address):
        self.peers.add(address)
    def get_peers(self):
        return list(self.peers)

class GossipProtocol:
    """Broadcast messages to random peers."""
    def __init__(self, node_discovery):
        self.node_discovery = node_discovery
    def broadcast(self, message):
        peers = self.node_discovery.get_peers()
        for peer in random.sample(peers, min(3, len(peers))):
            print(f"Gossiping to {peer}: {message}")

class DHTProtocol:
    """Simple key-value store."""
    def __init__(self):
        self.store = {}
    def put(self, key, value):
        self.store[key] = value
    def get(self, key):
        return self.store.get(key)

class Sharding:
    """Partition chain state into shards."""
    def __init__(self, num_shards=2):
        self.num_shards = num_shards
        self.shards = [{} for _ in range(num_shards)]
    def get_shard(self, key):
        idx = hash(key) % self.num_shards
        return self.shards[idx]

class MeshNetwork:
    """Peer-to-peer mesh connections."""
    def __init__(self):
        self.connections = {}
    def connect(self, node_a, node_b):
        self.connections.setdefault(node_a, set()).add(node_b)
        self.connections.setdefault(node_b, set()).add(node_a)
    def get_connections(self, node):
        return self.connections.get(node, set())

class LightningNetwork:
    """Simple payment channel management."""
    def __init__(self):
        self.channels = {}
    def open_channel(self, node_a, node_b, amount):
        self.channels[(node_a, node_b)] = amount
    def close_channel(self, node_a, node_b):
        self.channels.pop((node_a, node_b), None)
    def get_channel(self, node_a, node_b):
        return self.channels.get((node_a, node_b))
