from datetime import datetime
import hashlib

class TestClass(object):
    """docstring for TestClass"""
    def __init__(self, test):
        #super(TestClass, self).__init__()
        self.test = test


class Block(object):
    """docstring for Block"""
    def __init__(self,index,proof,previous_hash,transactions):
        #super(Block, self).__init__()
        self.index = index
        self.proof = proof
        self.previous_hash = previous_hash
        self.transactions = transactions
        self.timestamp = datetime.now()

    def __repr__(self):
        return "{} - {} - {} - {} - {}".format(self.index, self.proof, self.previous_hash, self.transactions, self.timestamp)
    
    def get_block_hash(self):
        block_string = "{}{}{}{}".format(self.index,self.proof,self.previous_hash,self.transactions,self.timestamp)
        return hashlib.sha256(block_string.encode()).hexdigest()

class BlockChain(object):
    """docstring for BlockChain"""
    def __init__(self):
        self.chain = []
        self.current_node_transactions = []
        self.nodes = set()
        self.create_genesis_block()

    def create_genesis_block(self):
        self.create_new_block(0,0)

    def create_new_block(self,proof,previous_hash):
        block = Block(index = len(self.chain),
            proof = proof,previous_hash = previous_hash,
            transactions = self.current_node_transactions)
        self.current_node_transactions = []
        self.chain.append(block)
        return block
    
    def create_new_transaction(self,sender,recipient,amount):
        self.current_node_transactions.append({"sender" : sender,"recipient" : recipient,amount : "amount"})
        return self.last_block.index+1

    def mine_block(self,miner):
        self.create_new_transaction(0,miner,amount=1)
        last_block = self.last_block
        proof = self.create_proof_of_work(last_block.proof)
        new_block = self.create_new_block(proof,last_block.get_block_hash())
        return vars(new_block)

    def create_node(self, address):
        self.nodes.add(address)
        return True

    @property
    def get_serialized_chain(self):
        return [vars(block) for block in self.chain]

    def create_proof_of_work(self,previous_proof):
        proof = previous_proof + 1
        while (proof + previous_proof) % 7 != 0:
            proof += 1
        return proof
    
    @property
    def last_block(self):
        return self.chain[-1]