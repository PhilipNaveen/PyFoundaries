import threading
import socket
import json

class Node:
    def __init__(self, address):
        self.address = address
        self.peers = set()

    def add_peer(self, peer_address):
        self.peers.add(peer_address)

    # Minimal stub for networking
    def broadcast(self, message):
        for peer in self.peers:
            try:
                host, port = peer.split(":")
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.connect((host, int(port)))
                    s.sendall(json.dumps(message).encode())
            except Exception as e:
                print(f"Failed to send to {peer}: {e}")
