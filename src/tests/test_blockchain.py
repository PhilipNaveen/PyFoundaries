import unittest
import time
from pychain.blockchain import Blockchain
from pychain.consensus import PoWConsensus, DPoSConsensus
from pychain.contracts.engines import EVMEngine, NativeEngine
from pychain.transaction_types import (
    UTXOTransaction, AccountTransaction, ConfidentialTransaction,
    MultiSigTransaction, AtomicSwapTransaction, TimeLockedTransaction
)
from pychain.networking import NodeDiscovery, GossipProtocol, DHTProtocol, Sharding, MeshNetwork, LightningNetwork
from pychain.api import RESTAPI, CLIAPI
from pychain.governance import OnChainVoting, GovernanceToken, LiquidDemocracy, Futarchy, HardFork, SoftFork

class TestBlockchainFramework(unittest.TestCase):

    def test_transaction_sequence(self):
        # Account-based transactions
        balances = {'Alice': 100, 'Bob': 50, 'Carol': 0}
        tx1 = AccountTransaction('Alice', 'Bob', 30)
        self.assertTrue(tx1.validate(balances))
        balances = tx1.apply(balances)
        self.assertEqual(balances['Alice'], 70)
        self.assertEqual(balances['Bob'], 80)

        tx2 = AccountTransaction('Bob', 'Carol', 20)
        self.assertTrue(tx2.validate(balances))
        balances = tx2.apply(balances)
        self.assertEqual(balances['Bob'], 60)
        self.assertEqual(balances['Carol'], 20)

        # UTXO transactions
        utxo_set = {('tx0', 0): ('Alice', 50), ('tx0', 1): ('Bob', 30)}
        tx3 = UTXOTransaction(inputs=[('tx0', 0)], outputs=[('Carol', 50)])
        self.assertTrue(tx3.validate(utxo_set))
        utxo_set = tx3.apply(utxo_set)
        self.assertIn('Carol', [v[0] for v in utxo_set.values()])

        # Multi-sig transaction
        balances['Carol'] = 20
        tx4 = MultiSigTransaction(['Carol', 'Bob'], 2, 'Carol', 'Alice', 10)
        tx4.add_signature('sigCarol')
        tx4.add_signature('sigBob')
        self.assertTrue(tx4.validate(balances))
        balances = tx4.apply(balances)
        self.assertEqual(balances['Carol'], 10)
        self.assertEqual(balances['Alice'], 80)

        # Time-locked transaction
        unlock_time = time.time() - 1
        tx5 = TimeLockedTransaction('Alice', 'Bob', 5, unlock_time)
        self.assertTrue(tx5.validate(balances))
        balances = tx5.apply(balances)
        self.assertEqual(balances['Alice'], 75)
        self.assertEqual(balances['Bob'], 65)

        # Atomic swap transaction
        expiry = time.time() + 100
        tx6 = AtomicSwapTransaction('Bob', 'Carol', 5, hash('secret'), expiry)
        self.assertTrue(tx6.validate(balances))
        tx6.redeem('secret')
        balances = tx6.apply(balances)
        self.assertEqual(balances['Bob'], 60)
        self.assertEqual(balances['Carol'], 15)
    def test_pow_consensus(self):
        class DummyBlock:
            def __init__(self, hash):
                self.hash = hash
        pow = PoWConsensus({'type': 'PoW', 'params': {'difficulty': 2}})
        block = DummyBlock('00abc')
        self.assertTrue(pow.validate_block(block, []))
        block2 = DummyBlock('abc')
        self.assertFalse(pow.validate_block(block2, []))

    def test_dpos_consensus(self):
        dpos = DPoSConsensus({'type': 'DPoS', 'params': {'validators': ['A', 'B']}})
        class DummyBlock: pass
        self.assertTrue(dpos.validate_block(DummyBlock(), []))

    def test_native_contract_engine(self):
        class DummyContract:
            def foo(self, x):
                return x + 1
        engine = NativeEngine()
        cid = engine.deploy(DummyContract(), None, 'user')
        result = engine.interact(cid, 'foo', [5], 'user')
        self.assertEqual(result, 6)

    def test_utxo_transaction(self):
        utxo_set = {('tx1', 0): ('A', 10)}
        tx = UTXOTransaction(inputs=[('tx1', 0)], outputs=[('B', 10)])
        self.assertTrue(tx.validate(utxo_set))
        utxo_set = tx.apply(utxo_set)
        self.assertIn('B', [v[0] for v in utxo_set.values()])

    def test_account_transaction(self):
        balances = {'A': 10, 'B': 0}
        tx = AccountTransaction('A', 'B', 5)
        self.assertTrue(tx.validate(balances))
        balances = tx.apply(balances)
        self.assertEqual(balances['A'], 5)
        self.assertEqual(balances['B'], 5)

    def test_multisig_transaction(self):
        balances = {'A': 10, 'B': 0}
        tx = MultiSigTransaction(['A', 'C'], 2, 'A', 'B', 5)
        tx.add_signature('sigA')
        tx.add_signature('sigC')
        self.assertTrue(tx.validate(balances))
        balances = tx.apply(balances)
        self.assertEqual(balances['A'], 5)
        self.assertEqual(balances['B'], 5)

    def test_atomic_swap_transaction(self):
        balances = {'A': 10, 'B': 0}
        expiry = time.time() + 100
        tx = AtomicSwapTransaction('A', 'B', 5, hash('secret'), expiry)
        self.assertTrue(tx.validate(balances))
        tx.redeem('secret')
        balances = tx.apply(balances)
        self.assertEqual(balances['A'], 5)
        self.assertEqual(balances['B'], 5)

    def test_timelocked_transaction(self):
        balances = {'A': 10, 'B': 0}
        unlock_time = time.time() - 1
        tx = TimeLockedTransaction('A', 'B', 5, unlock_time)
        self.assertTrue(tx.validate(balances))
        balances = tx.apply(balances)
        self.assertEqual(balances['A'], 5)
        self.assertEqual(balances['B'], 5)

    def test_node_discovery_and_gossip(self):
        nd = NodeDiscovery()
        nd.add_peer('node1')
        nd.add_peer('node2')
        gossip = GossipProtocol(nd)
        gossip.broadcast('hello')
        self.assertIn('node1', nd.get_peers())

    def test_dht_protocol(self):
        dht = DHTProtocol()
        dht.put('key', 'value')
        self.assertEqual(dht.get('key'), 'value')

    def test_sharding(self):
        sharding = Sharding(num_shards=2)
        shard = sharding.get_shard('key')
        self.assertIsInstance(shard, dict)

    def test_mesh_network(self):
        mesh = MeshNetwork()
        mesh.connect('A', 'B')
        self.assertIn('B', mesh.get_connections('A'))

    def test_lightning_network(self):
        ln = LightningNetwork()
        ln.open_channel('A', 'B', 10)
        self.assertEqual(ln.get_channel('A', 'B'), 10)
        ln.close_channel('A', 'B')
        self.assertIsNone(ln.get_channel('A', 'B'))

    def test_rest_api(self):
        # Only test instantiation, not actual server run
        class DummyChain:
            chain = []
            def add_transaction(self, **kwargs): pass
        api = RESTAPI(DummyChain())
        self.assertIsNotNone(api)

    def test_cli_api(self):
        class DummyChain:
            def mine_block(self): pass
            def add_transaction(self, sender, recipient, amount): pass
        api = CLIAPI(DummyChain())
        self.assertIsNotNone(api)

    def test_governance(self):
        voting = OnChainVoting()
        voting.vote('p1', 'alice', 'yes')
        voting.vote('p1', 'bob', 'no')
        tally = voting.tally('p1')
        self.assertEqual(tally['yes'], 1)
        self.assertEqual(tally['no'], 1)

        token = GovernanceToken()
        token.mint('alice', 10)
        self.assertEqual(token.balance_of('alice'), 10)

        liquid = LiquidDemocracy()
        liquid.delegate('alice', 'bob')
        self.assertEqual(liquid.get_delegate('alice'), 'bob')

        futarchy = Futarchy()
        futarchy.create_market('p1')
        futarchy.bet('p1', 'yes', 5)
        self.assertEqual(len(futarchy.markets['p1']), 1)

        hardfork = HardFork()
        hardfork.fork(2)
        self.assertIn(2, hardfork.versions)

        softfork = SoftFork()
        softfork.add_restriction('rule')
        self.assertIn('rule', softfork.restrictions)

if __name__ == '__main__':
    unittest.main()
