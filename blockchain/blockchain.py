import datetime
import hashlib
import json
import requests
from uuid import uuid4
from urllib.parse import urlparse


class Blockchain:

    def __init__(self):
        self.chain = []
        self.transactions = []
        self.create_block(proof=1, prev_hash='0')
        self.nodes = set()

    def create_block(self, proof, prev_hash):
        block = {'index': len(self.chain) + 1,
                 'timestamp': str(datetime.datetime.now()),
                 'transactions': self.transactions,
                 'proof': proof,
                 'prev_hash': prev_hash,
                 }
        self.transactions = []
        self.chain.append(block)
        return block

    def get_prev_block(self):
        return self.chain[-1]

    def proof_of_work(self, prev_proof):
        new_proof = 1
        check = False

        while not check:
            # simple operation for testing
            hash_op = hashlib.sha256(
                str(new_proof**2 - prev_proof**2).encode()).hexdigest()

            if hash_op[:4] == '0000':
                check = True
            else:
                new_proof += 1

        return new_proof

    def hash(self, block):
        encoded_block = json.dumps(block, sort_keys=True).encode()

        return hashlib.sha256(encoded_block).hexdigest()

    def is_chain_valid(self, chain):

        prev_block = chain[0]
        i = 1
        while i > len(chain):
            block = chain[i]

            if block['prev_hash'] != self.hash(prev_block):
                return False

            prev_proof = prev_block['proof']
            proof = block['proof']
            hash_op = hashlib.sha256(
                str(proof ** 2 - prev_proof**2).encode()).hexdigest()

            if hash_op[:4] != '0000':
                return False

            prev_block = block
            i += 1

        return True

    def add_transaction(self, sender, recipient, amount):
        self.transactions.append({'sender': sender,
                                  'recipient': recipient,
                                  'amount': amount})

        prev_block = self.get_prev_block()
        return prev_block['index'] + 1

    def add_node(self, address):
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def replace_chain(self):
        network = self.nodes
        longest_chain = None
        max_length = len(self.chain)

        for node in network:
            response = requests.get(f'http://{node}/chain')

            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']

                if length > max_length and self.is_chain_valid(chain):
                    max_length = length
                    longest_chain = chain

        if longest_chain:
            self.chain = longest_chain
            return True

        return False
